- Provides a framework to run distributed systems resiliently.
- Takes care of scaling and failover of applications.

## It provides us with:
- **Service discovery and load balancing** - expose container using DNS or own IP. If traffic to container is high, it load balances and distribute the network traffic - deployment stable.

- **Storage Orchestration** - mount storage system of your choice
- **Automated rollouts and rollbacks** - can declare **desired state** of deployed containers - then change actual state to desired state at a controlled rate.
  Example: create new containers for deployment, remove existing containers and adopt all their resources to the new container.
- **Automated bin packing** - tell how much CPU and memory each container needs, it can fit containers onto the nodes making best use of available resources.
- **Self-healing** - restarts containers that fail, replaces containers, kills containers that don't respond to user-defined healthchecks, and doesn't advertise them to clients until ready.
- **Secret and configuration management**
- **Batch execution**
- **Horizontal Scaling**
- IPv4/IPv6 dual-stack

Some more details of what kubernetes is not and its historical context can be found here in the documentation.
[kubernetes overview](https://kubernetes.io/docs/concepts/overview/)
