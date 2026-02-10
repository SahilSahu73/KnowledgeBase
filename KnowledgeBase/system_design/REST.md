# REST
REST = Representational State Transfer

- Central idea => representation of the entities
When client sends a request, server sends a response, which is in some representation.
More often we see JSON as this representation.

Everything in REST is a resource.
E.g. if building a library management system, then books are the resource.

REST is just a specification of how the client should be asking things from the server and 
how the server should respond.

Any and every data that we have in our service is an exposed resource.
REST cannot enforce how I want to store my data in my database, it just expects a specific 
format when communicating with the API.

This is where REST gives us the flexibility, wherein the client can ask for a particular 
representation.

The representation can be in any format => JSON, Text, XML, etc.
We only care about JSON but REST does not restrict us.
REST empowers clients to demand resource in one of the format the server supports.

When client requests(asks) for some information, the request is sent to the server.
It is the servers responsibility to send the information available in the DB in rows and 
columns format to send to the user in the JSON format.
![above example's image](./KnowledgeBase/images/REST_1.png)
once the client has one "representation" it can request to update it.

The idea is: everything happens on the data/entity sent by the REST server.

## REST and underlying Protocol
It does not enforce a certain protocol, but it is most commonly implemented over HTTP.

HTTP verbs: GET, PUT, POST, DELETE has well defined meanings.
So, by seeing a particular verb we could anticipate it's purpose.
DELETE  /users/1  => DELETE the resource of type 'user' identified by id 1.
The resource is identified by the URL.

With HTTP verbs we can multiplex on the same resource.
eg: get a student's details  GET /students/1 
Instead of having an endpoint like /getstudent

update a student's details  POST /students/1 
instead of having an endpoint like /updatestudent

So we are basically using the same url but just changing the verb to accordingly change the
action performed on that data.

## Why HTTP gels up so well with REST:
It because of the already available tooling of HTTP.
Because the entire internet works on HTTP, we already have a large efficient set of tooling 
that would work as is for REST.
- HTTP client: CURL, postman, requests, etc.
- Web caches: nginx cache, varnish, ha proxy
- HTTP monitoring tools: tracing, packet sniffing
- load balancers: distribute load uniformly
- security control: SSL

## Downsides of doing REST over HTTP
- consumption is not easy
- consumption is repetitive
