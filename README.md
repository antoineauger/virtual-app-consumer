# virtual-app-consumer
A shippable 'virtual app'`container for the iQAS platform that consumes observations from Kafka topic(s).

### Building the virtual app container
Inside the resources root directory (`virtual-app-consumer`), type the following command:
```
$ docker build -t antoineog/virtual-app-consumer .
```

### Running the virtual app container
The generic command is:
```
$ docker run -p 127.0.0.1:PORT:8080 antoineog/virtual-app-consumer
```

You should specify the following MANDATORY and [OPTIONAL] arguments:

* TODO

For instance, following commands are valid:
```
TODO
```

To exit the container, just press `CTRL` + `C`.

Instead, if you prefer to run the docker container in background (in detached mode), just add the `-d` option:
```
$ docker run -d -p 127.0.0.1:9092:8080 antoineog/virtual-app-consumer
```

### Managing the virtual app container

The following are a quick remainder of basic docker commands.

You can see docker containers and their statuses by running `docker ps`. 
```
$ docker ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                      NAMES
0657fb1624c3        antoineog/virtual-app-consumer   "/usr/bin/python3 /ho"   47 seconds ago      Up 51 seconds       127.0.0.1:9092->8080/tcp   prickly_roentgen
```
Note: use the command `docker ps -a` if the list is empty or if you do not find your container.

To stop a given container, just type the following command:
```
$ docker stop prickly_roentgen
prickly_roentgen
```

Now the container is stopped, you can remove it:
```
$ docker rm prickly_roentgen
prickly_roentgen
```
