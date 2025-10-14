# Hypervisors - Wiki
A Hypervisor - a.k.a. Virtual Machine Monitor (VMM) or Virtualizer, is a type of computer software, firmware, or hardware that creates and
runs virtual machines.



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
