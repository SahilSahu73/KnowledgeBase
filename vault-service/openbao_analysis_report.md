# Architectural Specification of a Multi-Tenant Cloud Vault Service: OpenBao Design and AWS KMS Key Management Integration
Managing cryptographic operations, sensitive configurations, and API credentials requires a centralized, secure, and resilient identity-based secrets management system. For a cloud service provider such as ESDS, relying on decentralized, static configurations or native storage systems creates significant security risks. It expands the potential exposure area during a breach and makes it difficult to verify access. To mitigate these vulnerabilities, ESDS requires a dedicated vault service to isolate secrets from application code and ensure continuous logging of all cryptographic operations.Because HashiCorp transitioned its core Vault platform to a restrictive Business Source License (BSL), integrating it into commercial cloud services carries significant licensing liabilities. OpenBao, an open-source fork of HashiCorp Vault managed under the Linux Foundation's LF Edge subproject and licensed under the Mozilla Public License 2.0 (MPL 2.0), provides a fully compatible alternative. It preserves the core API schemas while introducing community-driven enhancements such as horizontal read scalability and native multi-tenant namespaces. This technical report details the internal mechanics of OpenBao's storage engines, cryptographic operations, administrative subsystems, and logical multi-tenancy models. It also analyzes the architecture of AWS Key Management Service (KMS) to guide ESDS in building its own cloud-native key management platform.

## OpenBao Core Systems, Keyring, and Barrier Cryptography
At the core of OpenBao is a layered architecture designed to isolate logical client engines from physical storage. This design ensures that the underlying storage system is treated as untrusted, meaning it never receives, manages, or processes plaintext secrets.

+-------------------------------------------------------------------------+
|                          OpenBao Core Boundary                          |
|                                                                         |
|  +-------------------+     +---------------------+     +-------------+  |
|  |     HTTP API      | --> |  Core Routing Engine| --> |   Identity  |  |
|  |   (REST Client)   |     | (Auth/Policy Verify)|     |   Engine    |  |
|  +-------------------+     +----------+----------+     +-------------+  |
|                                       |                                 |
|                                       v                                 |
|                            +--------------------+                       |
|                            |   Cryptographic    |                       |
|                            |  Barrier (AES-GCM) |                       |
|                            +----------+---------+                       |
|                                       | (Barrier Encrypted Keyring)     |
+---------------------------------------v---------------------------------+
|                                                                         |
|                            +--------------------+                       |
|                            |  Untrusted Physical|                       |
|                            |   Storage (Raft)   |                       |
|                            +--------------------+                       |
+-------------------------------------------------------------------------+

## The Cryptographic Barrier and Vault States
All read and write operations directed to physical storage must pass through the cryptographic barrier. The barrier secures the stored data by encrypting all outbound payloads using the Advanced Encryption Standard in Galois Counter Mode with a 256-bit key length (AES-GCM-256). In addition to encrypting data at rest, AES-GCM-256 computes an authentication tag to protect the integrity of the data. This allows OpenBao to detect unauthorized modifications or data corruption in the physical storage layer.OpenBao operates in either a sealed or unsealed state. When started, the service enters a sealed state where the core engine cannot decrypt any data in the storage backend. Unsealing is the process of retrieving or reconstructing the plaintext Root Key (historically called the Master Key) required to decrypt OpenBao's internal database keyring. This keyring stores the actual active data encryption key (DEK) used by the cryptographic barrier.To prevent sensitive keys from being written to disk swap files, OpenBao uses the mlock system call on Linux platforms. This locks the physical memory pages containing the plaintext keyring and active barrier keys, preventing the operating system from writing this sensitive material to swap space on physical disks.

### Rekeying vs. Key Rotation
OpenBao distinguishes between updating unseal/recovery key materials and cycling the data encryption keys used to protect physical storage:Rekeying: This process modifies the threshold or structure of the unseal keys. During a rekey, OpenBao accepts a quorum of current unseal key shares, generates a new Root Key, and uses Shamir's Secret Sharing to split it into a new set of shares with updated threshold rules. The internal data encryption keys are then re-encrypted using this new Root Key.Key Rotation: This operation updates the internal encryption key used by the cryptographic barrier. When triggered, OpenBao generates a new AES-GCM-256 data key and appends it to the internal keyring. All subsequent write operations use this new key, while older keys remain in the keyring to decrypt legacy storage blocks.During key rotation in high-availability (HA) deployments, the active node creates a short-lived, ephemeral upgrade key encrypted under the previous internal key. Standby nodes retrieve this upgrade key to update their local memory-resident keyrings without requiring a manual unseal operation or cluster restart.

