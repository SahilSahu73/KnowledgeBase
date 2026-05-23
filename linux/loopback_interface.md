The Internet Protocol (IP) specifies a loopback network with the (IPv4) address 127.0.0.0/8.
Most commonly used IP address on the loopback network is 127.0.0.1 for IPv4 and ::1 for IPv6.
Standard domain name for the address is `localhost`.

Most IP implementations support a loopback interface (lo0) to represent the loopback facility.
Any traffic that a computer program sends on the loopback network is addressed to the same computer.

A network device also includes an internal loopback interface (lo0.16384).
The internal loopback interface is a particular instance of the loopback interface with the logical unit no. 16384

- Can use the loopback interface to identify the device.
(we can use any interface address to determine if the device is online, the loopback address is preferred, because
interfaces might get removed or addresses changed based on network topology changes, the loopback address never changes.

- When you ping an individual interface address, the results do not always indicate the health of the device.
  For example, a subnet mismatch in the configuration of two endpoints on a point-to-point link makes the link appear to be inoperable.
  Pinging the interface to determine whether the device is online provides a misleading result.
  An interface might be unavailable because of a problem unrelated to the device configuration or operation.
  You can use the loopback interface to address these issues.
