# Virtualization
Technology that can be used to create virtual representations of servers, storage, networks and other physical machines. 
With virtualization, we can interact with any hardware resource with greater flexibility.
It abstracts physical hardware functionality into software, which in turn helps to manage, maintain, and use hardware as a web application.

SUSE Linux Enterprise is an enterprise-class Linux server operating system that offers 2 types of hypervisors: Xen and KVM.
Both hypervisors support virtualization on the AMD64/Intel 64 architecture.
Both Xen and KVM support full virtualization mode.
Additionally, Xen supports paravirtualized mode, and you can run both paravirtualized and fully virtualized guests on the same host.
Xen or KVM acts as a **virtualization host server (VHS)** that supports VM guests with its own guest operating systems. The SUSE VM Guest 
architecture consists of a hypervisor and management components that constitute the VHS, which runs many application-hosting VM guests.

In Xen, the management components run in a priviledged VM Guest often called `Dom0`.
In KVM, where the linux kernel acts as the hypervisor, the management components run directly on the VHS.

Virtualization Capabilities:
1. server consolidation: many servers - replaced by one big physical server - so hardware is consolidated, and guest OS are converted to VM.
    provides ability to run legacy software on new hardware.
2. Isolation: guest OS fully isolated from the host running it. If VM corrupted, the host system is not harmed.
3. Migration: move a running VM to another physical machine, without disconnection of the client or the application.
4. Disaster Recovery: Virtualized guests are less dependent on the hardware, and host server provides snapshot features to be able to restore
    a known running system without any corruption.
5. Dynamic Load Balancing


The different modes of virtualizaton is for the question - "How much does the guest OS know about the fact that it is virtualized?"
## Virtualization Modes
Guest OS are hosted on VMs in either full virtualization (FV) or paravirtual (PV) mode.
1. Full virtualization mode:
In this mode the guest OS does not know it's running inside a VM.
Hypervisor completely emulates the hardware - CPU, memory, disk, NICs, etc.
The guest thinks it's running on real physical hardware.
No modification to the guest OS is needed.
e.g. - VMware ESXi or KVM with hardware virtualization (Intel VT-x or AMD-V).
These hypervisors trap and emulate priviledged instructions so that even unmodified OSs can run safely.

advantage:
can run any OS (no modification needed).
strong isolation between VMs.

disadvantage:
slightly higher overhead, because the hypervisor must emulate hardware and intercept priviledged operations.

side note: It can use either Binary translation or hardware-assisted virtualization tech.
Using hardware-assistance allows for better performance on processors that support it.

2. Paravirtualized mode:
Here the guest OS knows it's being virtualized and cooperates with the hypervisor.
The guest OS is modified to replace certain hardware instructions with hypercalls (direct calls to the hypervisor).
This avoids the need for full hardware emulation, improving efficiency.

advantage:
better performance (fewer traps/emulations)
simpler hypervisor design

disadvantage:
guest OS must be modified (so only opensource OSs like linux or BSD can be used easily).


## Types of Virtualization
4 types of virtualization:
1. **Operating System (OS) Virtualization**:
Client virtualization refers to virtualization on a desktop or laptop computer.
OS virtualization means the movement of the main desktop OS in a virtual environment. In this method, the OS is hosted on a server, i.e. one version
on the server and copy of that is present on each user. The user can modify his/her own OS without impacting other users.

2. **Server Virtualization**:
Means moving a physical server into a virtual environment.
Servers can run more than one server simultaneously helping to reduce the number of servers. 
With this they can add more machines

3. **Storage Virtualization**:
Means combining multiple physical HDDs or SSDs into a single virtualized storage. = Cloud computing
It can help administrators easily with backup, archiving, and recovery.
In cloud storage, data is stored in logical pools and physical storage and physical environments owned by provider. 

4. **Hardware Virtualization**:
Means taking the components of a real machine and making it virtual -> Platform virtualization, which refers to creating a VM that behaves like a 
real computer with an OS.


