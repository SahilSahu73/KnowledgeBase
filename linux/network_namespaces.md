A network namespace is a linux kernel feature that gives a process its own isolated view of networking resources.
This allows multiple independent network environments to exist in single host.
Technically virtualizing the network within the same Linux kernel instance.
The `ip nets` command-line utility from the `iproute2` package is the primary tool for managing network namespaces.

Container technologies use this feature to create isolated network stack in the OS.
We can run applications in different network stacks.

**VETH** devices are virtual ethernet devices.
They act as tunnels between network namespaces to create a bridge to a physical network device in another namespace,
but can also be used as a standalone network device.

Reasons as to why we might want to manage the network stack:
- Configure a point-to-point net namespace demonstrating that one namespace can talk to a python webserver in another namespace.
- Configure DHCP inside a namespace to show that namespaces can isolate broadcast traffic, even from the host.
- Combine the net namespace and Open vSwitch to isolate 2 or more processes that use the network to communicate without
  permitting the outside (or even the host) to access those processes.

# A practical session
Objective:
- create 2 network namespaces and establish a connection b/w them
- Add a bridge network device and communicate 2/multiple network namespaces via bridge
- Namespaces to root/default namespace communication via bridge.
- Make a communication with outside world via bridge.

## Create network namespace
> sudo ip netns add earth
> sudo ip netns add neptune

Now we have 2 different namespaces, and its like 2 different computer. To check the list:
> sudo ip netns list

Now we add a virtual ethernet peer between these 2 namespaces
> sudo ip link add earth-veth type veth peer name neptune-veth
This has basically created an open ended link b/w 2 network namespaces, but has not been linked to any namespace yet.

We now assign them, so assign earth-veth to earth and another end i.e. neptune-veth to neptune.
> sudo ip link set earth-veth netns earth
> sudo ip link set neptune-veth netns neptune

To look at the earth network namespace:
> sudo ip netns exec earth ip addr
similarly:
> sudo ip netns exec neptune ip addr
Note:
If we want to run a command inside a network namespaces, we can execute our command like this:
> ip netns exec <command> or ip -n command

We can see that the `earth` namespace has 2 ethernet devices, `lo` and `earth-veth`.
Similarly `neptune`
`lo` is a loopback device (more details in [loopback_interface](./loopback_interface.md))
Initially when we check the state of the network namespaces, they are in `DOWN` state.

We will `UP` those now:
> sudo ip netns exec earth ip link set dev earth-veth up
> sudo ip netns exec earth ip link set dev lo up

