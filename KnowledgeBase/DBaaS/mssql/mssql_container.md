1. We pull the latest docker image of MSSQL using this command:
> docker pull mcr.microsoft.com/mssql/server:2025-latest

2. This will pull and download the official image.
3. After that we run the container and do some basic user and env config
> docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=<password>" \
   -p 1433:1433 --name sql1 --hostname sql1 \
   -d \
   mcr.microsoft.com/mssql/server:2025-latest

Note: the system administrator (sa) account is a system administrator on the SQL server 
instance that gets created during setup. 
As a best practice it is recommended to disable the `sa` account, because after we create 
the SQL server container, the `MSSQL_SA_PASSWORD` environment variable we specified in the 
above command is discoverable by running `echo $MSSQL_SA_PASSWORD` in the container.
For security purposes, we should change our `sa` password in a production environment. 
But disabling the sa account is a better approach and create a new login, and make it 
a member of the sysadmin server role.

There is a tutorial available as to how to configure active directory authentication
with SQL server on linux containers. [link](https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-containers-ad-auth-adutil-tutorial?view=sql-server-ver17)
The above one is to enable windows authentication, and create a new windows-based login and 
add it to the sysadmin server role.

The alternative is to create a login using SQL server authentication, and add it to the 
sysadmin server role.
Need to go through a lot of links to find how to do it, here are some starter links:
[create a login](https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-login?view=sql-server-ver17)
In the documentation, there is a security section in which there are alot of How-to's which
will teach us how to set all that up.
For now skipping it.

## Run multiple SQL server containers
Can run multiple SQL server containers on the same host machine.
Each container much expose itself on a different port.
Example:
> docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=<password>' -p 1401:1433 -d mcr.microsoft.com/mssql/server:2025-latest
> docker run -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=<password>' -p 1402:1433 -d mcr.microsoft.com/mssql/server:2025-latest
This creates 2 containers from the MSSQL server image and maps them to ports 1401 and 1402 on the host machine.

Clients can connect to each SQL Server instance by using the IP address of the container host
and the port number for the container.
> sqlcmd -S 10.3.2.4,1401 -U sa -P '<YourPassword>'
> sqlcmd -S 10.3.2.4,1402 -U sa -P '<YourPassword>'

