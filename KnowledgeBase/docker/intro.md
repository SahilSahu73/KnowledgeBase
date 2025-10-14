# What is Docker ?
- The Docker engine is a daemon (a service running in the background).
- This daemon manages containers, the same way that a hypervisor manages VMs.
- Interact with docker engine by using docker CLI.
- Docker CLI and Docker engine communicate through an API.

# Why use Docker: Key Benefits
Because of the simplicity and improvements it brings to the app development lifecycle.
1. *Cost-saving*: Docker containers use far less memory, compared to VMs. Thus spend less on IT infra resources.
2. *Flexible resource sharing*: Containerized apps are all running on the same OS even though your application and its dependencies are
isolated from the underlying OS and other containers by docker containers.
3. *Multi-cloud platforms*: all cloud service providers support running docker and switching between environments is simple.
4. *Configuration and consistent delivery of your application*: offers faster, more resource efficient, and standardized way to deploy, ship
and run applications. Apps can be distributed on various platforms without worrying about framework, library, and compatibility issues.
5. *Pipelines*': allows you to standardize the development and release cycle. This acts as a form of legacy change management for apps and 
encourages CICD


Note: If we have access to Docker control socket, you can take over the machine (Because you can run containers that will access the machine's
resources). Therefore, on linux machines, the docker user is equivalent to root.
You should restrict access to it like you would protect root.
By default, docker control socket belongs to the docker group. You can add trusted users to the docker group, otherwise you will have to
prefix every docker command with sudo.

# First containers

> sudo docker run busybox echo Hello World

a more useful container - ubuntu
> sudo docker run -it ubuntu
- Brand new container, runs a bare-bones, no frills ubuntu system.
- `-it` is shorthand for `-i -t`
`-i` tells docker to connect us to the container's stdin.
`-t` tells docker that we want a sudo terminal.


