# Logical Volume Management
- Storage device management - gives user the power to pool and abstract the physical layout
of component storage devices for flexible administration.
- Utilizes the device mapper linux kernel framework - can be used to gather existing storage
devices into groups and allocate logical units from the combined space as needed.

Advantages:
1. allows dynamic storage allocation
2. efficient snapshot creation
3. improved disk I/O performance
4. Simplified disk management tasks

Usecases:
1. Creating single logical volumes of multiple phy. vols. or entire hard disks,
allowing for dynamic storage resizing.
2. Performing consistent backups by taking snapshots of the logical volumes.

Key components:
1. Physical volumes
2. Volume Groups
3. Logical Volume


