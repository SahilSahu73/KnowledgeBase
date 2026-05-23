The process of starting a linux system:
Power ON -> BIOS -> Master Boot Record (MBR) or EFI Partition -> Boot Loader -> Kernel -> initial RAM Disk (initramfs) -> /sbin /init (parent 
process) -> command shell using getty -> GUI (Wayland oe X windows)

- When Powered ON, the BIOS (Basic Input/Output System) is initialized.
It initializes the hardware including the screen and keyboard and tests the main memory.
This process is called POST (Power On Self Test). BIOS is stored in ROM.


- After POST, system control is passed from BIOS to Boot loader.
Boot loader is stored on system's hard disk or SSD drive, either in Boot sector (for traditional BIOS/MBR systems) or the EFI partition (for 
more (unified) Extensible Firmware Interface or EFI/UEFI systems). 
Upto this stage, the machine does not access any mass media storage. The info. on date, time, and the most imp. peripherals are loaded from
the CMOS values.
CMOS is used to store imp. system settings & configurations such as the date and time, boot order, hardware settings, and password info.
This info. is stored in a small battery powered chip on the motherboard called the CMOS battery, which enables the system to keep track of
the date and time even when it is powered off.
So as the control from BIOS to the boot loader is passed, the values from the CMOS are also loaded.
When booting linux, the boot loader is reponsible for loading the kernel image and the initial RAM disk or file system (which contains some 
critical files and device drivers needed to start the system) into the memory.

Boot loader has 2 distinct stages:
1. Systems using BIOS/MBR method, the boot loader resides in the 1st sector of the hard disk a.k.a. the Master Boot Record (MBR).
MBR Size => 512 Bytes
By 1st sector it means the very first 512 bytes of the storage.

Note: The 1st sector is crucial => it contains the initial part of the boot loader code and the partition table.
When the system powers on, the BIOS firmware looks for this specific location to load the boot loader and start the boot process.
Partition table - small Data structure in the MBR that records info. about the disks partitions. 
Partitions divide a hard disk into sections that the OS can manage separately. Each entry in the partition table describes a partition,
including its start and end points, size, type (like primary, extended or logical), and whether it is marked as "bootable"(active).
This helps the boot loader to identify where the bootable partition resides so it knows where to find the 2nd stage boot loader (e.g. GRUB).

For systems using the EFI/UEFI method, UEFI firmware reads its Boot Manager data to determine which UEFI application is to be launched and
from where (i.e., from which disk and partition the EFI partition can be found). The firmware then launches the UEFI application, for example
GRUB, as defined in the boot entry in the firmware's boot manager. This procedure is more complicated but more versatile than the older MBR
methods.

In this stage, the boot loader examines the partition table and finds a bootable partition.
Once it finds a bootable partition, it then searches for the 2nd stage boot loader, example GRUB, and loads it into RAM.

2. 2nd stage boot loader resides under /boot directory. A splash screen is displayed, which allows us to choose which OS and/or kernel to use.
After the OS & kernel are selected, the boot loader loads the kernel of the OS into the RAM and passes control to it.
Kernels are almost always compressed, so the first job they have is to uncompress themself. After this, it will check and analyze the system
hardware and initialize any hardware device drivers built into the kernel.


- The initial RAM Disk
The initramfs filesystem image contains programs and binary files that perform all actions needed to:
    - mount the proper root filesystem,
    - providing the kernel fucntionality required for the specific filesystem that will be used
    - loading the device drivers for mass storage controllers, by taking adbantage of the udev system (for user device), which is responsible
    for figuring out which devices are present.
    - locating the device drivers they need to operate properly, and loading them.
    - After the root filesystem has been found, it is checked for errors and mounted. 

The **mount** program instructs the OS that a filesystem is ready for use and associates it with a particular 

