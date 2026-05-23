# Container Networking
For test will use the NGINX image (named `nginx`)
It runs static web server listening on port 80.

## Running an NGINX server
> docker run -d -P nginx

Here `-P` tells docker to publish all ports (publish = make them reachable from other computers)

No when we do `docker ps`
we will see under the ports column 0.0.0.0:12345->80/tcp 
This means:
port 12345 on the docker host is mapped to port 80 in the container.

The address of the Docker Host depends on where the Docker is running.
Basically `localhost` or the IP address of the machine.


## How does docker know which port to map?
- There is metadata in the image telling "this image has something on port 80".
- We can see that metadata with `docker inspect`:
> docker inspect --format '{{.Config.ExposedPorts}}' nginx
output:
map[80/tcp:{}]

This metadata was set in the Dockerfile, with the `EXPOSE` keyword.
> EXPOSE 80/tcp

## Manual allocation of port numbers
> docker run -d -p 80:80 nginx
> docker run -d -p 8000:80 nginx

- The convention is `port-on-host:port-on-container`.

## Finding the container's IP address
We can use the `docker inspect` command
> docker inspect --format '{{ .NetworkSettings.IPAddress}}' <yourContainerID>

We can ping our container from another container.
> docker run alpine ping <ipaddress>

When running on linux, we can even ping that IP address directly.
And connect to a container's ports even if they aren't published.

# Container Network Drivers
- Built-in drivers include:
1. bridge (default)
2. null (for the special network called none)
3. host (for the special network called host)
4. container

Network is selected with `docker run --net ...`
Each network is managed by a driver.

## The default bridge
- By default, the container gets a virtual `eth0` interface.
(In addition to its own private `lo` loopback interface.)
- That interface is provided by a `veth` pair.
- It is connected to the Docker bridge.
(Named `docker0` by default; configurable with `--bridge`)


Basically, a docker container gets a normal Linux network setup built out of ordinary kernel primitives:
- network namespaces
- interfaces
- veth pairs
- bridges
- routing
- NAT via iptables

When we run a container on Docker's default bridge network, it creates a tiny isolated network
environment for that container.
The environment has:
 - its own network interfaces
 - its own IP address
 - its own routing table
 - its own loopback device
 - its own port space

From inside the container, it feels like a small Linux machine
But physically, the container is not a VM with a real NIC. Instead, Docker wires it into the host's network
stack using virtual devices.

- **Container network namespace**:
`eth0 -> veth -> bridge (docker0) -> host network -> internet`

## Networking concepts
- A container uses a network namespace.
- A network namespace is a linux kernel feature that gives a process its own isolated view of networking resources.
  This allows multiple independent network environments to exist in single host.
  Technically virtualizing the network within the same Linux kernel instance.
  The `ip nets` command-line utility from the `iproute2` package is the primary tool for managing network namespaces.

- Inside 1 network namespace, a process sees its own:
    - interfaces, IP addresses, routing table, ARP table, port bindings, firewall rules
- So if 2 containers are in different network namespaces:
    - both can have an `eth0`, can bind to port 80, and can have independent routes.

## By default, the container gets a virtual eth0 interface.
- `eth0` network interface connected to some NIC.
- Inside Docker container, `eth0` is usually a virtual ethernet interface, not a physical card.

When we run the following command inside the container:
> ip addr
The output will be something like:
2: eth0@if123: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 172.17.0.2/16 ...

so the container has:
1. `lo` loopback traffic
2. `eth0` for external traffic.
Move on loopback and eth0 in [linux_networks](../linux/network_namespaces.md)

- **Important Subtlety**
The container's 127.0.0.1 is not the host's 127.0.0.1
So if the app inside the container listens on:
127.0.0.1:5000 or localhost:5000
then only processes inside that same container can reach it.

The host cannot reach it through the bridge, because binding to `127.0.0.1` means "only accept local namespace traffic".
To make a service reachable from outside the container, the app usually must bind to:
0.0.0.0
which means "listen on all interfaces", including `eth0`

## veth pair
A veth pair means virtual Ethernet pair.
It is like a virtual cable with 2 ends, wherein one endpoint is placed inside the container namespace, and
the other remains on the host namespace.

So Docker does basically this:
- create a veth pair
- move one end into the container's network namespace
- rename that end to eth0
- keep the other end on the host
- attach the host-side end to the bridge `docker0`.

So a virtual wire is created b/w the container and the host-side bridge.

## It is connected to the Docker Bridge (named docker0 by default)
- A linux bridge is like a virtual layer 2 switch.
- A real ethernet switch forwards frames between ports based on MAC addresses.
- A linux bridge does basically the same thing in software.

Docker creates a bridge interface, usually called:
docker0
This bridge acts like a virtual switch for containers on the default bridge network.

Every container connected to that default bridge has:
- one veth endpoint inside the container
- the peer endpoint plugged into `docker0`.

So visually:
container A eth0 -- veth --+
                           |
container B eth0 -- veth --+--> docker0 bridge
                           |
container C eth0 -- veth --+

This means containers on the same bridge can talk to each other at Layer2/Layer3 using their bridge-subnet IPs.
The bridge itself also has an IP address, usually something like:
172.17.0.1/10
That IP often acts as the container's default gateway.

More details in this chatgot session:
[chatgpt chat session](https://chatgpt.com/share/69b2a6b8-5d78-8011-a89e-8e7bb6e2df6c)
