# Understanding Docker Images

## What is an image
Image = files + metadata
These files form the root filesystem for the container.

metadata can indicate:
for e.g.: the author of the image, commands to execute in the container when starting it, env. variables to be set, etc.

- Images are made of layers, conceptually stacked on top of each other.
- Each layer can add, change and remove files and/or metadata.
- Images can share layers to optimize disk usage, transfer times, and memory use.

## Difference b/w containers and images
- image is a read-only filesystem
- a container is an encapsulated set of processes, running in a read-write copy of that filesystem.
- to optimize container boot time, copy-on-write is used instead of regular copy.
- `docker run` starts a container from a given image.

comparison or analogy:
- Images conceptually similar to classes.
- Layers = inheritance
- Containers = instances

Since the images are Read-only, how do we change it?
- we dont.
- we create a new container from that image.
- make changes to that container.
- When satisfied with those changes, we transform them into a new layer.
- a new image is created by stacking the new layer on top of the old image.

Note: only way to create an image is by "freezing" a container.
only way to create a container is by instantiating an image.
So, There is a special empty image called `scratch`.
    - It allows to build from scratch.
The `docker import` command loads a tarball into docker (tar/zip file).
    - the imported tarball becomes a standalone image.
    - that new image has a single layer.
*Will probably never need this but good to know*


## Creating other images
`docker commit`
- saves all the changes made to a container into a new layer.
- Creates a new image (effectively a copy of the container).

`docker build` (will be used 99% of the time)
- performs a repeatable build sequence.


## Namespaces
3 namespaces:
1. Official images => e.g. ubuntu, busybox etc.
2. User (and organizations) images => e.g. jpetazzo/clock
3. Self-hosted images => registry.example.com:5000/my-private/image

Root namespaces:
- official images, gated by Docker Inc.
- generally authored and maintained by third-party
- includes: Distro images, ready-to-use components and services like redis, postgresql...

User namespaces:
- holds images for Docker Hub users and organizations
- In jpetazzo/clock => Docker Hub user is jpetazzo, and image name is clock.

Self-hosted namespaces:
- images hosted in 3rd-party registries.
- contains the hostname (or IP address), and optionally the port, of the registry server.
e.g. localhost:5000/wordpress
localhost:5000 => host and port of the registry
wordpress => name of the image


To store and manage images:
We use the docker client to tell a docker engine to push and pull images to and from a registry.

Use `docker search <image name>` to search for images in a remote registry

## Download images
2 ways to download images:
- explicitly, with `docker pull`
- implicitly, when executing `docker run` and the image is not found locally.

## Pulling an image
> docker pull debian:jessie

- as seen previously, images are made up of layers.
- Docker will download all necessary layers.
- In the above example, `:jessie` indicates which exact version of Debian we would like.
It's a version tag.

Images can have tags, they define image versions or variants.
`docker pull ubuntu` will refer to `ubuntu:latest`
The `:latest` tag is generally updated often.

No need to specify tags when:
- doing rapid testing and prototyping.
- experimenting
- we want the latest version.

Only specify tags when:
- recording a procedure into a script.
- going to production.
- to ensure that the same version will be used everywhere.
- to ensure repeatability later.

## Multi-arch images
- An image can support multiple architectures.
- More precisely, a specific tag in a given repo can have either:
    - a single manifest referencing an image for a single architecture.
    - a manifest list (or fat manifest) referencing multiple images.
- In a manifest list, each image is identified by a combination of:
    - os (linux, windows)
    - architecture (amd64, arm64, arm....)
    - optional fields like variant, os.version etc.
