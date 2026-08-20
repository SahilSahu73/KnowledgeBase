# Swaraaj Vault Service — Architecture Plan & Design Discussion

> **Status:** Draft v1 for discussion · **Author:** Principal Architecture review (Claude) · **Date:** 2026-06-29
> **Core engine:** OpenBao **v2.5.5** (open-source, MPL-2.0) · CLI binary `bao`
> **Scope:** Multi-tenant, self-hosted secrets-management product integrated with the Swaraaj Portal.

This document evaluates the proposed architecture, identifies what is strong and what is risky, proposes a hardened and more scalable design, and specifies every major flow and its security controls. It is grounded in a thorough review of current OpenBao documentation (sources listed at the end).

---

## 1. Executive summary

Your instinct — **one dedicated OpenBao instance per client, fronted by a single control plane integrated with the Swaraaj Portal** — is a sound, defensible model for a security product at your scale (20–100 clients). It gives strong tenant isolation, clean per-client billing/monitoring, and a small blast radius per tenant. We keep that shape.

We make **three substantive changes** to make it secure and scalable:

1. **Do not store client-vault login credentials in the control-plane vault.** This is the highest-risk part of the original plan — it makes the control-plane vault a single key to every client's secrets. Replace it with **federated, zero-stored-credential access**: OIDC for human users, Kubernetes auth for the control plane's machine access, and just-in-time **response-wrapped, single-use** credentials for the rare cases that need them. The control-plane vault then holds only *non-secret* connection metadata and tightly-controlled break-glass material. (See §4 and §6.)

2. **Use OpenBao namespaces for within-client product/service isolation** (a free OSS feature in OpenBao, unlike Vault). A **hybrid model** — one namespace per product/service for hard admin isolation, plus templated policies inside — gives each of a client's products real autonomy without per-secret policy sprawl. (See §5.)

3. **Operationalize for fleet scale from day one** — Transit auto-unseal, GitOps/operator-driven provisioning, automated snapshot CronJobs (automated snapshots are *not* in OSS), dual audit devices, and per-tenant network isolation. (See §9–§14.)

The result is a **three-plane architecture**: a **Control Plane**, a **Data Plane** (the fleet of per-client OpenBao instances), and a small hardened **Trust/Unseal Plane** (the Transit auto-unseal vault + root-of-trust). The control plane is an *orchestrator and proxy*, never a credential warehouse.

---

## 2. Decisions locked in this discussion
---
| Dimension | Decision | Rationale |
|---|---|---|
| Tenant model | One OpenBao instance per client | Strong isolation, clean per-client monitoring/billing |
| Scale target | 20–100 clients (2–3 yr) | Instance-per-client is sustainable with automation |
| K8s isolation | Namespace-per-client (NetworkPolicy + ResourceQuota + StatefulSet) | Good isolation/density balance |
| Within-client tenancy | **Namespaces per product/service + templated policies** (hybrid) | OpenBao namespaces are OSS; gives real delegation |
| Identity | **OIDC federation** from **Keycloak** (Swaraaj Portal IdP) | No long-lived vault tokens; self-hosted IdP fits on-prem; flexible group/claim mapping |
| Client capability | Full self-service: secrets + users/access + engines/policies | Drives the control-plane API surface & policy model |
| Auto-unseal | **Transit auto-unseal** via a dedicated hardened unseal vault | No cloud dependency; scales to the whole fleet |
| **Root-of-trust seal** | **Shamir on the *one* unseal vault** (offline-split shares, dual control), unsealed only on rare restart; upgrade to PKCS#11/HSM or KMIP if hardware becomes available | No cloud KMS allowed; HSM availability TBD. Hand-unseal **one** vault, not the fleet |
| Compliance | SOC 2 / ISO 27001, **single India region**, tamper-evident audit | Drives audit, retention, scheduling, isolation |
| Client tiers | **Single instance profile for now** (tiering deferred) | Simpler launch; sizing table kept as a future tiering reference |
| DR / HA | 3-node Raft quorum + automated encrypted snapshots (single India region) | OSS has no replication; snapshot-restore is the DR path |
| OpenBao version | **v2.5.5 minimum** | Namespace stability/deadlock fixes land in 2.5.x |
---

## 3. Why OpenBao OSS is sufficient (and where it is not)

OpenBao is the Linux-Foundation MPL-2.0 fork of HashiCorp Vault (forked from Vault 1.14, the last MPL release). Crucially for us, **several features that are Enterprise-only and license-restricted in HashiCorp Vault are free and open-source in OpenBao**:

| Capability | OpenBao OSS | HashiCorp Vault |
|---|---|---|
| **Namespaces** (multi-tenancy) | ✅ OSS since v2.3, stable v2.5.5 | 💲 Enterprise only |
| **Performance standby nodes** (read scaling) | ✅ OSS since v2.5.0 | 💲 Enterprise only |
| **Transform engine** (FPE, masking, tokenization) | ✅ OSS | 💲 Enterprise (ADP) |
| **PKCS#11 / HSM auto-unseal** | ✅ OSS since v2.2.0 | 💲 Enterprise only |
| Integrated Raft storage, KV/PKI/Transit/DB/SSH | ✅ | ✅ |
| OIDC/JWT, Kubernetes, AppRole, LDAP, Userpass auth | ✅ | ✅ |

