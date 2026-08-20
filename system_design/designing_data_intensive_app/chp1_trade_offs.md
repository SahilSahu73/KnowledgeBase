# Trade-Offs in Data Systems Architecture
*Data Intensive* application: if data management is the primary challenge in development.
worry more about things like storing and processing large data volumes, managing changes to data, ensuring consistency in face of failures
and concurrency, and making sure services are highly available.
*Compute Intensive* application: primary challenge in parallelizing very large computation.

## Operational versus Analytical Systems
Different types of people in an enterprise will use the same data in different ways and for different usecases.
Two types of systems:
- *Operational systems* consists of the backend services and data infra where data is created, example by serving external users.
Here, the application code both reads and modifies the data in its databases, based on the actions performed by the users.
- *Analytical systems* for business analytics and data scientists needs. They contain a read-only copy of data from the operational
systems, and they are optimized for the types of data processing needed for analytics.

## Characterizing Transaction Processing and Analytics
Early days of business data processing - write to a DB typically corresponds to a commercial transaction taking place:
making sale, placing an order with a supplier, paying an employee's salary, etc. As DB expanded into areas that didn't invole money
changing hands, the term *transaction* nevertheless stuck, referring to a **group of reads and writes that form a logical unit**.

Term **Transaction** here loosely refers to low-latency reads and writes.

DB is used for many kinds of data, in different fields but the basic access pattern remained similar to processing business transactions.
An operational system typically looks up a small number of records by a key (called a *point query*).
Records are inserted, updated, or deleted based on the user's input.
Because these applications are interactive, this access pattern became known as *online transaction processing (OLTP)*.

Since DB's are also used for analytical works, they have very different access patterns compared to OLTP.
Usually analytical queries scan over a huge number of records and calculates aggregate statistics (such as count, sum, or average)
rather than returning individual records.
This pattern of using DB is called *online analytical processing (OLAP)*.

Operational systems - users generally not allowed to construct custom SQL query and run on DB - because potentially will have to allow
read or modify data to which they do not have permission to access.
Can also write queries expensive to execute - affect DB performance for other users.
Therefore, OLTP systems mostly run fixed set of queries that are baked into the application code.

Analytical systems - give users freedom to write arbitrary SQL queries by hand, or generate queries automatically.
PowerBI, Tableau, Looker etc.
Another type of system designed for analytical workloads but embedded into user-facing products - aka *product analytics* or
*real-time analytics* - includes Pinot, ClickHouse, and Druid.
These systems ingests data in real time and are optimized for low-latency query responses.
In contrast, OLTP systems ingests data in batches and are optimized for high-throughput query processing.

## Data Warehousing

