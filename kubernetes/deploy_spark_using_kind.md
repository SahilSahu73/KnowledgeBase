# Deploy Apache Spark on a local Kubernetes Cluster
- Kubernetes will enable us dynamic scaling, fault tolerance, and resource allocation,
ensuring optimal performance and resource utilization.

- Will be using KIND (Kubernetes in Docker) - tool designed for running kubernetes clusters using docker container as nodes.
- `kubectl` - kubernetes command line tool

- once K clusters are up and running, then we will create a docker image for apache spark, including all necessary
dependencies and configurations.
- then push the docker image to the kubernetes internal repository, making it accessible within the cluster.