**What OpenBao OSS does *not* have (must design around):**

- ❌ **Cross-cluster replication (Performance & DR Replication)** — Enterprise-only in Vault, *not on OpenBao's near-term roadmap*. **Implication:** our DR strategy must be **snapshot-and-restore**, not live replication. (See §13.)
- ❌ **Automated snapshots to object storage** — Enterprise-only. **Implication:** we build snapshot scheduling ourselves with Kubernetes CronJobs. (See §13.)
- ❌ **Sentinel policy engine** — OpenBao has CEL-based policies (narrower). ACL + templated policies cover our needs.
- ❌ **FIPS 140-3 builds** — open issue. Relevant only if a client contractually requires FIPS-validated crypto.
- ⚠️ **Namespace *sealing*** (per-namespace cryptographic key isolation) is in v2.6.0-beta, **not yet stable**. We treat namespaces as a logical/administrative boundary, not a cryptographic one (the instance boundary is our cryptographic boundary).

> **Net:** OpenBao OSS covers this product fully. The only true gaps (replication, automated snapshots) are operational and we solve them at the platform layer.

---

## 4. High-level architecture: three planes

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  SWARAAJ PORTAL (existing)  ── OIDC IdP / SSO ──┐                              │
└───────────────┬─────────────────────────────────┼──────────────────────────────┘
                │ user logs in, opens "Vault" tile │ (OIDC tokens, group claims)
                ▼                                   ▼
┌──────────────────────────────── CONTROL PLANE ─────────────────────────────────┐
│  ┌────────────────────┐   ┌──────────────────────┐   ┌───────────────────────┐ │
│  │ Vault Dashboard SPA │──▶│ Control-Plane API     │──▶│ Control-Plane Vault    │ │
│  │ (client + admin)    │   │ (orchestrator/proxy)  │   │ (KV: metadata only,    │ │
│  └────────────────────┘   │  • tenant registry    │   │  NO client creds)      │ │
│                            │  • provisioning       │   └───────────────────────┘ │
│                            │  • OIDC broker/proxy  │   ┌───────────────────────┐ │
│                            │  • metrics aggregator │──▶│ Tenant Registry DB     │ │
│                            └──────────┬────────────┘   │ (Postgres: mappings)   │ │
│                                       │                └───────────────────────┘ │
└───────────────────────────────────────┼────────────────────────────────────────┘
            machine auth (Kubernetes auth, no stored secrets)  │  user OIDC token (proxied)
                                         ▼
┌──────────────────────────────── DATA PLANE (per-client fleet) ─────────────────┐
│  k8s ns: client-acme           k8s ns: client-globex        k8s ns: client-…    │
│  ┌──────────────────────┐      ┌──────────────────────┐     ┌────────────────┐ │
│  │ OpenBao StatefulSet   │      │ OpenBao StatefulSet   │    │ OpenBao …       │ │
│  │ 3-node Raft (HA)      │      │ 3-node Raft (HA)      │    │                 │ │
│  │ namespaces:           │      │ namespaces:           │    │                 │ │
│  │  product-a/ product-b/│      │  payments/ shipping/  │    │                 │ │
│  │ OIDC auth (federated) │      │ OIDC auth (federated) │    │                 │ │
│  └──────────┬───────────┘      └──────────┬───────────┘     └────────────────┘ │
└─────────────┼──────────────────────────────┼─────────────────────────────────────┘
              │ seal "transit" (auto-unseal)  │
              ▼                                ▼
