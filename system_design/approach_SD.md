What is System Design?
Customer needs -> Product and Business Requirements -> System to satisfy them.

The system could be:
  - an application = end-to-end feature
  - a microservice = pure engineering solution that someone else needs
  - a library = common library support
  - a hardware = embedded

When someone says design a system, it could be one or all of the following:
1. a high level architecture design - Macro, Bird's eye view
  a high level over view of how many micro-services are there and how they will interact with
  each other and how persistence is done etc.

2. a logical design - In this they can ask us to design Business logics, Algorithms,
  Data Structures, core storage techniques that we might use etc.

3. a Physical design - Where we will have to design the storage part, I/O operations, 
  Hardware, capacity estimation, Data Backup & Restore, Pipeline.

How to approach System Design:
1. Spiral Approach:
  In this approach we first decide the core of our SD, and start building around it.
  example: we start with storage, that I am using MySQL, then I have to provide an API 
  then also add a Queue to it......

  Use this approach when we are pretty confident on the decisions we are making.
  
  So, here we move from one service to another and build around the main one and support it.
  Like I first chose the databse, then build an API service and load balancer to handle
  requests, then provide another service and attach to the existing or build around it.

2. Incremental MVP approach:
  We start with a simple and basic Day0 architecture, and then evolve it.
  Example => SQL DB, one API server and a user.
  Over time scale each component to handle the scale at the next level.


## Key Pointers
1. Every system is infinitely buildable.....Fence it. -  Restrict the scope.
2. Seek clarifications from senior or interviewer.
3. Ask critical questions that challenges the design decisions.

**One thing that always works is Divide and Conquer**
**Start small, build on top.**

