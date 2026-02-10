# Enterprise DBaaS Platform

A comprehensive cloud-native Database-as-a-Service platform built with Go and Kubernetes, providing automated database provisioning, management, and operations capabilities.

## Architecture

The platform follows a microservices architecture with the following core services:

- **API Gateway**: Entry point for all external API requests with authentication and rate limiting
- **Provisioning Service**: Database instance creation, deletion, and lifecycle management
- **Backup Service**: Automated backup scheduling and point-in-time recovery
- **Monitoring Service**: Real-time metrics collection and alerting
- **Access Control Service**: User authentication, authorization, and RBAC
- **High Availability Controller**: Database clustering and automatic failover
- **Disaster Recovery Service**: Cross-region replication and recovery
- **Scaling Service**: Horizontal and vertical database scaling
- **Cost Management Service**: Resource usage tracking and optimization

## Supported Database Engines

- PostgreSQL
- MySQL

## Quick Start

### Prerequisites

- Go 1.21+
- Docker
- Kubernetes cluster
- kubectl configured

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/enterprise-dbaas-platform
cd enterprise-dbaas-platform
```

2. Install dependencies:
```bash
go mod download
```

3. Run tests:
```bash
make test
```

4. Build all services:
```bash
make build
```

5. Deploy to Kubernetes:
```bash
make deploy
```

## Project Structure

```
├── cmd/                    # Service entry points
│   ├── api-gateway/
│   ├── provisioning/
│   ├── backup/
│   ├── monitoring/
│   ├── access-control/
│   ├── ha-controller/
│   ├── disaster-recovery/
│   ├── scaling/
│   └── cost-management/
├── internal/               # Internal packages
│   ├── api/               # API definitions and handlers
│   ├── domain/            # Domain models and interfaces
│   ├── infrastructure/    # External integrations
│   └── shared/            # Shared utilities
├── pkg/                   # Public packages
├── deployments/           # Kubernetes manifests
├── docker/               # Dockerfiles
├── scripts/              # Build and deployment scripts
└── tests/                # Integration and e2e tests
```

## Development

### Running Services Locally

Each service can be run independently for development:

```bash
# API Gateway
go run cmd/api-gateway/main.go

# Provisioning Service
go run cmd/provisioning/main.go

# Other services...
```

### Testing

The project uses both unit tests and property-based tests:

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run property-based tests only
make test-property
```

### Building Docker Images

```bash
# Build all service images
make docker-build

# Build specific service
make docker-build-api-gateway
```

## Configuration

Services are configured via environment variables and configuration files. See `configs/` directory for examples.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

Enterprise License - See LICENSE file for details.