┌──────────────────────── TRUST / UNSEAL PLANE (hardened, isolated) ─────────────┐
│  ┌───────────────────────────────┐   Break-glass: Shamir recovery keys (offline,│
│  │ Unseal Vault (Transit engine) │   split across officers, in a safe).          │
│  │ 3-node Raft, KMS/HSM or        │   Root tokens: generated on demand, revoked   │
│  │ static-key sealed (root of     │   immediately. Never stored.                  │
│  │ trust)                         │                                              │
│  └───────────────────────────────┘                                              │
└────────────────────────────────────────────────────────────────────────────────┘
```

### Plane responsibilities

- **Control Plane** — the only thing the client touches. It is an **orchestrator + authenticating reverse proxy**, plus a small **control-plane vault** (KV) for *non-secret* tenant metadata and a **registry DB** (Postgres) for mappings. It provisions instances, brokers OIDC logins, proxies dashboard API calls to the right client vault, and aggregates metrics/audit summaries.
- **Data Plane** — the fleet of per-client OpenBao instances. Each is a 3-node Raft StatefulSet in its own Kubernetes namespace, with OIDC auth federated to the portal and internal OpenBao *namespaces* for the client's products/services.
- **Trust / Unseal Plane** — a single, heavily-restricted OpenBao whose Transit engine auto-unseals every data-plane instance, plus the offline root-of-trust material (recovery key shares, break-glass). This plane has the smallest attack surface and the tightest network policy in the system.

---

## 5. Within-client multi-tenancy: products & services

Inside a single client's OpenBao instance, we represent the client's products/services with the **hybrid model**:

```
client-acme OpenBao instance (root namespace = the client)
├── namespace: product-a/
│    ├── auth/oidc/         → bound to IdP groups "acme:product-a:*"
│    ├── secret/  (KV v2)   → templated policy isolates by env/service
│    ├── database/          → dynamic DB creds for product-a services
│    └── policies: product-a-admin, product-a-dev, …
├── namespace: product-b/
│    ├── auth/oidc/         → bound to IdP groups "acme:product-b:*"
│    ├── secret/  (KV v2)
│    └── pki/               → product-b's internal CA
└── namespace: shared/      → cross-product shared secrets (optional)
```

**Why namespaces here (not just mounts):** each product team gets genuine administrative autonomy — their own auth config, their own policies, their own mounts — and a `namespace admin` cannot see or affect a sibling namespace. Nested namespaces support a hierarchy like `product-a/prod` and `product-a/dev`.

**Templated policies inside a namespace** give per-service/per-env isolation without writing a policy per service. Example (KV v2 requires both `data/` and `metadata/` paths):

```hcl
# product-a/dev developer policy: each service only sees its own prefix,
# keyed off an OIDC claim copied into entity metadata via claim_mappings.
path "secret/data/{{identity.entity.metadata.service}}/*" {
  capabilities = ["create", "read", "update", "patch", "delete"]
}
path "secret/metadata/{{identity.entity.metadata.service}}/*" {
  capabilities = ["read", "list"]
}
```

**Important constraints we design around (from the docs):**
- KV v2 ignores `allowed_parameters`/`denied_parameters` — don't rely on them there.
- Templated-policy failures surface only as `permission denied` (no debug tooling) — so we keep a **policy test harness** in CI that asserts effective access per role.
- For AppRole-authenticated workloads, template off **alias metadata** (`role_name`) via the mount accessor, not `entity.name`.
- Namespaces share one physical storage backend (no per-namespace storage isolation yet) — acceptable because the **instance** is the hard isolation boundary between *clients*.

> **Decision:** Namespace = product/service boundary (delegation). Templated policy = env/service sub-isolation. The client (or their product admins) manages this via the dashboard, which calls the control-plane API, which calls the client vault with the *user's own* federated token.

---

## 6. The critical security revision: no stored client-vault credentials

### The problem with the original plan

> *"The control plane vault stores login details of clients' OpenBao instances; on login it fetches the client's vault credentials and uses them."*

This makes the **control-plane vault a single key to every client's secrets**. If it is compromised (or an insider with control-plane access goes bad), *every* client vault falls at once. That is the worst-possible blast radius for a security product and would be a SOC 2 / ISO 27001 finding.

### The fix: federate identity, broker nothing long-lived

We use **three credential-free or short-lived mechanisms** instead:

**(a) Human users → client vault: OIDC federation (no stored creds).**
Each client OpenBao instance has an **OIDC auth method** trusting the Swaraaj Portal IdP. When a user opens their vault dashboard, the control plane runs the OIDC flow *against that client's vault* and the dashboard then operates with the **user's own short-lived token**, scoped by their group claims to the right namespace/policies. The control plane never holds a password or static token for the user.

**(b) Control plane → client vault (machine ops: provisioning, metrics, snapshots): Kubernetes auth (no stored creds).**
The control plane runs in the same Kubernetes cluster. Each client vault has a **Kubernetes auth role** bound to the control-plane service account, granting a **narrow, purpose-specific policy** (e.g., read health/metrics, create namespaces on request). The control plane authenticates with its **projected service-account token** — there is no secret to store anywhere. Tokens are short-lived (15 min) and minted per operation.

**(c) Anything that genuinely needs a secret handed across a boundary: response-wrapped, single-use AppRole.**
For the rare cases where (a)/(b) don't fit (e.g., an out-of-cluster agent), the broker issues a **response-wrapped, single-use SecretID** (`secret_id_num_uses=1`, `secret_id_ttl=60s`). Only the wrapping token transits; the secret never appears in logs; the path is validated (`sys/wrapping/lookup`) before unwrap; a failed unwrap is a security event.

### What the control-plane vault then actually stores

Only **non-secret operational metadata** and **break-glass material**:
- Per-client instance **connection metadata**: API address, CA certificate, namespace layout, tier, region. (Not credentials — knowing the address grants nothing without auth.)
- **Break-glass recovery material**: e.g., references to recovery-key custodians, emergency procedures. Actual recovery key *shares* are **split (Shamir) and stored offline**, never whole in the vault.
- Platform-internal config (feature flags, tenant tier policies).

> **Blast-radius result:** compromising the control plane no longer yields any client's secrets — an attacker still has to pass each client vault's OIDC/K8s auth and is bounded by short TTLs, per-tenant policy, and audit. This is the single most important hardening in the design.

The **Tenant Registry** (client→instance→namespace mappings, billing, status) lives in a normal **Postgres** DB, not the vault — it's relational metadata, not secrets.

---

## 7. Detailed flows (with security controls at each step)

### 7.1 Client user opens their vault dashboard (the primary flow)

```mermaid
sequenceDiagram
    participant U as Client User
    participant P as Swaraaj Portal (IdP/SSO)
    participant CP as Control-Plane API
    participant REG as Tenant Registry (Postgres)
    participant CV as Client OpenBao (acme)
    U->>P: Log in to Swaraaj Portal (SSO)
    P-->>U: Session + OIDC identity (groups: acme:product-a:dev)
    U->>CP: Open "Vault" dashboard (portal session/JWT)
    CP->>CP: Validate portal session; extract tenant=acme
    CP->>REG: Look up acme → instance addr, CA, namespaces
    CP->>CV: Begin OIDC auth (authorization-code + PKCE) on behalf of user
    CV->>P: Validate ID token against IdP JWKS / discovery
    CV->>CV: Map groups_claim → external group → policies (per namespace)
    CV-->>CP: Short-lived client_token (TTL 15m, user's policies)
    CP-->>U: Dashboard renders (token held server-side in CP proxy session)
    U->>CP: e.g. "list secrets in product-a/dev"
    CP->>CV: API call with user's token (X-Vault-Namespace: product-a/)
    CV->>CV: ACL/templated-policy check; AUDIT every request
    CV-->>CP: Result
    CP-->>U: Rendered result
```

**Security controls:** portal session validated → tenant pinned server-side (user can never select another tenant) → user's *own* OIDC identity drives policy in the client vault → token is short-lived and never persisted → every request audited in the client vault → control plane only proxies, holds no standing credential.

### 7.2 Control-plane machine access (provisioning / metrics / snapshots)

```mermaid
sequenceDiagram
    participant CP as Control-Plane (pod, SA token)
    participant CV as Client OpenBao
    participant K8s as Kubernetes TokenReview
    CP->>CV: auth/kubernetes/login (projected SA JWT, role=control-plane-ops)
    CV->>K8s: TokenReview(SA token)
    K8s-->>CV: valid; ns=control-plane, sa=cp-operator
    CV->>CV: Bind role → narrow policy (health, metrics, ns-admin-on-request)
    CV-->>CP: client_token TTL 15m
    CP->>CV: sys/metrics, sys/health, or namespace create (scoped)
    CV-->>CP: result (audited)
```

**Security controls:** no secret stored — identity is the pod's projected SA token, validated by Kubernetes; least-privilege policy; 15-min tokens minted per task; CIDR-bindable; fully audited. Provisioning privileges (create namespace, enable engine) are separated from read privileges via distinct K8s roles.

### 7.3 A client's *application/workload* fetches a secret (the day-2 value)

This is what the client's own services do in production — the real payoff of the platform.

```mermaid
sequenceDiagram
    participant App as Client workload (pod)
    participant CV as Client OpenBao (their namespace)
    participant DB as Backing database
    App->>CV: auth/kubernetes/login (SA JWT) OR AppRole (wrapped SecretID)
    CV-->>App: short-lived token (policy = service's prefix only)
    App->>CV: read database/creds/orders-ro  (dynamic secret)
    CV->>DB: CREATE ROLE … VALID UNTIL (TTL 1h)
    CV-->>App: username/password, lease_id (TTL 1h, renewable)
    Note over App,CV: Lease auto-revoked at TTL; rotation is free.
```

**Security controls:** prefer **dynamic, short-TTL credentials** (DB, PKI, SSH) over static KV; per-service policy via templating; leases revocable instantly on incident (`bao lease revoke -prefix`); the OpenBao Agent / CSI provider / External Secrets Operator can deliver these without app code changes.

### 7.4 Admin (you) monitoring across all clients

The admin dashboard is a **separate control-plane surface** authenticated by *your* staff IdP groups (e.g., `swaraaj:platform-admin`). It reads **aggregated** data only:
- Per-instance health (`/v1/sys/health`), seal status, Raft autopilot state.
- Prometheus metrics (`/v1/sys/metrics?format=prometheus`) scraped per instance.
- Audit **summaries** (counts, anomalies) — *not* secret values (audit logs HMAC sensitive fields anyway).
- Usage/billing rollups from the registry.

Admins **cannot read client secret values** through the platform UI by default; any such access is a **break-glass, dual-control, fully-audited** path (see §16). This separation is essential for client trust and SOC 2.

### 7.5 Break-glass / emergency root access

Root tokens are **never stored**. When genuinely needed:
1. `bao operator generate-root -generate-otp` on a secure host.
2. Recovery-key custodians (Shamir quorum, e.g., 3 of 5) each submit their share.
3. Resulting root token is used for the one emergency task, then **revoked immediately** (`bao token revoke`).
All steps audited; the procedure requires ≥2 officers (dual control).

---

## 8. Control-plane design

**Components:**
- **Dashboard SPA** (client + admin variants) — talks only to the control-plane API; never directly to client vaults.
- **Control-plane API** (stateless, horizontally scaled) — responsibilities:
  - *Tenant resolution & pinning* (portal session → tenant; never client-selectable).
  - *OIDC broker/proxy* — runs the OIDC flow against the target client vault; holds the user token only for the request/session, server-side.
  - *Provisioning orchestrator* — creates/decommissions instances and namespaces (via the operator / GitOps, see §12).
  - *Metrics & audit aggregator* — scrapes per-instance telemetry, builds dashboards.
  - *API surface for self-service*: secrets CRUD (proxied with user token), user/role management, engine/policy management — each mapped to OpenBao API calls under the user's token + correct `X-Vault-Namespace`.
- **Control-plane vault** — KV-only, metadata + break-glass (see §6).
- **Tenant Registry (Postgres)** — client, instance, namespace, tier, region, status, billing counters.

**Hardening:** the control-plane API is the internet-facing tier, so it gets WAF, strict authN/Z, rate limiting, mTLS to data-plane, structured request logging, and its own audit trail. It is **stateless** w.r.t. secrets (tokens are short-lived and request-scoped).

---

## 9. Per-client OpenBao instance design (Kubernetes)

**Topology (per client, in its own k8s namespace):**
- **StatefulSet, 3-node Raft** (HA; tolerates 1 failure). Offer **5-node** for premium/critical tier (tolerates 2). Integrated Storage (Raft) — the recommended K8s backend; no Consul.
- **Headless service** for Raft peer DNS + **ClusterIP service** for client traffic.
- **Pod anti-affinity** (`requiredDuringScheduling` on `kubernetes.io/hostname`) — one peer per node.
- **PodDisruptionBudget** `maxUnavailable: 1` — protect quorum during drains.
- **PVC** `ReadWriteOnce`, sized per tier; separate `auditStorage` PVC.
- **Probes:** readiness `/v1/sys/health?standbyok=true&sealedcode=204&uninitcode=204`, liveness `/v1/sys/health?standbyok=true` (so standbys stay in the Service).
- **Telemetry** stanza with `prometheus_retention_time` for scraping.
- **TLS everywhere** (listener mTLS; per-instance certs from an internal PKI).

**Deployment tooling:** the **official OpenBao Helm chart** (`openbao/openbao`, chart `0.28.4`, K8s ≥1.30). Note `updateStrategyType: OnDelete` — upgrades are a deliberate, ordered pod-deletion (standbys first, active last). See §12 for fleet automation.

**Resource sizing (community baseline — OpenBao publishes no official numbers; benchmark before committing):**

| Tier | CPU req/limit | Mem req/limit | Nodes | PVC |
|---|---|---|---|---|
| Small | 250m / 500m | 256Mi / 512Mi | 3 | 10Gi |
| Medium | 500m / 1000m | 512Mi / 1Gi | 3 | 20Gi |
| Premium | 1000m / 2000m | 1Gi / 2Gi | 5 | 50Gi |

> ⚠️ The Helm chart ships **no resource limits by default** — we must set them per tier or a noisy tenant can starve neighbors. Combine with `ResourceQuota` per k8s namespace.

---

## 10. Auto-unseal architecture (Trust / Unseal Plane)

Manual Shamir unsealing does not scale to 20–100 instances. We use **Transit auto-unseal**:

- A dedicated, hardened **Unseal Vault** (3-node Raft) exposes a Transit engine. Each data-plane instance config has:

```hcl
seal "transit" {
  address         = "https://unseal-vault.trust-plane.svc:8200"
  mount_path      = "transit/"
  key_name        = "autounseal-acme"          # per-client key for blast-radius control
  # auth via Kubernetes auth (env-injected short-lived token), NOT a static token
  tls_ca_cert     = "/etc/openbao/tls/ca.crt"
  tls_server_name = "unseal-vault"
}
```

- **Per-client Transit unseal keys** (`autounseal-<client>`) so revoking one client's unseal capability is surgical.
- **Recovery keys** (not unseal keys) are generated for auto-unsealed client instances; used only for `generate-root`/admin quorum, split offline.

### 10.1 How the Unseal Vault itself is sealed (the root of trust)

This is the unavoidable "turtles all the way down" question: the unseal vault auto-unseals the fleet, but **something must unseal the unseal vault**. The root of trust must bottom out in either **hardware** (HSM/TPM) or **human-held key shares** (Shamir). There is no secure way to *fully* auto-unseal the root without an external hardware anchor — a static-key seal merely relocates the secret to a less-protected place and **fails compliance**. Given the constraints (no cloud KMS; HSM availability TBD):

**Confirmed approach (launch): Shamir on the *one* unseal vault.**
- The unseal vault is the **only** vault sealed with Shamir keys (e.g., **3-of-5**), with shares **split offline** across trusted officers (separate custodians/locations, dual control). It is hand-unsealed **only on rare full-restart events**.
- This satisfies the requirement directly: you manually unseal **one** vault, and it then **auto-unseals all 20–100 client vaults**. You never hand-unseal the fleet.
- **Minimize restart events** so the manual step is rare: run the unseal vault as a **3–5 node HA Raft** cluster with node/rack anti-affinity and a PodDisruptionBudget — a simultaneous loss of the whole quorum should be a planned-maintenance event, not a routine one. Keep a documented, drilled unseal runbook (which officers, where shares are, dual-control sign-off).

**Upgrade path (eliminate the manual step) — investigate with infra:**
- **PKCS#11 / HSM** — OpenBao supports PKCS#11 **in OSS** (Enterprise-only in Vault). *Any* on-prem HSM — even a modest network HSM appliance, or a server **TPM** fronted via a PKCS#11 token — lets the unseal vault auto-unseal with **zero human action**. This is the preferred end state; confirm hardware availability.
- **On-prem KMIP appliance** — OpenBao can act as a KMIP unseal client. If the datacenter has any KMIP-compatible key manager, that is another fully-automated, no-cloud root seal.

**Hard rule:** never seal the root with something weaker than what it protects. No static-key seal for the unseal vault; no chaining the unseal vault's seal back to itself (circular).

- **Network posture:** the unseal vault has the tightest NetworkPolicy in the system — only `data-plane → unseal:8200`, nothing else; no general ingress; HA so it is highly available for on-demand unseal calls.
- **Transit auth:** client instances authenticate to the unseal vault's Transit engine via **Kubernetes auth** (env-injected short-lived token), not a static token embedded in config.

---

## 11. Secret engines & mapping to client self-service capability

You chose **full self-service** (secrets + users/access + engines/policies). Map to OpenBao features and gate by role:

| Client capability | OpenBao mechanism | Notes / guardrails |
|---|---|---|
| Manage secrets | KV v2 (versioned) | per-product namespace; templated policy by service/env |
| Dynamic DB creds | Database engine | short TTL; client configures connection + roles |
| Internal PKI | PKI engine | client issues short-lived certs; max-TTL capped by platform |
| Encryption-as-a-service | Transit | client encrypt/decrypt without holding keys |
| SSH access | SSH engine (signed certs) | short-lived CA-signed certs |
| Manage users & access | OIDC roles + Identity groups/entities | group claims → policies; client admins map their teams |
| Manage engines | `sys/mounts` (scoped) | **platform caps** which engine types are allowed per tier |
| Manage policies | `sys/policies/acl` (in their namespace) | linting + max-TTL/limits enforced by control-plane validation |

> **Guardrail:** "manage engines/policies" is powerful. The control-plane API **validates and constrains** every such request (allow-list of engine types, max-TTL ceilings, forbidden `sudo`/root-only paths, policy linting) *before* proxying to the vault — so self-service can't be used to escalate or exceed the tenant's tier.

---

## 12. Provisioning & lifecycle automation (fleet of 20–100)

Manual per-instance ops won't scale. Options, in order of preference:

1. **GitOps + Helm (recommended baseline):** each client is a Helm release described in Git (Argo CD / Flux). A new client = a new values file + an automated bootstrap Job that runs `operator init` (auto-unseal → recovery keys captured into the break-glass flow), enables OIDC/K8s auth, creates the client's product namespaces, and applies base policies. Declarative, auditable, reviewable — ideal for SOC 2 change management.
2. **Community lifecycle operator (`dc-tec/openbao-operator`, pre-GA):** offers `OpenBaoCluster`, `OpenBaoTenant`, `OpenBaoRestore` CRDs (TLS, backups, upgrades, scaling). Attractive but **pre-GA — breaking changes possible**; evaluate in staging, don't bet production on it yet.
3. **Custom operator** later if scale/complexity warrants.

**Secret delivery to client workloads:** prefer **External Secrets Operator** (the archived `openbao-secrets-operator` is dead) or the **OpenBao Agent injector** (`openbao-k8s`) / **CSI provider**.

> ⚠️ **Supply-chain item (SOC 2):** the OpenBao Helm chart has historically defaulted the injector image to `hashicorp/vault-k8s`. **Pin and verify** all images to OpenBao-built, digest-pinned references in a private registry.

---

## 13. DR, HA, and backup

- **HA:** 3-node Raft per instance (5 for premium). **Autopilot** for dead-server cleanup — *enable explicitly* (`cleanup_dead_servers=true`, `min_quorum=3`); it's off by default.
- **No replication in OSS** → DR = **snapshot/restore**.
- **Automated snapshots (we build this):** a Kubernetes **CronJob** per instance runs `bao operator raft snapshot save` on a schedule, pushes the file to **object storage with Object Lock / WORM** (covers tamper-evidence + India residency by choosing region). Snapshots contain the *encrypted* keyring, so they're safe at rest — **but restore requires the same seal** (the Transit unseal key must still exist). **Therefore: protect and version the Transit unseal keys as carefully as the snapshots** — losing them makes backups unrecoverable.
- **Restore runbook:** spin instance, ensure matching `seal "transit"` + key present, `bao operator raft snapshot restore`, verify peers/autopilot. Point-in-time (data after snapshot is lost) — set RPO via snapshot frequency (e.g., hourly).
- **Cross-region DR (later):** ship snapshots to a second region/cluster; restore on failover. This is the OSS path to site failover absent replication.

---

## 14. Audit, logging, monitoring (SOC 2 / ISO 27001)

- **Dual audit devices per instance** (e.g., `file` → log-shipper → WORM **and** `syslog`/`http`). Rationale: if the *only* audit device blocks, **OpenBao stops serving requests** — two devices on different transports avoid a single sink hanging the vault while preserving "at least one recorded it."
- **HMAC:** sensitive fields are HMAC-SHA256'd with a per-instance salt by default — keep `log_raw=false`. Use `sys/audit-hash` to test for a known value without exposing it.
- **Shipping:** write to file/stdout → Fluentd/Vector → object storage with **Object Lock (WORM)** + defined retention → SIEM. Region-pin for residency.
- **Metrics:** scrape `/v1/sys/metrics?format=prometheus` (active node only) → Prometheus/Grafana. Watch `vault.raft.*`, `vault.expire.*` (leases), `vault.runtime.*`, autopilot health, seal status.
- **Alerting:** seal events, audit-device failure, Raft leadership flaps, quorum loss, lease blowups, auth failure spikes (AppRole lockout after 5 fails / 15 min).

---

## 15. Network & isolation

- **k8s namespace per client** + **default-deny NetworkPolicies**: client pods reach only their own OpenBao service; OpenBao reaches only its Raft peers + the Unseal Vault.
- **ResourceQuota + LimitRange** per namespace (prevents noisy-neighbor starvation; pairs with the per-tier resource limits).
- **mTLS everywhere**; per-instance certs from internal PKI; the control plane reaches data-plane over mTLS only.
- **Trust plane** is the most locked-down: only `data-plane → unseal:8200`. No general ingress.
- **Ingress:** only the control-plane API is internet-facing (behind WAF + rate limiting). **Client vaults are never directly internet-exposed** — all client access is proxied through the control plane.

---

## 16. Security model & threat summary (per-step)

| Threat | Control |
|---|---|
| Control-plane compromise → all client secrets | **Eliminated as a single point**: no stored client creds; federated OIDC + K8s auth + short TTLs (§6) |
| Cross-tenant access | Instance-per-client (hard boundary) + k8s NetworkPolicy + per-namespace OIDC binding + templated policy |
| Stolen user session | Short-lived tokens, tenant pinned server-side, per-request audit, OIDC re-auth |
| Insider admin reads client secrets | Admin UI exposes aggregates only; secret access is break-glass, dual-control, audited |
| Long-lived/leaked credentials | Prefer dynamic secrets; response-wrapped single-use SecretIDs; periodic short tokens; instant lease revoke |
| Lost root token | Root never stored; `generate-root` via recovery-key quorum, revoke after use |
| Audit tampering | HMAC fields + WORM/Object-Lock shipping + dual devices |
| Backup theft | Snapshots encrypted (keyring); useless without the Transit unseal key |
| Unseal-vault compromise | Smallest surface, tightest NetworkPolicy, KMS/HSM-sealed, per-client unseal keys limit blast radius |
| Supply chain (images) | Digest-pinned, OpenBao-built images in private registry; verify injector image |
| Self-service privilege escalation | Control-plane validates/constrains every engine/policy request before proxying |

**Residual risks to accept/track:** namespaces share physical storage (not cryptographically isolated until per-namespace sealing is stable in 2.6+); OSS has no replication (DR is restore-based, non-zero RPO); OpenBao publishes no official sizing (we benchmark). All are acceptable at this scale with the mitigations above.

---

## 17. Scalability roadmap — and when instance-per-client stops working

At **20–100 clients**, instance-per-client is sustainable *with the automation above*. Watch these signals; when they trip, evolve:

- **Cost/density:** ~3 pods + PVCs per client. At many hundreds of small clients this dominates cost. **Mitigation / next step:** a **tiered model** — premium clients keep dedicated instances; the long tail of small clients moves into **shared instances partitioned by OpenBao namespaces** (now that namespaces are OSS-stable, a namespace can represent a *whole small client* on a shared instance). This is the natural escape hatch and a strong reason we invested in the namespace model early.
- **Control-plane scaling:** stateless API scales horizontally; registry DB is the state — standard Postgres HA.
- **Read load:** enable **performance standbys** (OSS in 2.5) for read-heavy tenants.
- **Operational toil:** if per-instance upgrades/snapshots get heavy, graduate from GitOps+Helm to a hardened operator (custom or a matured `dc-tec` operator).
- **DR maturity:** add cross-region snapshot shipping, then automated restore drills.

---

## 18. What you should study next (reading list)

1. **OpenBao Namespaces** — concept + CLI + `/sys/namespaces` API (the core of within-client tenancy).
2. **Integrated Storage (Raft)** — internals, autopilot, snapshot save/restore, quorum sizing.
3. **Seal/Transit auto-unseal** + **seal migration** — the unseal plane.
4. **JWT/OIDC auth** — roles, `bound_claims`, `groups_claim`, `claim_mappings`; **Identity** entities/groups/aliases; **policy templating**.
5. **Kubernetes auth** — TokenReview, projected SA tokens, alias metadata for templated policies.
6. **Audit devices** — blocking behavior, HMAC, multi-device, WORM shipping.
7. **OpenBao Helm chart** (`run`/`examples`, incl. snapshot CronJob) + **Agent injector / CSI / External Secrets Operator**.
8. **AppRole + response wrapping** — for any cross-boundary credential delivery.
9. **Telemetry/metrics** + `/sys/health` semantics for K8s probes.
10. **OpenBao vs Vault feature/licensing delta** — so you know exactly what's OSS.

---

## 19. Phased implementation roadmap

- **Phase 0 — Foundations (PoC):** stand up the Trust/Unseal Vault (KMS/HSM or Shamir), one client instance via Helm with Transit auto-unseal, OIDC auth wired to a test IdP. Validate the §7.1 dashboard flow end-to-end with namespaces + templated policies.
- **Phase 1 — Control plane MVP:** tenant registry, OIDC broker/proxy, secrets CRUD proxy, per-instance health/metrics. Admin monitoring (read-only aggregates).
- **Phase 2 — Self-service depth:** user/role management, engine/policy management with control-plane validation guardrails; dynamic secrets (DB/PKI) enablement.
- **Phase 3 — Productionize:** GitOps provisioning, dual audit + WORM shipping, snapshot CronJobs, NetworkPolicies/quotas, alerting, runbooks (break-glass, restore, upgrade).
- **Phase 4 — Compliance & scale:** SOC 2/ISO control mapping & evidence, residency verification, DR drills, tiered-tenancy escape hatch design, load/benchmark for sizing.

---

## 20. Open questions

**Resolved (2026-06-29):**
- ✅ **IdP:** Keycloak (self-hosted) — fits on-prem; gives flexible group/claim mapping.
- ✅ **Tenant tiers:** single instance profile for now; tiering deferred (sizing table kept as future reference).
- ✅ **Residency:** single India region for instances and snapshots.
- ✅ **Root-of-trust seal:** Shamir on the one unseal vault now (offline-split, dual control), with PKCS#11/HSM or KMIP as the upgrade path (§10.1).

**Still open for the next session:**
1. **HSM / TPM / KMIP availability:** confirm with infra whether *any* on-prem hardware anchor exists (network HSM, server TPM via PKCS#11, or a KMIP key manager). If yes, we upgrade the root seal to fully-automated and remove the last manual unseal step.
2. **Keycloak group/claim taxonomy:** naming scheme for client→product→role groups (e.g., `acme:payments:admin`) and how realms/clients are structured (one realm shared, or realm-per-client?). Needed before building OIDC roles + policy templating.
3. **Admin secret access policy:** confirm admins get **no** plaintext secret access except via break-glass dual-control — state explicitly for client contracts.
4. **RPO/RTO targets:** snapshot frequency (e.g., hourly?) and whether a second India-region DR copy is in scope at launch.
5. **Keycloak realm topology:** single realm with per-client groups vs realm-per-client — affects token issuer/JWKS config on each client vault's OIDC auth method.

---

## 21. Sources (OpenBao official docs & repos, reviewed 2026-06-29)

**Multi-tenancy / identity / policy**
- Namespaces announcement — https://openbao.org/blog/namespaces-announcement/
- Namespaces concept — https://openbao.org/docs/concepts/namespaces/
- Namespace CLI — https://openbao.org/docs/commands/namespace/ · `/sys/namespaces` API — https://openbao.org/api-docs/system/namespaces/
- Namespace RFC #787 — https://github.com/openbao/openbao/issues/787
- Policies (syntax + templating) — https://openbao.org/docs/concepts/policies/
- Identity (entities/groups/aliases) — https://openbao.org/docs/concepts/identity/
- JWT/OIDC auth — https://openbao.org/docs/auth/jwt/ · Kubernetes auth — https://openbao.org/docs/auth/kubernetes/ · AppRole — https://openbao.org/docs/auth/approle/
- KV v2 — https://openbao.org/docs/secrets/kv/kv-v2/ · Secrets engines — https://openbao.org/docs/secrets/

**Kubernetes / operations**
- K8s overview — https://openbao.org/docs/platform/k8s/ · Helm — https://openbao.org/docs/platform/k8s/helm/ · Helm run — https://openbao.org/docs/platform/k8s/helm/run/
- Helm repo — https://github.com/openbao/openbao-helm · Agent injector — https://github.com/openbao/openbao-k8s · CSI — https://openbao.org/docs/platform/k8s/csi/
- Community operator — https://github.com/dc-tec/openbao-operator
- Raft storage — https://openbao.org/docs/configuration/storage/raft/ · Integrated storage internals — https://openbao.org/docs/internals/integrated-storage/ · Autopilot — https://openbao.org/docs/concepts/integrated-storage/autopilot/
- Seal types — https://openbao.org/docs/configuration/seal/ · Transit seal — https://openbao.org/docs/configuration/seal/transit/
- Telemetry — https://openbao.org/docs/configuration/telemetry/ · Raft metrics — https://openbao.org/docs/internals/telemetry/metrics/raft/ · `/sys/health` — https://openbao.org/api-docs/system/health/
- HA upgrade — https://openbao.org/docs/upgrading/ha-upgrade/

**Security operations**
- Audit devices — https://openbao.org/docs/audit/ (file/syslog/socket subpages) · `sys/audit-hash` — https://openbao.org/api-docs/system/audit-hash/
- Response wrapping — https://openbao.org/docs/concepts/response-wrapping/ · Tokens — https://openbao.org/docs/concepts/tokens/
- operator init — https://openbao.org/docs/commands/operator/init/ · generate-root — https://openbao.org/docs/commands/operator/generate-root/ · Seal concepts — https://openbao.org/docs/concepts/seal/
- Leases — https://openbao.org/docs/concepts/lease/ · Database engine — https://openbao.org/docs/secrets/databases/ · Transit engine — https://openbao.org/docs/secrets/transit/ · operator raft — https://openbao.org/docs/commands/operator/raft/

**Release / version**
- Release notes 2.5.x — https://openbao.org/community/release-notes/2-5-0/ · 2.4.x — https://openbao.org/community/release-notes/2-4-0/ · GitHub releases — https://github.com/openbao/openbao/releases
