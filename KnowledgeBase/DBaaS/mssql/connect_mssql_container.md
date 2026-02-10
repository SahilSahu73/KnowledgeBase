After we pull and run the MSSQL container image, there are 2 ways to connect to it:
1. From outside the container:
We can use sqlcmd, SQL server Management Studio, and MSSQL extension for VS code.


2. Directly connect inside the container using the `docker exec` command.
once the MSSQL docker container has started running (can be done using the commands mentioned in [mssql_container.md](./mssql_container.md))
we need to execute:
> docker exec -it <containerID> bash
This will put us inside the container.
Now to access the database and run the queries we need sqlcmd which is started by:
> /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<Password>"

We might end up with a certificate verification error so we need to use `-C` flag to 
self sign the certificate.
> /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "<Password>" -C
