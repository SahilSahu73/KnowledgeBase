# Replication

- Data Replication works by creating duplicates of your imp. info. and storing them across various servers or locations.
If 1 server fails or encounters a problem, replicated data stored somewhere else steps in, ensuring that the database
continues to function  smoothly without loosing any vital info.

## Types of Data Replication:

1. Master-Slave Replication
2. Multi-Master Replication
  - Allows multiple databases to independently receive and process updates. This means that various copies of the data can be altered
  separately without waiting for instructions from a central database.
3. Peer-to-Peer Replication

Source Database server - Master server
DB receiving the copied data - Replica server

Failover - term used to describe the recovery process
**PostgreSQL itself does not provide built-in tools for detecting server failures**

High Availability refers to DB systems that are set up so that standby servers can take over
quickly when the master or primary fails

To achieve HA, a DB system should meet some key requirements:
- should have redundancy to prevent single point of failure
- reliable switchover mechanisms
- active monitoring to detect any failures that may occur.

## Models of PostgreSQL DB Replication:
1. Single-Master Replication (SMR) - the replicated tables in the replica DB are not permitted
to accept any changes (except from the master).
2. Multi-Master Replication (MMR) - changes to table rows in more than one designated master DB
are replicated to their counterpart tables in every other master DB.
In this model conflict resolution schemas are often employed to avoid problems like 
duplicate primary keys.
MMR adds to the uses of replication:
- write Availability and scalability
- ability to employ Wide Area Network (WAN) of master DBs that can be geographically close to 
groups of clients, yet maintain data consistency across the network.

## Replication modes - Synchronous vs. Asynchronous Replication

Synchronous Replication:
  - Changes made to the master database are instantly mirrored to the slave databases, ensuring they have the most current data.
  - E.g.: Online banking application that processes financial transactions in real time.
  SR ensures that whenever a transactions occurs, it is immediately mirrored/replicated across all databases in different locations.
  This ensures consistency and accuracy, but may introduce some latency due to the wait time for confirmation from multiple databases.

Asynchronous Replication:
  - Changes made to the master databases aren't immediately replicated to the slave DB.
  - Instead, there might be a delay before the updates are copied over, allowing a bit time between changes and replication.
  - E.g.: Social media platform - "Like" Feature

## Types of PostgreSQL DB Replication:
1. Physical
2. Logical

PG supports high availability through streaming replication.
We have a physical (WAL-based) system in which primary (master) server continuously ships WAL records to one 
or more standby servers. default: Asynchronous, primary does not wait for the standy to confirm writes, so a 
**crash can incur data loss**.
To avoid loss - use Synchronous replication: to set this up it requires adding `synchronous_standby_names` in
`postgresql.conf` and typically restarting or reloading.

- Streaming standby requires a base backup of the primary.


Repmgr - In PostgreSQL, to monitor node health and automate the promotion of standby nodes to primary in case of a failure.
