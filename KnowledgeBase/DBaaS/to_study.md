ETCD
Consul Hashicorp
Zookeeper
They all are for metadata of provisioning


**Architecture of Amazon dynamo DB**
Amazon aurora
KMS vault
CORS
GO svc

Async sync and semi sync replication (WAL)
Quorum (pgWAL)
Promote replica (replication time - pg_promote)
HA proxy or Envoy
PG bouncer or Amazon RDS proxy

B-Trees
gRPC

Debezium (Red Hat - take inspiration) confluent cloud

EBS snapshots + WAL logs => backups
Kubernetes operator -> Crunchy data

Rate limiting in APIs
How SDK's are created and works


### HA (High-Availability)
1. Failover
2. Leader election
3. Multinode Clusters

For all of this work we will need
Paxos
Raft => AWS aurora uses this for metadata
(Anyone of them for master-slave)

### Replication
Distributed WAL shipping
Async and Sync replications
Concensus for failover


### Multitenant
Isolated pods
Isolated networks
Connection pools
Different engines

For this kubernetes is required


### Automatic provisioning
Scheduler for shared resources
storage controller
compute allocator
VM pools
Metadata store => ETCD, Consul Hashicorp, Zookeeper
secret manager - KMS vault


### Backup and storage
1. S3 buckets
2. MinIO 
3. Agent monitoring - health checks (of replicas as well)


### Security

