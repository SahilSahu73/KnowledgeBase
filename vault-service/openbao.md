# What is OpenBao
Identity-based secrets and encryption management system.

A modern sys requires access to multitude of secrets, including DB credentials, API keys for external services,
credentials for service oriented architecture communication, etc. It can be difficult to understand who is accessing
which secrets, especially since this can be platform-specific. Adding on key-rolling, secure storage, and detailed
audit logs requires a custom solution. This is where OpenBao steps in.
It validates and authorizes clients (users, machines, apps) before providing them access to secrets or stored
sensitive data.

# How does OpenBao Work (high level overview)
Works primarily with tokens and a token is associated to the client's policy.
Each policy is path-based and policy rules constrains the actions and accessibility to the paths for each client.
You can create tokens manually and assign them to your clients, or the clients can log in and obtain a token.

The core OpenBao workflow consists of 4 stages:
1. Authenticate: Authentication in OpenBao is the process by which a client supplies information that openbao uses
to determine if they are who they say they are. Once the client is authenticated against an auth method, a token is
generated and associated to a policy.
2. Validation: OpenBao validates the client against 3rd-party trusted sources, such as GitHub, LDAP, AppRole and more.
3. Authorize: A client is matched against the OpenBao security policy. This policy is a set of rules defining which API
endpoints a client has access to with its OpenBao token. Policies provide a declarative way to grant or forbid access to
certain paths and operations in OpenBao.
4. Access: OpenBao grants access to secrets, keys, and encryption capabilities by issuing a token based on policies
associated with the clients's identity. The client can then use their OpenBao token for future operations.


# Core System, Keyring and Barrier Cryptography
Core of OpenBao is a layered architecture designed to isolate logical client engines from physical storage.
This design ensures that the underlying storage system is treated as untrusted, meaning it never receives,
manages or processes plaintext secrets.

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

All read and write operations directed to the physical storage must pass through the cryptographic barrier.
Barrier secures the stored data by encrypting all outbound payloads using AES-GCM with a 256-bit key length.

Operates on either sealed or unsealed state.
When started, the service enters a sealed state where the core engine cannot decrypt any data in the storage backend.
Unsealing is the process of retrieving or reconstructing the plaintext Root Key (Master Key) required to decrypt OpenBao's
internal database keyring. This keyring stores the actual active Data Encrypting Key (DEK) used by the cryptographic barrier.

