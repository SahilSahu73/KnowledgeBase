# Xen Project
Xen project creates a Virtual Machine Monitor (VMM) a.k.a. hypervisor.
It is Type-1 or "bare-metal" hypervisor - more details in [Hypervisor](./hypervisors.md)

Guest VMs running on a Xen project Hypervisor - called "Domains".
A special domain - "Domain0" or "Dom0" - responsible for controlling the hypervisor and starting other OSs.
These other guest OSs - called "DomainU" or "DomUs" - This is because these domains are "unpriviledged" in the sense that they cannot control the 
hypervisor or start/stop other domains.

Xen supports paravirtualization (PV) and Hardware Virtualized Machines (HVM) a.k.a. "Full virtualization".
Paravirtualization uses modified guest OS - termed "enlightened" guests. These OSs are aware that they are being virtualized and as such don't
require virtual hardware devices. Instead they make special calls to the hypervisor that allows them to access CPUs, storage, and network resources.

HVM guests - no modification, as hypervisor will create a fully virtual set of hardware devices for the machine resembling a physical x86 comp.
This emulation requires more overhead than the PV mode but allows unmodified guest OSs (like windows) to run on top of the hypervisor.

## Xen Project Architecture
[Xen Architecure](./images/Xen_basic_architecture.png)

We see that the hypervisor sits on the bare metal.
The guest VMs all sit on the hypervisor layer, as does `Dom0`, the *Control Domain*.
The control domain is a VM like the guest VMs, except it has 2 basic functional differences:
1. It has the ability to talk to the hypervisor to instruct it to start and stop guest VMs.
2. It by default contains the device drivers needed to address the hardware.

[Xen architecture with Dom0 details](./images/xen_architecture_Dom0_detail.png)
So now `Dom0` forms the interface to hypervisor.
Through special instructions `Dom0` communicates to the Xen project s/w and changes the configuration of the hypervisor. This includes instantiating
new domain and related tasks.

Another **crucial** part of `Dom0`'s role is as the primary interface to the hardware. The hypervisor does not contain device drivers.
Instead the devices are attached to dom0 and use standard linux drivers. Dom0 then shares these resources with the guest OSs.

To implement paravirtualization, each paravirtualized datapath consists of two parts: 
1) a “backend” that lives in dom0, which provides the virtual device and 
2) a “frontend” driver within the guest domain, which allows the guest OS to access the virtual device. 
The backend and frontend use a high-speed software interface based on shared memory to transfer data between the guest and dom0.

The two important paravirtualized datapaths are: `net-back/net-front`, and `blk-back/blk-front` - which are the paravirtualized networking and
storage systems, respectively. 
There are also paravirtualized interrupts, timers, page-tables and more.

In case of HVM guests, dom0 uses H/W virtualization extensions provided by the CPU. The most basic of these is virtualization of the CPU itself.
Dom0 also emulates some hardware using components of qemu (the Quick emulator).
Emulation in s/w requires the most overhead, -> performance is reduced.