## Difference between Containers and Virtualization
1. The core idea:
Virtualization splits the hardware into several virtual computers, so that we can run multiple OSes on one machine.
Containers split the OS into several isolated user spaces, so that we can run multiple isolated apps on one OS.

2. In terms of architecture:
Each VM runs its own kernel and system libraries, on top of the virtuaized hardware (CPU, disk, NIC, etc.) -> hence heavier, as we are running
multiple full operating systems.

Each container shares the same kernel as the host, but uses namespaces and cgroups to isolate resources(process IDs, filesystems, networks, memory
etc.).
Hardware
│
├── Host OS (Linux)
│
├── Container Runtime (e.g., Docker, containerd, CRI-O)
│
└── Containers
      ├── App binaries + dependencies
      └── Share host kernel

3. Resource Allocation:
In virtualization CPU & memory are allocated per VM by the hypervisor (through hardware emulation + scheduling)
In containers it is limited using cgroups (resource control in kernel)

For storage each VM has a virtual disk (e.g. .vmdk, .qcow2)
Containers use layered file systems (e.g. overlayfs)

For Network each VM gets a virtual NIC via the hypervisor
Containers use virtual network namespaces (veth pairs, bridges)

4. Performance and Overhead:
VMs: High isolation but more overhead - every VM runs its own OS and kernel.
Containers: Lightweight and use less memory, since they share the host kernel.


# Hypervisors
A Hypervisor - a.k.a. Virtual Machine Monitor (VMM) or Virtualizer, is a type of computer software, firmware, or hardware that creates and
runs virtual machines.
Every virtual machine has its own operating system and applications. The hypervisor allocates the underlying physical computing resources such
as CPU and memory to individual virtual machines as required. Thus, it supports the optimal use of physical IT infrastructure.
Hypervisor loads the VM images to create multiple virtual OS.
Physical machine = host
virtual operating systems = guests

## Types of Hypervisors:
1. Type 1 Hypervisor:
a.k.a bare metal hypervisor, interacts directly with the underlying machine hardware.
It negotiates directly with server hardware to allocate dedicated resources to VMs. It can also flexibly share resources, depending on
various VM requests.

2. Type 2 Hypervisor:
a.k.a. hosted hypervisor, interacts with the underlying host machine hardware through the host machine's OS.
we can install it on the machine, where it runs as an application.
It negotiates with the OS to obtain underlying system resources. However, the host OS prioritizes its own functions and applications over the 
virtual workload.


# Appendix
**Firmware** - a software that provides low-level control of computing device hardware.
For a relatively simple device, firmware may perform all control, monitoring, and data manipulation functionality.
For a complex device, firmware may provide relatively low-level control as well as hardware abstraction services to higher-level software such
as an operating system.
Firmware is stored in a non-volatile memory - either ROM or programmable memory such as EPROM, EEPROM, or flash.

hardware - inside it we have firmware -> drivers -> OS

**Drivers** - Computer program that operates or controls a particular type of device that is attached to a computer.
It provides s/w interface to hardware devices, enabling OS and other computer programs to access hardware funtionalities without needing to
know precise details about the hardware.

**Virtual Machines** - VM is the virtualization or emulation of a computer system. They are based on computer architectures and provide the
fucntionality of a physical computer. 
VMs differ and are organized by their functions:
- System virtual machines: provide a substitute for a real machine. provides functionality needed to execute entire OS. A hypervisor uses
native execution (machine code) to share and manage hardware, allowing for multiple environments that are isolated from one another yet exist
on the same physical machine. Modern hypervisors use hardware-assisted virtualization, with virtualization-specific hardware features on the 
host CPUs providing assistance to hypervisors.
- process virtual machines: are designed to execute computer programs in a platform-independent environment.

Multiple environments - repetitive task
Pulumi
terraform
opentofu

172.16.22.78/login
