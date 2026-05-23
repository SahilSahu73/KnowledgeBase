1. Optimise processes and increase throughput with the same resource. -> Vertical Scaling
2. Preparing before hand during non-peak hours -> Preprocessing & cron jobs
3. Keep backups and avoid single points of failure -> Backups
4. Hire more resources -> Horizontal scaling
5. Micro services -> we have all responsibilities well defined
    have separate or specialized teams/components to handle each request.
    (dividing responsibilities)
6. Distributed system (partitioning)
7. Load Balancer
8. Decoupling
9. logging and metrics
10. Extensible

## Difference b/w Horizontal and Vertical Scaling

### Horizontal Scaling:
- Here we have multiple machines and can be scaled linearly as much we want.
- Since we have multiple machines, therefore require load balancers.
- It is Resilient, if one machine fails then we have another machines to provide the service.
- The communication b/w machines is done over the network through network calls (RPC), is 
  quite slow compared to IPC(Inter Process Communication).
- Data Inconsistency, as each machine has it's own storage and databases, which needs some 
loose transactional guarantee, which makes data consistency a real issue, but can be handled.
- Scales well as user increases.

### Vertical Scaling:
- It is one big machine with lots of compute power and storage.
- Since only one machine so no load balancing required.
- Single point of failure.
- Inter Process communication
- Consistent since all data is at one place only.
- Hardware limit, there is a limit upto which we can make the machine bigger.
