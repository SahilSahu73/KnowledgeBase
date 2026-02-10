## Troubleshooting commands
1. docker logs => in detail in [docker_intro](./intro.md)
2. docker exec
So now if we want to execute any command in an already running container, we can use this command:
> docker exec -it <containerID> /bin/bash
> docker exec -it <containerID> /bin/sh

here we are trying to execute the bash or sh binary of the container in interactive mode, so that we can
access the terminal of the container and get further details from within it, while it is running.
Also when we exit this interactive session which we started from the above command, it won't stop 
the container (like previously it did), but we have just exitted this session and the container will
still be running.

