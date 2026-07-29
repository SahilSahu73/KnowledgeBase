# Vault
Essentially a secret management Tool.

What are Secrets?
Information we use to login or authorize with various services.
like user name and password for login or API token.

There are 2 types of users who need to use these secrets to access those services:
Humans and System User.





questions:
etcd and vault relation
Do we need to connect/store kv pairs of etcd in vault ?

Master node - primary vault
cert manager - do we need vault for this.


The entire nuance of namespaces is I think to have isolation and multi-tenancy when we just have one of that. For example the network namespaces controls the same Wlan and eth0 connection but gives the users/services an
interface to think of it as an individual component dedicated to them and that service can control it, but in reality
internally there is just one. Basically virtualization.


