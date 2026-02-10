# DBaaS - Database as a Service

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  DBaaS Platform                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Client Interfaces Layer                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐              │
│  │   CLI Interface  │    │  REST API        │    │  Swagger UI      │              │
│  │   (main.py)      │    │  (FastAPI)       │    │  /docs           │              │
│  │                  │    │  Port: 8000      │    │  /redoc          │              │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘              │
│           │                       │                       │                         │
│           └───────────────────────┴───────────────────────┘                         │
│                                   │                                                  │
└───────────────────────────────────┼──────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              API Router Layer                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐              │
│  │  Instance Routes │    │ Database Routes  │    │ Monitoring Routes│              │
│  │  /instances/     │    │ /database/       │    │ /monitoring/     │              │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘              │
│           │                       │                       │                         │
└───────────┼───────────────────────┼───────────────────────┼──────────────────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Business Logic Layer                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐           │
│  │                        DBaaS Manager                                  │           │
│  │                   (Orchestrates All Operations)                       │           │
│  └──────────────────────────────────────────────────────────────────────┘           │
│           │                       │                       │                          │
│           ▼                       ▼                       ▼                          │
│  ┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐                 │
│  │ DB Provisioner  │   │ Database Service │   │  Agent Manager   │                 │
│  │ - Create dirs   │   │ - CRUD ops       │   │ - Deploy agents  │                 │
│  │ - Gen configs   │   │ - SQL execution  │   │ - Check status   │                 │
│  │ - Copy scripts  │   │ - Transactions   │   │ - Get logs       │                 │
│  └────────┬────────┘   └────────┬─────────┘   └────────┬─────────┘                 │
│           │                     │                      │                            │
│  ┌────────┴────────┐   ┌────────┴─────────┐   ┌────────┴─────────┐                 │
│  │ Docker Manager  │   │ Config Manager   │   │   Validator      │                 │
│  │ - Containers    │   │ - instances.json │   │ - Input checks   │                 │
│  │ - Lifecycle     │   │ - Persistence    │   │ - Validation     │                 │
│  └─────────────────┘   └──────────────────┘   └──────────────────┘                 │
│                                                                                       │
└───────────────────────────────────┬───────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          Infrastructure Layer                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│                            Docker Engine                                             │
│                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────┐         │
│  │                         Container Network (Bridge)                      │         │
│  │                                                                          │         │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────┐   │         │
│  │  │  Instance: db_xxx1  │  │  Instance: db_xxx2  │  │ Instance: db │   │         │
│  │  │  Port: 5432→5432    │  │  Port: 5433→5432    │  │ Port: 5434   │   │         │
│  │  ├─────────────────────┤  ├─────────────────────┤  ├──────────────┤   │         │
│  │  │                     │  │                     │  │              │   │         │
│  │  │  ┌──────────────┐  │  │  ┌──────────────┐  │  │  ┌────────┐  │   │         │
│  │  │  │ PostgreSQL   │  │  │  │ PostgreSQL   │  │  │  │ PG 15  │  │   │         │
│  │  │  │ Version 15   │  │  │  │ Version 14   │  │  │  │        │  │   │         │
│  │  │  │              │  │  │  │              │  │  │  │        │  │   │         │
│  │  │  │ Port: 5432   │  │  │  │ Port: 5432   │  │  │  │        │  │   │         │
│  │  │  └──────────────┘  │  │  └──────────────┘  │  │  └────────┘  │   │         │
│  │  │                     │  │                     │  │              │   │         │
│  │  │  ┌──────────────┐  │  │  ┌──────────────┐  │  │  ┌────────┐  │   │         │
│  │  │  │ Monitoring   │  │  │  │ Monitoring   │  │  │  │Monitor │  │   │         │
│  │  │  │ Agent        │  │  │  │ Agent        │  │  │  │Agent   │  │   │         │
│  │  │  │ (Python)     │  │  │  │ (Python)     │  │  │  │        │  │   │         │
│  │  │  └──────────────┘  │  │  └──────────────┘  │  │  └────────┘  │   │         │
│  │  │                     │  │                     │  │              │   │         │
│  │  │  Resource Limits:   │  │  Resource Limits:   │  │  Limits:     │   │         │
│  │  │  - Memory: 1GB      │  │  - Memory: 512MB    │  │  - Mem: 2GB  │   │         │
│  │  │  - CPU: 2.0         │  │  - CPU: 1.0         │  │  - CPU: 1.5  │   │         │
│  │  └─────────────────────┘  └─────────────────────┘  └──────────────┘   │         │
│  │           │                         │                      │            │         │
│  └───────────┼─────────────────────────┼──────────────────────┼────────────┘         │
│              │                         │                      │                      │
│              ▼                         ▼                      ▼                      │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────────┐            │
│  │  Volume Mounts      │  │  Volume Mounts      │  │  Volume Mounts   │            │
│  └─────────────────────┘  └─────────────────────┘  └──────────────────┘            │
│                                                                                       │
└───────────────────────────────┬───────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            Storage Layer (Host OS)                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  instances/                                                                          │
│  │                                                                                    │
│  ├── db_xxx1/                                                                        │
│  │   ├── data/              ← PostgreSQL data files (persistent)                    │
│  │   ├── logs/              ← PostgreSQL & agent logs                               │
│  │   │   └── metrics.json   ← Time-series metrics (newline-delimited JSON)          │
│  │   ├── scripts/           ← Initialization SQL scripts                            │
│  │   │   ├── 01-init-users.sql                                                      │
│  │   │   └── 02-monitoring-setup.sql                                                │
│  │   └── docker-compose.yml ← Instance-specific configuration                       │
│  │                                                                                    │
│  ├── db_xxx2/                                                                        │
│  │   ├── data/                                                                       │
│  │   ├── logs/                                                                       │
│  │   │   └── metrics.json                                                            │
│  │   ├── scripts/                                                                    │
│  │   └── docker-compose.yml                                                          │
│  │                                                                                    │
│  └── db_xxx3/                                                                        │
│      └── ... (same structure)                                                        │
│                                                                                       │
│  config/                                                                             │
│  └── instances.json          ← Central instance registry & metadata                 │
│                                                                                       │
│  templates/                                                                          │
│  ├── docker-compose.yml.j2   ← Jinja2 template for Docker Compose                  │
│  └── init-scripts/           ← Reusable SQL templates                               │
│      ├── 01-init-users.sql                                                           │
│      └── 02-monitoring-setup.sql                                                     │
│                                                                                       │
│  monitoring/                                                                         │
│  └── postgres_agent.py       ← Single agent script (copied to all containers)       │
│                                                                                       │
│  logs/                                                                               │
│  └── provisioning.log        ← Platform-level logs                                  │
│                                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Data Flow Diagrams                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│  1. Instance Creation Flow                                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  Client Request                                                                    │
│       │                                                                            │
│       ├─► Validator ────► Config Manager ────► DB Provisioner                     │
│                                 │                    │                             │
│                                 │                    ├─► Create directories        │
│                                 │                    ├─► Generate docker-compose   │
│                                 │                    └─► Copy init scripts         │
│                                 │                                                  │
│                                 ├─► Docker Manager                                 │
│                                 │        │                                         │
│                                 │        ├─► Create container                      │
│                                 │        ├─► Start container                       │
│                                 │        └─► Health check                          │
│                                 │                                                  │
│                                 └─► Agent Manager                                  │
│                                          │                                         │
│                                          ├─► Copy agent to container               │
│                                          └─► Start monitoring                      │
│                                                                                    │
│                                    Connection String ◄── Client                    │
│                                                                                    │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│  2. Monitoring Flow                                                               │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  Container (db_xxx)                                                               │
│       │                                                                            │
│       ├─► Monitoring Agent (Python)                                               │
│       │        │                                                                   │
│       │        ├─► Connect to PostgreSQL (localhost:5432)                         │
│       │        │                                                                   │
│       │        ├─► Query pg_stat_database                                         │
│       │        ├─► Query pg_stat_activity                                         │
│       │        ├─► Query pg_locks                                                 │
│       │        ├─► Query information_schema                                       │
│       │        │                                                                   │
│       │        ├─► Aggregate metrics                                              │
│       │        │                                                                   │
│       │        └─► Write to /var/log/postgresql/metrics.json                      │
│       │                     │                                                      │
│       │                     ▼                                                      │
│       └────────────► Host Volume Mount                                            │
│                              │                                                      │
│                              ▼                                                      │
│                      instances/db_xxx/logs/metrics.json                           │
│                              │                                                      │
│                              ▼                                                      │
│                      API: GET /monitoring/{id}/metrics                            │
│                              │                                                      │
│                              ▼                                                      │
│                          Client receives metrics                                   │
│                                                                                    │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│  3. Database CRUD Flow                                                            │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  Client ──► API /database/{id}/tables/{name}/rows                                │
│                    │                                                               │
│                    ▼                                                               │
│            Database Service                                                        │
│                    │                                                               │
│                    ├─► Get instance config from Config Manager                    │
│                    │                                                               │
│                    ├─► Create psycopg2 connection                                 │
│                    │    (host=localhost, port=5432-655XX)                         │
│                    │                                                               │
│                    ├─► Build parameterized SQL                                    │
│                    │                                                               │
│                    ├─► Execute query on PostgreSQL container                      │
│                    │                                                               │
│                    ├─► Fetch results (RealDictCursor)                             │
│                    │                                                               │
│                    └─► Return JSON response                                       │
│                                                                                    │
└──────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           Component Details                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────┐
│  Technology Stack                                                                  │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  • Language: Python 3.9+                                                           │
│  • API Framework: FastAPI + Uvicorn (ASGI)                                        │
│  • Template Engine: Jinja2                                                         │
│  • Validation: Pydantic                                                            │
│  • Database: PostgreSQL 12-16                                                      │
│  • Database Driver: psycopg2                                                       │
│  • Containerization: Docker + Docker Compose                                       │
│  • Docker SDK: docker-py                                                           │
│  • Config Format: JSON                                                             │
│  • Logging: Python logging module                                                  │
│                                                                                     │
└───────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────┐
│  Network Architecture                                                              │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Host OS (Rocky Linux 9.3)                                                        │
│  ├─ API Server: 0.0.0.0:8000 (FastAPI)                                           │
│  │                                                                                 │
│  ├─ Docker Bridge Network                                                         │
│  │  ├─ db_xxx1: 172.17.0.2 → exposed on host:5432                               │
│  │  ├─ db_xxx2: 172.17.0.3 → exposed on host:5433                               │
│  │  └─ db_xxx3: 172.17.0.4 → exposed on host:5434                               │
│  │                                                                                 │
│  └─ Volume Mounts: Bind mounts to ./instances/*                                   │
│                                                                                     │
│  Clients can connect to:                                                          │
│  • API: http://<host>:8000                                                        │
│  • Database Direct: postgresql://user:pass@<host>:543X/dbname                     │
│                                                                                     │
└───────────────────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────────────────┐
│  Security Considerations                                                           │
├───────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  • Container Isolation: Each instance in separate container                        │
│  • Network Isolation: Bridge network mode                                          │
│  • Volume Isolation: Separate directories per instance                             │
│  • Credential Storage: JSON file (TODO: encryption/vault)                          │
│  • SQL Injection Prevention: Parameterized queries                                 │
│  • Resource Limits: Docker CPU/memory constraints                                  │
│  • Port Exposure: Configurable per instance                                        │
│                                                                                     │
└───────────────────────────────────────────────────────────────────────────────────┘
