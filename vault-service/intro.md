# Vault
Essentially a secret management Tool.

What are Secrets?
Information we use to login or authorize with various services.
like user name and password for login or API token.

There are 2 types of users who need to use these secrets to access those services:
Humans and System User.
Username and password credentials.
The application can also need access to DBs, or payment gateways etc.
If anyone gets access to these keys then it can be misused and cause havoc.
SSH key pairs, TLS certificates - to encrypt and secure frontend and backend communication


Where these secrets are stored ?
In reality they can be everywhere or anywhere in text format - locally in notepad or confluence pages etc.
Huge security failure.
This is called secret sprawl.
2 huge problems with this:
 - We don't have any track of how many secrets there are and where they are stored.
 - We don't know who accessed what and when?
 - Also if API gets stolen then what to do, how to auto revoke, because if we delete old key and create new key then have to update
 at all places the new key.
 Also what if secrets are rotated once in a while, have to manage that as well.

## Capabilities of Secrets Management Tools
Purpose of these tools:
  - Offer centralized platform to manage all secrets, simplifying the administration and access control.
  - Provide a secure storage solution, protecting them from unauthorized access and potential leaks.

Instead of storing everything in plain text at one place, it encrypts everything.
Encryption at rest and Encryption in Transit
It is stored in a secured place in secured format, and encrypted even while sending (i.e. in transit)

Fine grained access control - admin can define who can access which secret - often integrated with identity and access management systems.
Can grant or forbit access to certain secrets or operations.
Ensure engineers and apps only have access to the secrets they need.

Audit and Compliance
- detailed logs of access and changes to secrets.
- Help organizations meet regulatory compliance requirements by tracking access to sensitive information.

Generate Dynamic Credentials:
Instead of generating static credentials, like long-lived credentials - credentials that never expire like the real API key and account
passwords - Vault lets us create short-lived credentials with short expiration periods or one time use.
Vault destroys credentials when validity period expires.
Creates dynamically on-demand.
Dynamic secrets minimizes risk as by the time the hacker finds and tries to use them it might already get expired and for hacking they need
time to access it.

From an auditing perspective as well every client will get its own unique, newly created short-lived credential.
So in case the credential gets leaked, then we will know from where or who leaked it.
And then credential rotation is needed for that client only - hence preventing outage

Encryption as a Service
- for regular data which are not considered secrets but are sensitive and private information that needs to be kept safe.
  like Personal Identifiable Information (PII)
- Vault allows to encrypt and decrypt the data (in transit and at rest) stored in our database.
- Vault handles the complexities of encryption key generation, storage, and lifecycle management.

## How Vault Works
Core:
 - vault server is the central component that processes all requests.
 - Manages the flow of requests through the system, enforces ACLS and ensures audit logging is done.
 - API driven system - all communication b/w clients and vault are done through API.
 - For storing different types of secrets vaults have different types of secret engines
    - example: Key/Value secret engine - used to store username and password.
    - or Database secret engine - generates DB credentials dynamically based on configured roles.
    - RabbitMQ secret engine - same as DB but based on configured permissions and virtual hosts.
    - PKI engines - for certification managements - generates dynamic X.509 certificates - relieves the burden of handling the complex
    certificates - Avoids having long-lived certificates.
    - SSH secret engine - provides secure authentication and authorization for access to machines via the SSH protocol.
    - Kubernetes secret engine - generates K8s service account tokens.

Comes with various pluggable components allowing us to integrate with external systems.
It uses the mechanisms of those tools to create temporary credentials for clients.

questions:
etcd and vault relation
Do we need to connect/store kv pairs of etcd in vault ?

Master node - primary vault
cert manager - do we need vault for this.


The entire nuance of namespaces is I think to have isolation and multi-tenancy when we just have one of that. For example the network namespaces controls the same Wlan and eth0 connection but gives the users/services an
interface to think of it as an individual component dedicated to them and that service can control it, but in reality
internally there is just one. Basically virtualization.


