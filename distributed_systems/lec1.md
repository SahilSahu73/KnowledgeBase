# Why make a system distributed?
1. Some systems are inherently distributed.
  e.g. sending a message from your mobile to your friend's mobile.
  It involves sending data over the network from one system to another.

2. For better Reliability:
  Even if one node fails, the system as a whole keeps functioning.

3. For better Performance:
  Get data from a nearby node rather than one halfway round the world.

4. To solve bigger problems:
  e.g. huge amounts of data, can't fit on one machine.

# Why NOT make a system distributed?
The trouble with distributed systems:
- Communication may fail (and we might not even know it has failed.)
- Processes may crash (and we might not know)
- All of this may happen nondeterministically.

To prevent them we need:
**Fault Tolerance** - We want the system as a whole to continue working, even when some parts are faulty.

# Distributed Systems and Computer Networking
