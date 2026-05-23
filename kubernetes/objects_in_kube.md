# Objects in Kubernetes
- Kubernetes Objects are persistent entities in the kubernetes system.
- Kubernetes uses these entities to represent the state of the cluster.
Specifically, they describe:
    - what containerized applications are running (and on which node)
    - resources available to those applications
    - The policies around how those applications behave, such as restart policies, upgrades, and fault tolerance.

- Kuberenetes Object is a "record of intent"
    - once an object is created, the Kubernetes system will constantly work to ensure that the object exists.
We are basically defining our cluster's desired state to the system, i.e. telling what we want our cluster's workload to look like.

- To work with kubernetes objects - whether to create, modify, or delete them - we'll need to use the kubernetes API.

- Every K-Object includes two nested object fields that govern the object's configuration:
`spec` and `status`.
- set the `spec` when we have to create the object, providing a description of the characteristics you want the resource to have
it's *desired state*.

- The `status` describes the current state of the object, supplied and updated by the kubernetes system and its components.
- Kubernetes CP continually and actively manages every object's actual state to match the desired state you supplied.

- E.g.: in K8s, a Deployment is an object that can represent an application running on your cluster.
When we create the Deployment, we might set the Deployment `spec` to specify that we want 3 replicas of the application to be running.
The system will read this spec and start 3 instances of the app - updating the status to match our spec.
If any of the instances should fail (a status change), the system responds to the difference b/w spec and status by making a correction,
in this case, starting a replacement instance.

## Describing Kubernetes Object
- we must provide the object spec that describes its desired state, as well as some basic info. about the object (like name).
- We provide this information to `kubectl` in a file known as *manifest*.
- By convention *manifests* are YAML, which is converted to JSON by kubectl when making the API request over HTTP.

Example manifest: `deployment.yaml`
```yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2 # tells deployment to run 2 pods matching the template
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```

- To use this manifest, we can pass this file as an argument to `kubectl apply`:
> kubectl apply -f application/deployment.yaml

It will output something similar to this:
> deployment.apps/nginx-deployment created

- To create kubernetes object, need to set values of the following fields:
    - `apiVersion`: which version of kubernetes API you're using to create this object
    - `kind`: what kind of object you want to create
    - `metadata`: Data that helps uniquely identify the object, including a `name` string, `UID`, `namespace`(optional)
    - `spec`: what state you desire for the object.