### Unseal Mechanisms: Shamir vs. Auto-Unseal
During initialization, OpenBao generates the central Root Key. To prevent a single administrator from gaining total control, OpenBao splits this Root Key using Shamir’s Secret Sharing. This algorithm generates $n$ unique unseal key shares, requiring a minimum threshold of $k$ shares to reconstruct the Root Key during startup.To avoid the manual coordination required to supply Shamir key shares after a node restart, ESDS can configure the Auto-Unseal mechanism. This delegates key protection to an external, trusted hardware security module (HSM) via PKCS#11 or a cloud Key Management Service.
Under an Auto-Unseal configuration:
OpenBao initializes and generates the central Root Key.
Instead of splitting the key using Shamir's algorithm, OpenBao encrypts (wraps) the Root Key using the external KMS or HSM key.
The resulting wrapped ciphertext is stored directly within the physical storage backend.
Upon reboot, the node retrieves this encrypted Root Key from physical storage and calls the external KMS API to decrypt it.
The external service decrypts and returns the plaintext Root Key, allowing OpenBao to automatically unseal and mount its physical storage engines.

  +-----------------------+      +------------------------+      +---------------------+
  | OpenBao Physical Boot | ---> | Fetch Encrypted Root   | ---> | Call Decrypt API on |
  |   (Auto-Unseal Config)|      | Key from Storage Layer |      | External KMS/HSM    |
  +-----------------------+      +------------------------+      +----------+----------+
                                                                            |
                                                                            v
  +-----------------------+      +------------------------+      +----------+----------+
  | OpenBao Core Unsealed | <--- | Decrypt Barrier DEK    | <--- | Receive Decrypted   |
  |  & Ready for Requests |      | from Active Keyring    |      | Plaintext Root Key  |
  +-----------------------+      +------------------------+      +---------------------+

## Deep-Dive into Secrets Engines
OpenBao isolates different types of secrets through path-based logical systems called Secrets Engines. Each engine behaves as a specialized plugin, handling key-value storage, dynamic certificate authority operations, or database credential management.

### Key-Value (KV) Engine: Version 1 vs. Version 2
The Key-Value engine stores arbitrary secrets within OpenBao's physical storage layer. ESDS can run this engine in one of two modes:
KV Version 1 (Non-Versioned)
This version stores only a single, active JSON payload for any given path. When a client writes new data to a path, the pre-existing secret is overwritten immediately. This mode offers better write performance and lower storage usage because it avoids the overhead of managing historical database records and locking schemas.
KV Version 2 (Versioned)
This version preserves a configurable history of secret versions (defaulting to 10) for each path. It achieves this by splitting the API path structure into separate prefixes: /data/ for reading and writing secret payloads, and /metadata/ for administrative and version control tasks.The KV Version 2 metadata schema contains several parameters:Meta ParameterData TypeFunctional Descriptioncurrent_versionIntegerThe latest numeric index of the active secret payload.oldest_versionIntegerThe earliest historical version index currently retained in storage.max_versionsIntegerThe maximum number of historical versions to keep before the oldest is purged.cas_requiredBooleanToggles mandatory Check-and-Set validation on all write requests.delete_version_afterDurationSpecifies an auto-expiry timeframe to delete versions after creation.custom_metadataMap[String]StringA key-value map for administrative tags, team owners, or descriptions.To prevent race conditions during updates, ESDS can enable the Check-and-Set (CAS) parameter. When active, a write operation must include the expected current version index. If another client has updated the secret in the interim, the version indices mismatch, and OpenBao rejects the write operation.When a secret version is deleted, OpenBao performs a soft-delete, updating the metadata to mark the version as inactive while preserving the underlying ciphertext. Deleted versions can be restored using the /undelete/ endpoint. To permanently remove a version's ciphertext, clients must call the /destroy/ endpoint, which physically overwrites the specific storage block.To resolve performance issues caused by linear scans of large datasets, OpenBao uses a dynamic indexing architecture based on B+ Trees. This allows attributes like certificate metadata or key-value structures to be indexed dynamically, reducing search complexities from $O(N)$ linear scans to $O(\log N)$ lookups.