- The docker engine will pull "native" images when available (images matching it's own OS/achitecture/variant)
- we can ask for a specific image platform with `--platform` option
- The docker engine can run non-native images thanks to **QEMU+binfmt**.

## Port Binding
Whenever a container is created using an image, by default all docker containers have a port binded to them.
For example: when we create a MySQL container we see that it has a port 3306/tcp attached to it.
Now this port is different from the port of the host machine.
The 3306 is the containers port, and other host port e.g. 8080 is different, so if we want to 
establish a communication between them, then we have to do port binding, specifying the host port and the container port using the `-p` option.
> docker run --name some_mysql -d -e MYSQL_ROOT_PASSWORD=some_pass -p 8080:3306 mysql

Now since this port (8080) is assigned to the mysql container we cannot use the same host machine 
port for another container.
WE need to use another host machine port for another container.
Also different images might have the same port number written i.e. mysql:latest image will have 3306 
port as well as mysql:8.0 will have the same 3306 port but it does not mean that they are the same ports
They are different images and when containers are created from them, they will be seperate environments
so, we have to bind different host machine ports to those container ports.

# Building Images Interactively

We will first manually try the entire process.
1. set up the ubuntu container (or of any distro) using the `docker run` command.
> docker run -it ubuntu

2. We will then run a bunch of commands to install and set up our software in the container.
> apt-get update && apt-get install figlet

This will refresh the list of packages available to install and install the program we are interested in.
Note: This 2nd command is being run inside the container.

3. Now we exit the docker container using `exit` command and run `docker diff` to see differences b/w the base image
and our container.
> docker diff <containerID>

as mentioned before:
image is read-only. when we make changes, they happen in a copy of the image.
docker can show the difference b/w the image and it's copy.
for performance, docker uses copy-on-write systems.
(i.e. starting a container based on a big image doesn't incur a huge copy.)
`docker diff` gives an easy way to audit changes.
Note: Containers can also be started in read-only mode.
(their root FS will be read-only but they can still have read-write data volumes)

4. Commit our changes using `docker commit` which will create a new layer with those changes, and new image using
this new layer.
> docker commit <containerID>

This will output the ID of the newly created image (imageID), which can be used as an argument for docker run.

5. we can then do `docker run <newImageID>` and inside it run `figlet hello` which will work and then also see
that it is a new image that is created.

6. We can also tag the image as referencing the image by its ID everytime is not convenient.
> docker tag <newImageID> figlet

we can also specify the tag as an extra argument to `commit`:
> docker commit <containerID> figlet

Then we can run it normally using the tag in the command instead of the ID.
> docker run -it figlet

every time we do `docker run` we create a new container.
but by using docker start and docker stop commands, we can restart or stop an existing container.
If we want to restart an existing container, we can use:
> docker start <containerID>
- can also use it's name to start it again. 

We can also specify some environment variables while starting the container using the `-e` option.
So we basically declare them while starting the contianer itself (like a password)
example while starting a mySQL container we run it in detach mode and specify the mySQL root password
in the env. var.
> docker run -e MYSQL_ROOT_PASSWORD=some_password -d mysql:<tag>

Also each container is given a default random name by docker, so to give it a custom name we can use
the --name option.


# Building Docker images with a dockerfile
A `Dockerfile` is a build recipe for a docker image.
It contains a series of instructions telling docker how an image is constructed.
The `docker build` command builds an image from a `Dockerfile`.

## writing 1st Dockerfile
It should be in a new, empty directory.
> mkdir myimage
> cd myimage
> vim Dockerfile

Inside the dockerfile we write:
```
FROM ubuntu
RUN apt-get update
RUN apt-get install figlet
```
- `FROM` indicates the base image for our build
- Each `RUN` line will be executed by docker during the build.
Note: Our `RUN` commands must be non-interactive. No inputs can be provided to Docker during the build.
We can use -y flag in the apt-get

> docker build -t figlet .

- `-t` indicates the tag to apply to the image.
- `.` indicates the location of the build context.

**The things that happened when we build the image by the above command**:
- The build can be done by the BuildKit or by the "old-style" builder.
The difference b/w them:
Classic Builder:
    - Classic builder copies the whole "build context" to the Docker Engine.
    - It is linear (processes lines one after the other)
    - requires full docker engine
BuildKit:
    - only transfers parts of the "build context" when needed.
    - will parallelize operations (when possible)
    - can run in non-priviledged containers (e.g. kubernetes)

Basically what happens is:
- build context is the `.` directory given to `docker build`.
- it is sent (as an archive) by the docker client to the docker daemon.
- This allows to use a remote machine to build using local files.
- can use `.dockerignore` to speed the process up as it will ignore the specific files mentioned in it.
(only add those files that you won't need in the build context)

The process that happened was:
- A container was created from the base image.
- RUN commands were executed in this container.
- container is committed into an image.
- The build container is removed.
- the output of this step will be the base image for the next one.

Now BuildKit process:
- Transfers the Dockerfile and build context. (1st 2 [internal] stages)
- Then it executes the steps defined in the Dockerfile
- Finally exports the result of the build. (image definition + collection of layers)

## The caching system
If we run the same build again, it will be instantaneous.
- after each build step, Docker takes a snapshot of the resulting image.
- before executing next step, it checks if it has already built the same sequence.
- It uses the exact string defined in the Dockerfile, so:
    - RUN apt-get install figlet cowsay is different from install cowsay figlet

To force a rebuild:
> docker build --no-cache ...

## Using image and viewing history
`history` command lists all the layers composing an image.
- for each layer it shows its creation time, size, and creation command.
- when an image was built with a Dockerfile, each layer corresponds to a line of the Dockerfile.
> docker history figlet

**Why `sh -c`** was mentioned in the "created by" column of the history?
- when we run a command for e.g. `ls -l /tmp`, something needs to parse the command.
(i.e. split the program and it's arguments into a list)
This needs to be done because in UNIX like systems to start a new program, we need two system calls:
    - fork(), to create a new child process;
    - execve(), to replace the new child process with the program to run.
    - conceptually execve() works like this:
        - execve(program, \[list, of, arguments])
The shell is the one who does this.
So when we do `RUN ls -l /tmp`, the Docker builder needs to parse the command.
Instead of implementing it's own parser, it outsources this job to the shell.
That's why we see `sh -c ls -l /tmp` in that case.
We can also do the parsing job ourselves, by passing `RUN` a list of arguments.
This is called the *exec* syntax.

So according to *exec* syntax the Dockerfile should look like:
> RUN \["apt-get", "install", "figlet"]

So if we build the container using this line in our Dockerfile then we can see that:
- Exec syntax specifies an exact command to execute.
- shell syntax specifies a command to be wrapped within `/bin/sh -c "..."`.

When to use either of them:
- Shell syntax:
    - easier to write
    - interpolates environment variables and other shell expressions
    - creates an extra process to parse the string (/bin/sh -c "...")
    - requires /bin/sh to exist in the container.

- exec syntax:
    - is harder to write (and read!) (I dont think so)
    - passes all arguments without extra processing
    - doesn't create an extra process
    - doesn't require /bin/sh to exist in the container.

Example using `exec`
> CMD exec figlet -f script hello

In this example, `sh -c` will still be used, but `figlet` will be PID 1 in the container.
The shell gets replaced by figlet when figlet starts execution.
This allows to run processes as PID 1 without using JSON.


## `CMD` and `ENTRYPOINT`
These commands allow us to set default command to run in a container.
example: we want the command "figlet -f script hello" to be executed when the container starts.
So, in the dockerfile we will add this line:
> CMD figlet -f script hello

- `CMD` defines a default command to run when none is given.
- can appear at any point in the file.
- Each `CMD` will replace and override the previous one, so having multiple CMD lines is useless.
- After the default command is executed given by `CMD` the container will get stopped and exit.

Overriding CMD
- If we want to get a shell into our container (instead of figlet), we just have to specify a different program
to run:
    > docker run -it figlet bash
    - here we specified bash and it replaced the value of CMD.
(command line arguments will take priority over the CMD when specified.)

Using `ENTRYPOINT`
- we want to input the message on the command-line that should be printed, while retaining figlet and some params.
> docker run figlet salut
- so salut should get printed instead of the default hello.

Adding entrypoint defines a base command (and its parameters) for the container.
The command-line arguments are appended to those parameters.
like CMD, entrypoint can appear anywhere, and replace the previous value.

The new dockerfile will look like:
```
FROM ubuntu
RUN apt-get update
RUN ["apt-get", "install", "figlet"]
ENTRYPOINT ["figlet", "-f", "script"]
CMD ["hello world"]
```

Now when we give any command-line argument, that will replace the CMD command (parameter) which was suppose to go 
as a default parameter if none is given.

Note: why we used JSON syntax for CMD and ENTRYPOINT?
because if we give string syntax, it gets wrapped in sh -c
to avoid this wrapping, we use JSON syntax

cause if we use string syntax in entrypoint, then it would look something like this:
> sh -c "figlet -f script" salut
- This will not work and not print anything.

So when using both CMD and ENTRYPOINT, it is necessary to use JSON syntax for both.

Now what if we want to override the ENTRYPOINT command.
To do so we use the --entrypoint parameter.

So now if I run the command:
> docker run -it --entrypoint bash figlet
- this will override the entrypoint line and execute the bash command and give access to the bash terminal
So overriding both the statements entrypoint and cmd.
Note here we have the -it option as well to get the terminal.

When to use entrypoint vs cmd?
- ENTRYPOINT is good for containerized binaries.
example: docker run consul --help
- CMD is great for images with multiple binaries.
example: docker run busybox ifconfig
(pretend docker run is not there, we basically want to do the same thing but with the dockerfile.)


## Copying files during the build

We can copy files from the build context to the container that we are building.
Note: Build context is the directory containing the `Dockerfile`

### Build some C code

- Build a container that compiles a basic "Hello World" program in C.
```
``` C
int main() {
  puts("Hello World!");
  return 0;
}
```
We now create a dockerfile with these commands
```
FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential
COPY hello.c /
RUN make hello
CMD /hello
```
The `-y` flag was essential because the build cannot be interactive and it will end up failing.
Then we use COPY to place the source file into the container.
The package build-essential will get us a compiler.

Steps:
1. go inside a directory in which we created 2 files: Dockerfile and hello.c (The file containing our code)
2. once they both are written we executed the following commands.
> docker build -t hello .
> docker run hello

- Docker can cache steps involving COPY and those steps will not be executed again if the files haven't changed.
- We can copy whole directories recursively => `COPY . .`
(but it might require extra precautions to avoid copying too much)

Another better way of compiling a C code inside the container:
  - place it in a different directory, with the `WORKDIR` instruction
  - even better, use the `gcc` official image.

## .dockerignore
- can create this file at the top-level of the build context.
- contains filename and globs to ignore.
- They won't be sent to the builder (so won't end up in the resulting image)

## Exercise
In the wordsmith directory created one Dockerfile for each component of the project.
