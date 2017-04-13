# virtual-app-consumer
A shippable 'virtual app'`container for the iQAS platform that consumes observations from Kafka topic(s).

## System requirements

In order to correctly work, a virtual-app-consumer requires that the following software have been correctly installed and are currently running:
* Apache Zookeeper `3.4.9`
* Apache Kafka `0.10.2.0`
* Logstash `5.3.0`

## Building the virtual app container
Inside the resources root directory (`virtual-app-consumer`), type the following command:
```
$ docker build -t antoineog/virtual-app-consumer .
```

## Running the virtual app container
The generic command is:
```
$ docker run -p 127.0.0.1:PORT:8080 antoineog/virtual-app-consumer APPLICATION_ID JSON_REQUEST
```

You should specify the following MANDATORY and [OPTIONAL] arguments:

* `APPLICATION_ID`: The name of the virtual application
* `JSON_REQUEST`: A string that represent the request to send to the iQAS platform (remember to escape double quotes. E.g., `"{\\"param\\": \\"value\\"}"`).
* You can also pass the request by specifying a file path instead with option `-f PATH/TO/JSON/FILE`. 

Note: for more details about the format of an iQAS request, please refer to the documentation of the iQAS platform: <https://github.com/antoineauger/iqas-platform>.

For instance, following commands are valid:
```
$ docker run antoineog/virtual-app-consumer app1 "{\\"topic\\": \\"ALL\\", \\"location\\": \\"ALL\\", \\"obs_level\\": \\"INFORMATION\\"}" 
```

```
$ docker run antoineog/virtual-app-consumer app2 -f ../templates/request.json 
```

To exit the container, just press `CTRL` + `C`.

Instead, if you prefer to run the docker container in background (in detached mode), just add the `-d` option:
```
$ docker run -d antoineog/virtual-app-consumer app2 -f ../templates/request.json
```

## Managing the virtual app container

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
