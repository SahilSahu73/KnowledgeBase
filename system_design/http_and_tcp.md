Communication b/w our devices and the internet takes place using a protocol.
2 most common ones:
1. HTTP - Hyper Text Transfer Protocol
2. HTTPS - Hyper Text Transfer Protocol Secure

Analogy:
Regular postal service delivering letters without an envelope. Anyone along the way can read them.
HTTPS on the other hand is like sending those same letters sealed inside a locked envelope. Only the
sender and receiver can understand the contents.

HTTP is the standard protocol used by web browsers and servers to communicate and exchange data.
Operates on port 80 by default.
Transfers data in plain text, meaning the content is not protected.
Because it is unencrypted, attackers can intercept or modify the data easily.
Majorly used by non-sensitive websites where security is not a concern.

HTTPS is an extension of HTTP with added layer of security through encryption.
Operates on port 443 by default.
It uses SSL (Secure Socket Layers) or TLS (Transport Layer Security) to encrypt the data.
Even if attackers capture the traffic, they wont be able to read the actual message.

# TCP
Set of communication protocols that support network communication.
It has 5 layers:
1. Application
2. Transport
3. Network
4. Data Link
5. Physical