### Transit Engine: Encryption-as-a-Service (EaaS)
The Transit secrets engine performs cryptographic operations on data in transit without persisting any input payloads to disk. It acts as a cryptographic oracle, accepting base64-encoded plaintexts over HTTP API calls and returning encrypted ciphertexts. It supports symmetric algorithms such as aes128-gcm96, aes256-gcm96 (the default), chacha20-poly1305, and xchacha20-poly1305, alongside asymmetric algorithms including RSA and ECDSA.
A standard Transit ciphertext is returned as a colon-separated string:
$$\text{vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX9vyf7w==}$$
H`The prefix vault identifies the ciphertext as a wrapped payload. The version tag v2 indicates that key version 1 was used to encrypt the payload, allowing OpenBao to automatically route decryption requests to the correct historical version in its keyring. The remaining string contains the base64-encoded initialization vector (IV) concatenated with the payload's ciphertext and its authentication tag.Key Derivation and Convergent EncryptionFor high-volume database column encryption, generating unique, random nonces for millions of rows can lead to operational bottlenecks and prevent query filtering based on exact matches. To address this, the Transit engine supports Key Derivation and Convergent Encryption:Key Derivation: When enabled (derived=true), all cryptographic operations require a base64-encoded context string. OpenBao derives a unique, context-specific cryptographic key from the master transit key using a Key Derivation Function (KDF).Convergent Encryption: This mode ensures that identical inputs yield identical ciphertexts. When enabled, OpenBao derives both the encryption key and the initialization vector (nonce) deterministically from a combination of the derived key and the plaintext data. This allows application systems to perform exact-match lookups on encrypted database columns without decrypting the data beforehand.Key Import and Plaintext BackupsTo migrate existing cryptographic architectures, ESDS can import external keys into the Transit engine. The import sequence wraps the target symmetric or asymmetric key using an ephemeral symmetric wrapper before transit:The client generates an ephemeral 256-bit AES key.The client wraps the target key using this ephemeral AES key with the AES-KWP algorithm.The client encrypts the ephemeral key under the OpenBao wrapping key using RSAES-OAEP with MGF1.The client appends the wrapped target key to the wrapped ephemeral key, base64-encodes the compiled payload, and posts it to OpenBao’s import endpoint.For data recovery purposes, the Transit engine supports plaintext backups. When a key is created with allow_plaintext_backup=true, authorized administrators can retrieve the key material in plaintext. This parameter is immutable once set, ensuring the configuration cannot be modified later to bypass security rules.Public Key Infrastructure (PKI) Engine: TLS Certificate IssuanceThe PKI secrets engine automates the generation and signing of dynamic X.509 certificates. This allows services to retrieve certificates on demand without going through manual CSR submissions or verification queues.OpenBao can generate a self-signed root CA or act as an intermediate CA by generating a CSR to be signed by an external enterprise offline Root CA. The generated private keys are stored within the cryptographic barrier and are marked as non-exportable to prevent exposure.The standard certificate lifecycle in OpenBao is driven by roles. A role defines the parameters of certificate issuance, such as maximum Time-to-Live (TTL), allowed domains, subdomain wildcards, and cryptographic key parameters.                Client                        PKI Engine Role
                  |                                  |
                  | --- POST /pki/issue/my-role ---> |
                  |     { "common_name": "db.foo" }  |
                  |                                  |
                  |                                  v [Validates against Role Policies]
                  |                                  | [Generates Private Key & Cert]
                  |                                  | [Registers Serial to Storage]
                  |                                  |
                  | <--- Returns PEM Bundle ---------|
                  |      (Cert, Key, Chain)          |
The PKI secrets engine supports standard ACME directory integrations, allowing external clients to automate certificate lifecycle management. The engine handles http-01, dns-01, and tls-alpn-01 validation challenges natively. For enterprise configurations, the PKI engine supports External Account Binding (EAB) tokens to validate and link incoming ACME registration requests back to authorized internal accounts.Common Expression Language (CEL) Integration in PKITo support more complex, dynamic validation requirements than standard roles allow, OpenBao integrates Google's Common Expression Language (CEL) into the PKI engine. Using the /pki/cel/ endpoints, administrators can define programmatic policies that validate, mutate, or reject incoming certificate requests in real-time:Code snippet// Example CEL expression validating SAN domains and adjusting key usages
request.common_name.endsWith("esds.co.in") && 
parsed_csr.dns_names.all(d, d.endsWith("esds.co.in"))
The evaluation context provides variables such as now (timestamp), request (raw parameters), and parsed_csr (the structured CSR). The evaluation output must return a structured ValidationOutput object:Gotype ValidationOutput struct {
    Template             CertTemplate // Matches the target x509.Certificate fields
    IssuerRef            string       // Points directly to the target signer identifier
    UsePSS               bool         // Defines if RSA-PSS signatures are required
    GenerateLease        bool         // Toggles whether an OpenBao lease is created
    NoStore              bool         // If true, skips storing the certificate in the database
}
This capability allows ESDS to write dynamic logic, such as:Validating that subject alternative names (SANs) match metadata values bound to the requesting OIDC authentication token.Automatically shortening certificate validity windows based on the classification of the requesting client.Conditionally skipping persistent storage for short-lived certificates (no_store = true) to prevent database storage amplification.Database Secrets EngineThe Database secrets engine manages database credentials dynamically. Rather than storing static connection strings inside application configurations, client systems request dynamic credentials from OpenBao. OpenBao then connects to the target database engine, executes administrative SQL creation queries, and returns a short-lived username and password pair.   Client                  Database Engine                   Target DB
     |                            |                              |
     | --- GET /creds/my-role --> |                              |
     |                            v [Retrieves role template]    |
     |                            |                              |
     |                            | --- Runs CREATE USER ------> |
     |                            |     & GRANT queries          |
     |                            |                              |
     |                            | <--- Confirms user creation -|
     |                            |                              |
     | <--- Returns username -----|                              |
     |      and password          |                              |
OpenBao supports two distinct operational modes for credentials:Dynamic Roles: For every request to /database/creds/:name, OpenBao generates a unique database user. It interpolates the {{name}}, {{password}}, and {{expiration}} values into configured SQL statements. This ensures each microservice instance operates within its own security boundary, facilitating precise auditing and access control.Static Roles: A static role maps directly to a pre-existing, single database account. OpenBao stores the password for this user and automatically rotates it at a configurable interval (rotation_period), ensuring the credentials are regularly cycled without manual intervention.To execute these operations, the Database engine relies on a modular, RPC-based plugin framework. The OpenBao core connects to independent plugin binaries via GRPC bindings, enforcing process-level separation.To build a custom database driver for a proprietary ESDS database, the developer must implement the standard dbplugin.Database interface from the OpenBao SDK:Gotype Database interface {
    Initialize(ctx context.Context, req InitializeRequest) (InitializeResponse, error)
    NewUser(ctx context.Context, req NewUserRequest) (NewUserResponse, error)
    UpdateUser(ctx context.Context, req UpdateUserRequest) (UpdateUserResponse, error)
    DeleteUser(ctx context.Context, req DeleteUserRequest) (DeleteUserResponse, error)
    Type() (string, error)
    Close() error
}
When an application's lease expires, OpenBao's internal engine triggers the DeleteUser RPC. This runs a configured SQL revocation statement to clean up database privileges and drop the user account from the database engine.Technical Infrastructure ComponentsTo establish a production-grade, multi-tenant deployment, ESDS must configure several infrastructure subsystems within the vault architecture. +---------------------------------------------------------------------------------+
 |                                    OpenBao                                      |
 |                                                                                 |
 |  +--------------------+   +-----------------------+   +----------------------+  |
 |  |  Raft Consensus    |   |     Fail-Closed       |   | Lease Manager        |  |
 |  |  Active/Standby    |   |     Audit Engine      |   | (Dynamic Lease TTL)  |  |
 |  +--------------------+   +-----------------------+   +----------------------+  |
 |                                                                                 |
 |  +--------------------+   +-----------------------+   +----------------------+  |
 |  | Identity Engine    |   |     Pathways Policy   |   | Namespaces Engine    |  |
 |  | (Entities, Aliases)|   |     (ACL Evaluator)   |   | (Tenant Separation)  |  |
 |  +--------------------+   +-----------------------+   +----------------------+  |
 +---------------------------------------------------------------------------------+
Cryptography, Key Management, and Storage ResilienceOpenBao clusters support high availability (HA) deployments using Integrated Storage, which relies on the Raft Consensus Protocol. In a Raft-backed HA architecture, each cluster node acts as an independent storage unit, replicating state changes across all nodes. To maintain consensus and successfully commit transactions, Raft requires a majority quorum:$$Q = \left\lfloor \frac{N}{2} \right\rfloor + 1$$Where $N$ represents the total number of voting nodes in the cluster, requiring an odd number of nodes to ensure partition tolerance.OpenBao supports horizontal read scalability, allowing unsealed standby nodes to handle read requests locally. These standby nodes route only write operations and lease renewals back to the active leader.                           +------------------------+
                           |  Client Read Request   |
                           +-----------+------------+
                                       |
                                       v
                           +------------------------+
                           |  Standby Node (Read)   |
                           |   [Serves Read Locally] |
                           +-----------+------------+
                                       |
                        (If Write)     v
                           +------------------------+
                           |   Active Leader Node   |
                           |   [Processes Write]    |
                           +------------------------+
To maintain data consistency across nodes, OpenBao uses index headers. Standby nodes append the current Raft transaction index to their response headers, allowing clients to detect stale reads and verify that their queries align with the latest replicated state.Audit Logging: Non-Trivial Fail-Closed SecurityFor a cloud provider, keeping tamper-proof records of administrative and cryptographic operations is critical for maintaining security and compliance. OpenBao processes every incoming request and outgoing response through its core audit engine.To ensure data confidentiality, the audit log engine parses all JSON request payloads and replaces sensitive values (such as passwords, tokens, and secret data keys) with an HMAC-SHA256 hash using an internal salt. This allows security operators to correlate matching input parameters across systems without exposing the raw plaintext values within log repositories.For certain operational workflows where tracking key values in plaintext is necessary, administrators can use the -audit-non-hmac-request-keys and -audit-non-hmac-response-keys parameters to exempt specific API fields from default hashing.The Fail-Closed MechanismOpenBao enforces a strict logging constraint: no API write or read request is permitted to succeed unless it has been successfully written to at least one configured audit device. If an audit device becomes blocked or encounters an error (such as a full disk partition, network socket termination, or syslog daemon hang), the entire OpenBao node halts processing. It blocks subsequent API interactions and returns HTTP 500 errors to clients to maintain audit trail integrity.To avoid single-point operational failures, ESDS should configure multiple independent audit logging devices, such as local files, syslog endpoints, and remote HTTP webhook listeners:Terraform# Enabling multiple, parallel audit devices in OpenBao config
path "sys/audit/file-sink" {
  capabilities = ["sudo", "create", "update"]
}
If one logging sink fails while another remains operational, OpenBao continues processing transactions while generating alerts about the degraded state.Leases, TTLs, and Revocation PipelinesEvery dynamic secret, database credential, and TLS certificate issued by OpenBao is bound to a lease. A lease contains an explicit Time-to-Live (TTL) duration that defines the validity window of the secret.OpenBao implements two main configuration limits for TTL values:Default TTL: The initial duration assigned to a lease if the client does not specify a lifetime.Maximum TTL: The upper limit for lease extensions, preventing clients from renewing a secret indefinitely.When a lease reaches its expiration limit, OpenBao’s internal system triggers an automated revocation routine.                                  +----------------------+
                                  | Lease Expiry Reached |
                                  +----------+-----------+
                                             |
                                             v
                                  +----------------------+
                                  | OpenBao Core Engine  |
                                  |  [Triggers Revoke]   |
                                  +----------+-----------+
                                             |
                                             v
                                  +----------------------+
                                  | Core API Endpoint /  |
                                  | DB Engine Plugin     |
                                  +----------+-----------+
                                             |
                                             v
                                  +----------------------+
                                  | Target Resource      |
                                  | [Removes Credentials]|
                                  +----------------------+
The system administrator can also initiate manual, prefix-based revocations to handle security incidents or rotated configurations:Single Revocation: Targets a specific lease identifier (such as database/creds/my-role/abc123), prompting OpenBao to connect to the downstream service and clean up the associated resource.Prefix Revocation: Targets a broader path (such as database/creds/my-role/), executing a cascade revocation that invalidates all active credentials issued under that path.Force Revocation: If a downstream database engine or external cloud endpoint becomes unavailable, standard revocation attempts can fail and block the pipeline. In such cases, operators can run a force revocation using the -force flag. This removes the lease metadata from OpenBao's storage layer immediately, bypassing the downstream cleanup calls to restore operational processing.JWT/OIDC Authentication and Identity EngineTo integrate with container orchestration systems, CI/CD runners, and enterprise single sign-on (SSO) directories, OpenBao supports JSON Web Token (JWT) and OpenID Connect (OIDC) authentication.During authentication, the client sends a cryptographically signed JWT to OpenBao’s /login endpoint. OpenBao verifies the token's authenticity using one of several configured methods:Static Key Verification: Comparing the signature against a pre-configured, local public key.JWKS Endpoint Query: Fetching active public keys dynamically from a designated JSON Web Key Set (JWKS) URL.OIDC Discovery: Querying the .well-known/openid-configuration metadata endpoint of the identity provider to locate signature verification keys automatically.Once verified, OpenBao validates claims such as aud (audience), iss (issuer), and exp (expiration) against the parameters defined in the mapped login role.The Identity Engine: Entities, Aliases, and GroupsInstead of treating each login as an isolated, short-lived token session, OpenBao parses authentication metadata into a persistent Identity Engine.                 +-----------------------------------------------+
                 |                Identity Engine                |
                 |                                               |
                 |               +---------------+               |
                 |               |    Entity     |               |
                 |               |  "Bob Smith"  |               |
                 |               +-------+-------+               |
                 |                       |                       |
                 |          +------------+------------+          |
                 |          v                         v          |
                 |   +------+------+           +------+------+   |
                 |   |    Alias    |           |    Alias    |   |
                 |   | (OIDC/Okta) |           |   (LDAP)    |   |
                 |   +-------------+           +-------------+   |
                 +-----------------------------------------------+
Entities: An Entity represents a single, unique identity representation within OpenBao. It serves as a centralized mapping resource across multiple authentication backends.Aliases: An Alias connects an entity to a specific account within an authentication backend (such as a unique LDAP username or OIDC subject claim). This allows OpenBao to associate separate login events from different providers back to the same logical entity.Groups: Entities can be grouped into logical units. This allows security teams to apply authorization policies globally to entire teams rather than managing access permissions for individual accounts.By applying policies directly to identity entities or groups rather than short-lived tokens, OpenBao can evaluate and update access privileges dynamically at request time.Pathways Policies: Fine-Grained AuthorizationOpenBao’s access control mechanism is built on path-based policies, evaluating client permissions against requested paths using a default-deny model. Policies are written in HashiCorp Configuration Language (HCL) or JSON, defining the operations a client can execute.The authorization engine matches paths using glob (*) and wildcard (+) parameters, using a lexicographical evaluation hierarchy to resolve overlapping rules:Terraform# Access control definitions for ESDS client system
path "secret/data/tenants/tenant-a/*" {
  capabilities = ["create", "read", "update"]
  allowed_parameters = {
    "tier" = ["standard", "premium"]
  }
}

path "secret/data/tenants/tenant-a/restricted" {
  capabilities = ["deny"]
}
The system maps standard operations to HTTP API verbs:create / update -> POST / PUTread -> GETlist -> LIST (custom HTTP verb)sudo -> Grants access to root-protected administrative endpoints.deny -> Explicit block that overrides all other permissions.To control data access more granularly, ESDS can configure parameter constraints within policies:allowed_parameters: Restricts client requests to specified parameters and values.denied_parameters: Explicitly blocks specified fields while permitting all others.list_scan_response_keys_filter_path: This configuration enables prefix filtering on LIST operations. When enabled, OpenBao checks each item in a list response against the user's explicit policy permissions, removing any keys the client is not authorized to read before returning the results. This prevents directory harvesting and ensures tenants can only discover resources they own.Multi-Tenancy and NamespacesFor cloud service providers, ensuring strict tenant isolation is critical. OpenBao provides multi-tenant isolation through logical partitions called Namespaces, which act as independent "mini-vaults" within a single cluster. / (Root Cluster Space)
 ├── platform.infra/
 └── tenants/
     ├── tenant-a/ (Namespaced Policies, Secret Engines, Auth Methods)
     │   └── dev/
     └── tenant-b/ (Isolated Keyrings, Metadata, Identity Profiles)
Each namespace operates with its own isolated configuration, containing its own policies, authentication methods, secrets engines, and identity groups.This logical segregation allows ESDS to delegate administrative capabilities to individual tenants, enabling them to self-manage secrets engines, auth roles, and policies within their own namespace without affecting other users.To implement multi-tenancy at scale, ESDS can combine namespaces with custom metadata:Assign each tenant a dedicated top-level namespace path (e.g., tenants/tenant-a/).Mount dedicated KVv2 engines within each tenant’s namespace.Inject custom tenant metadata (such as billing identifiers and environment tags) directly into the KVv2 paths.Bind JWT/OIDC authentication methods directly to namespaced roles. This ensures that client pipelines automatically authenticate against their own isolated namespace, keeping their credentials separate from other tenants.AWS Key Management Service (KMS) Deep-DiveAWS Key Management Service (KMS) is a fully managed, multi-tenant service that provides centralized control over the cryptographic keys used to protect cloud data. To design a resilient vault service for ESDS, it is helpful to analyze how AWS KMS structures its internal workflows, hardware boundaries, and envelope encryption model.       AWS KMS Front-End (Web Fleet API Tier)
                 |
                 v [Terminates TLS with Perfect Forward Secrecy]
                 v [Authenticates via IAM Credential Policies]
                 |
       ========================================================= [Security Boundary]
       Hardware Security Module (HSM) Cryptographic Tier
                 |
                 v [Hybrid RNG: Entropy + NIST SP800-90A DRBG]
                 |
                 +---> Domain Key (sitting in HSM volatile RAM only)
                       |
                       +---> HSA Backing Key (HBK)
                             |
                             +---> Customer Managed Key (CMK / KMS Key)
                                   |
                                   +---> Data Encryption Key (DEK)
KMS Front-End and HSM Cryptographic BoundariesThe AWS KMS architecture is divided into two primary tiers: web-facing KMS front-end hosts and dedicated, physical Hardware Security Modules (HSMs).KMS Front-End Hosts: These web-facing servers handle initial API request routing and TLS termination, enforcing perfect forward secrecy. They authenticate incoming requests using AWS Identity and Access Management (IAM) policies.HSMs: All cryptographic operations and key generation are executed within FIPS 140-3 Level 3 validated HSMs, which establish a physical security boundary. Plaintext customer master keys are kept in the volatile memory of these HSMs and are never written to disk or exposed to AWS operators.To generate random numbers securely, the HSMs use a hybrid random number generator. It uses a Deterministic Random Bit Generator (DRBG) conforming to the NIST SP800-90A standard, specifically utilizing CTR_DRBG with a 256-bit AES core. This generator is seeded with 384 bits of entropy from a hardware-based, non-deterministic physical generator, providing high prediction resistance.The AWS KMS Key HierarchyAWS KMS enforces strict logical separation through a multi-tiered key hierarchy:+---------------------------------------------------------------------------------+
| Level 1: Domain Key (Sitting in HSM Volatile RAM Only)                          |
+---------------------------------------------------------------------------------+
                                       | (Encrypts)
                                       v
+---------------------------------------------------------------------------------+
| Level 2: HSA Backing Key (HBK)                                                  |
+---------------------------------------------------------------------------------+
                                       | (Encrypts)
                                       v
+---------------------------------------------------------------------------------+
| Level 3: Customer Managed Key (CMK / KMS Key)                                   |
+---------------------------------------------------------------------------------+
                                       | (Encrypts)
                                       v
+---------------------------------------------------------------------------------+
| Level 4: Data Encryption Key (DEK)                                              |
+---------------------------------------------------------------------------------+
Domain Key (Level 1): The root of the hierarchy. This AES-GCM 256-bit symmetric key is generated inside the HSMs and resides exclusively in volatile memory. It is shared across HSM clusters within a specific AWS Region and is rotated regularly.HSA Backing Key (HBK) / Key Encryption Key (Level 2): Derived from the Domain Key, HBKs are intermediate key encryption keys that protect customer-specific master keys.Customer Managed Key (CMK / KMS Key) (Level 3): The logical key resource managed by the AWS customer. It is stored as an encrypted metadata structure inside AWS’s physical storage layer, wrapped by an HBK.Data Encryption Key (DEK) (Level 4): Generated on demand by calling the GenerateDataKey API, the DEK is used by client applications to encrypt larger datasets.Envelope Encryption and Service GeneralizationAWS KMS is designed to handle high performance and scalability. Because encrypting large datasets directly through network API calls can introduce high latency and overhead, KMS uses a pattern known as Envelope Encryption. AWS KMS API                                                  Client Host
     |                                                             |
     | <--- 1. Call GenerateDataKey(CMK) ------------------------- |
     |                                                             |
     | --- 2. Generate random 256-bit key -----------------------> |
     |        Decrypts under CMK to produce ciphertext             |
     |                                                             |
     | --- 3. Return { Plaintext DEK, Encrypted DEK } ---------->  |
     |                                                             |
     |                                                             v [Encrypts file locally with AES]
     |                                                             v [Destroys Plaintext DEK from RAM]
     |                                                             v [Stores Encrypted DEK with data]
Under this model, data encryption is handled locally by client applications or AWS services using data keys:The client invokes the GenerateDataKey API, passing the identifier of their KMS Key (CMK).The KMS HSM generates a secure, random 256-bit symmetric key using its internal random number generator.KMS encrypts this generated data key under the customer's CMK, producing an encrypted data key.KMS returns both the plaintext data key and the encrypted data key to the client.The client uses the plaintext data key to encrypt their raw data locally using symmetric algorithms like AES-GCM-256.Once local encryption is complete, the client purges the plaintext key from memory and stores the encrypted data key alongside the encrypted ciphertext.When the client needs to read the data, they send the encrypted data key back to the AWS KMS Decrypt API. KMS decrypts the key within its HSM boundary and returns the plaintext key to the client, allowing them to decrypt their data locally. This design pattern minimizes API traffic, limits network overhead, and ensures that sensitive data keys are never exposed in transit or stored in plaintext.To generalize key management across different cloud environments, AWS integrates KMS directly into its core services using three distinct key classifications:Key TypeLifecycle OwnershipFinancial ImplicationsAccess VisibilityCustomer Managed KeyCreated, configured, and deleted entirely by the customer.Subject to monthly hosting fees and excess API usage costs.Full visibility. Operations are logged as CloudTrail events.AWS Managed KeyCreated and managed automatically by AWS on behalf of a specific service (e.g., S3 or EBS).Free hosting. API usage fees apply above the free tier.Partial visibility. Customers can view policies and CloudTrail logs.AWS Owned KeyExclusively owned and managed internally by AWS across multiple customer accounts.Completely free of charges.No visibility. Key metadata and operations are hidden from customer logs.This classification model allows AWS services to configure encryption by default. By using AWS Owned keys, services like Amazon S3 can automatically encrypt customer data without introducing management overhead or API costs. For applications requiring fine-grained access control, developers can transition to Customer Managed Keys, which allow them to define precise IAM permissions and key policies for specialized compliance needs.Architectural Synthesis and Platform AlignmentFor ESDS to implement a secure, multi-tenant secrets management service, aligning OpenBao with the design principles of cloud architectures is key. The table below compares the core capabilities of OpenBao against AWS KMS to assist in planning deployment strategies:Evaluation VectorOpenBao Platform ConfigurationAWS KMS Architecture DesignLicensing FrameworkMozilla Public License 2.0 (Open Source)Proprietary (Closed Cloud Service Model)Underlying Physical BoundaryVirtualized Servers, Bare-Metal Nodes, or Kubernetes [cite: 4, 5, LKE]Dedicated Hardware Appliances without hypervisorsCryptographic CoreStandard open-source crypt/rand library componentsCustom FIPS 140-3 Level 3 Hardware Security ModulesMulti-Tenancy ModelNamespaces (Logical isolation within a single cluster)Separate Account IAM Policies, Groups, and GrantsCredential GenerationGenerates dynamic database users and dynamic PKI certificatesGenerates data keys (symmetric and asymmetric key pairs)High Availability EngineRaft consensus with horizontal read replicationRegionally distributed managed service clustersSecurity ValidationAudited independently against open standardsIntegrates with international frameworks (SOC 1/2/3, FIPS 140-3)Architectural Recommendations for ESDSBased on the capabilities and structures of both platforms, ESDS can design its proprietary secrets management service using the following strategies:Production Storage Layer (Raft Consensus): ESDS should avoid single-node standalone deployments for production workloads, as they lack high availability and failover mechanisms. Instead, deploy a multi-node OpenBao cluster (with a minimum of 3 to 5 nodes) using Integrated Storage with the Raft Consensus Protocol. This ensures data is consistently replicated across all nodes, preventing split-brain scenarios and data loss.Delegated Auto-Unseal Pipeline: To reduce the operational complexity of managing Shamir unseal keys manually, configure ESDS OpenBao nodes to use an Auto-Unseal driver. This can connect to an internal physical HSM via PKCS#11 or a regional key provider to unseal nodes automatically on reboot.Logical Isolation via Namespaces: Implement ESDS multi-tenancy by mapping tenants to unique, non-overlapping namespaces. Configure each namespace with its own isolated authentication mounts, policy engine, and KVv2 dynamic engines to keep tenant spaces separate.Strict Fail-Closed Logging Sinks: Configure at least two independent audit logging devices (e.g., local file sinks and remote HTTP webhook listeners) to avoid single-point operational failures. This ensures that if one logging device goes offline, OpenBao continues processing transactions while generating alerts about the degraded state, rather than blocking operations.Local Envelope Encryption Pattern: For internal cloud products, encourage developers to use OpenBao’s Transit engine in an envelope encryption pattern. This shifts high-volume encryption operations to client nodes using short-lived, local keys, keeping key management centralized while minimizing latency and network overhead.
