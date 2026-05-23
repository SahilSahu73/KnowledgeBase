# What is Docker ?
- The Docker engine is a daemon (a service running in the background).
- This daemon manages containers, the same way that a hypervisor manages VMs.
- Interact with docker engine by using docker CLI.
- Docker CLI and Docker engine communicate through an API.

# Why use Docker: Key Benefits
Because of the simplicity and improvements it brings to the app development lifecycle.
1. *Cost-saving*: Docker containers use far less memory, compared to VMs. Thus spend less on IT infra resources.
2. *Flexible resource sharing*: Containerized apps are all running on the same OS even though your application and its dependencies are
isolated from the underlying OS and other containers by docker containers.
3. *Multi-cloud platforms*: all cloud service providers support running docker and switching between environments is simple.
4. *Configuration and consistent delivery of your application*: offers faster, more resource efficient, and standardized way to deploy, ship
and run applications. Apps can be distributed on various platforms without worrying about framework, library, and compatibility issues.
5. *Pipelines*': allows you to standardize the development and release cycle. This acts as a form of legacy change management for apps and 
encourages CICD


Note: If we have access to Docker control socket, you can take over the machine (Because you can run containers that will access the machine's
resources). Therefore, on linux machines, the docker user is equivalent to root.
You should restrict access to it like you would protect root.
By default, docker control socket belongs to the docker group. You can add trusted users to the docker group, otherwise you will have to
prefix every docker command with sudo.

# First containers

> sudo docker run busybox echo Hello World

a more useful container - ubuntu
> sudo docker run -it ubuntu
- Brand new container, runs a bare-bones, no frills ubuntu system.
- `-it` is shorthand for `-i -t`
`-i` tells docker to connect us to the container's stdin.
`-t` tells docker that we want a sudo terminal.

> apt-get install figlet

The things we can conclude:
- we ran ubuntu container on this host
- It had different independent packages
- installing something in the container does not expose it to the host and vice-versa.
- can run any container on any host.

If we run the same command again
> docker run -it ubuntu

It starts a brand new container, it used the basic ubuntu image.
We can reuse the container that we customized but it is not the default workflow of docker.

Dockers default workflow is to always start with a fresh container.
If we need something installed in our container then build a custom image.
This workflow puts a strong emphasis on automation and repeatability.

## Non-interactive Container
> docker run jpetazzo/clock

This container will run forever
`^C` to stop
It is a user image.

**Note**: Sometimes `^C` might not work.
What actually happens when we press `^C` is that:
`SIGINT` = Signal Interrupt gets sent to the container, which means:
    - `SIGINT` gets sent to PID 1 (default case)
    - `SIGINT` gets sent to foreground processes when running with `-it`
But there is a special case for `PID 1`: it ignores all signals!
    - except `SIGKILL` and `SIGSTOP`
    - except signals handled explicitly.

PID 1 has some extra responsibilities:
    - it starts (directly or indirectly) every other process.
    - when a process exits, its processes are "reparented" under PID 1
So when PID 1 exits, everything stops:
    - on a regular machine, it causes a kernel panic
    - in a container, it kills all the processes.
We dont want PID 1 to stop accidentally, thats why we have these extra protections.
To kill these processes then we use `docker kill`.

## Run a container in the background
Containers can be started in the background, with the `-d` flag (daemon mode):
> docker run -d jpetazzo/clock

It will return the full ID of the container
The output is not shown on the screen, docker collects these outputs and logs it.

To list all the running containers:
> docker ps

It tells us:
- (truncated) ID of the containers.
- image used to start the container.
- It UP time, and other info. like Command, Port, Names etc.

We can start multiple containers by using the same command and each time it will create new containers as discussed earlier.
And when we do docker ps it will all be listed there.

In `docker ps` there are certain flags that can be used to control the list outputs.
1. `-l`(last) flag will return only the last container that was started.
2. `-q`(quiet or quick) flag will only return the IDs of the running containers.
we can even combine the flags

To view the logs:
$ docker logs <ID>
example > docker logs 068
Here we specified only the prefix (initial 3 characters of the truncated ID) of the full container ID.
We can also specify the full ID as well.
This command will output the entire log of the container which can be alot....

So use:
1. `--tail` option
> docker logs --tail 5 068

where 5 is the parameter of the no. of lines to be in the output.
can also combine it with the `--follow` option to keep printing logs in real time.
> docker logs --tail 5 --follow 068


## To stop the container
2 ways to terminate our detached container:
    - killing it using `docker kill` command
    - stopping it using `docker stop` command
`docker kill` stops the container immediately, by using the `KILL` signal.
`docker stop` is more graceful, it sends a `TERM` (terminate) signal first, and after 10 seconds, if the container has not stopped, it sends `KILL`.
Note: KILL signal cannot be intercepted, and will forcibly terminate the container.

example:
> docker stop 47d6

Now if we want to list all containers even the ones that we stopped/killed:
> docker ps --all
> docker ps -a

## Restarting and attaching to containers
There is no difference b/w background and foreground containers from Docker's perspective.
All containers run the same way, whether there is a client attached to them or not.
Analogy: attaching to a container is like plugging a keyboard and screen to a physical server.

To detach from an interactive container:
The "detach" sequence is `^P^Q`
OR detach by killing the docker client.
(not by `^C` as it will send a `SIGINT` to the container).

To attach to a container:
> docker attach <containerID>

- the container must be running
- there can be multiple clients attached to the same container.

Note: If the container was started without `-it` then we won't be able to detach with `^P^Q`
If we hit `^C`, the signal will be proxied to the container.
Remember: we can always detach by killing the container.
By default containers start in attach mode but we can run them in background using the -d option.
> docker run -d <imageName>


When a container is exited, it is in stopped state.
We can restart by:
> docker start <containerID>

It will be restarted with the same options we launched it with.


If we want to remove/delete containers from our machine:
> docker rm <containerID>
- or can use container name

If we want to remove/delete the image:
> docker rmi <imageID>
- or can use the image name

Note: to remove any image, we have to delete all the existing containers which were created using that 
image even if they are stopped.
