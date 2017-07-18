# virtual-app-consumer
A shippable "virtual app" container that consumes observations from Kafka topic(s) through the iQAS platform or not.

## The iQAS ecosystem

In total, 5 Github projects form the iQAS ecosystem:
1. [iqas-platform](https://github.com/antoineauger/iqas-platform) <br/>The QoO-aware platform that allows consumers to integrate many observation sources, submit requests with QoO constraints and visualize QoO in real-time.
2. [virtual-sensor-container](https://github.com/antoineauger/virtual-sensor-container) <br/>A shippable Virtual Sensor Container (VSC) Docker image for the iQAS platform. VSCs allow to generate observations at random, from file, or to retrieve them from the Web.
3. [virtual-app-consumer](https://github.com/antoineauger/virtual-app-consumer) (this project)<br/>A shippable Virtual Application Consumers (VAC) Docker image for the iQAS platform. VACs allow to emulate fake consumers that submit iQAS requests and consume observations while logging the perceived QoO in real-time.
4. [iqas-ontology](https://github.com/antoineauger/iqas-ontology) <br/>Ontological model and examples for the QoOonto ontology, the core ontology used by iQAS.
5. [iqas-pipelines](https://github.com/antoineauger/iqas-pipelines) <br/>An example of a custom-developed QoO Pipeline for the iQAS platform.

## System requirements

In order to correctly work, a virtual-app-consumer requires that the following software have been correctly installed and are currently running:
* Docker (see the [official website](https://www.docker.com/) for installation instructions)
* Apache Zookeeper `3.4.9`
* Apache Kafka `0.10.2.0`
* Logstash `5.3.0`
* iQAS platform if using `-withIQAS` option

## Project structure

```
project
│
└───etc
│   │   capabilities.config
│   │   app.config
│
└───src
    │
    └───utils
    │   │   http_utils.py
    │   │   obs_utils.py
    │   │   time_utils.py
    │
    │   main.py
    │   report.py
    │   consumer.py
```

## Building the virtual app container
Inside the resources root directory (`virtual-app-consumer`), type the following command:
```
$ docker build -t antoineog/virtual-app-consumer .
```

## Running the virtual app container
The generic command is:
```
$ docker run antoineog/virtual-app-consumer -withIQAS APPLICATION_ID JSON_REQUEST
```
or
```
$ docker run antoineog/virtual-app-consumer APPLICATION_ID LIST_TOPICS_TO_PULL_FROM
```

You should specify the following MANDATORY and [OPTIONAL] arguments:

* `-withIQAS`: Perform an iQAS request according to the specified template file and then start pull observation from the assigned topic.
* `APPLICATION_ID`: The name of the virtual application
* `JSON_REQUEST`: A string that represent the request to send to the iQAS platform (remember to escape double quotes. E.g., `"{\"param\": \"value\"}"`).
* `LIST_TOPICS_TO_PULL_FROM`: A comma-separated list of topics to directly pull observations from (only used when the `-withIQAS` option is absent). For the moment, it is not possible to specify QoO requirements when not using iQAS.

Note: for more details about the format of an iQAS request, please refer to the documentation of the iQAS platform: <https://github.com/antoineauger/iqas-platform>.

For instance, following commands are valid:
```
$ docker run antoineog/virtual-app-consumer -withIQAS app1 "{\"application_id\": \"app1\", \"topic\": \"ALL\", \"location\": \"ALL\", \"obs_level\": \"INFORMATION\"}"
```

```
$ docker run antoineog/virtual-app-consumer app2 "temperature,visibility"
```

To exit the container, just press `CTRL` + `C`.

Instead, if you prefer to run the docker container in background (in detached mode), just add the `-d` option:
```
$ docker run -d antoineog/virtual-app-consumer -withIQAS app1 "{\"application_id\": \"app1\", \"topic\": \"ALL\", \"location\": \"ALL\", \"obs_level\": \"INFORMATION\"}"
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

## Acknowledgments

The iQAS platform have been developed during the PhD thesis of [Antoine Auger](https://personnel.isae-supaero.fr/antoine-auger/?lang=en) at ISAE-SUPAERO (2014-2017).

This research was supported in part by the French Ministry of Defence through financial support of the Direction Générale de l’Armement (DGA).

![banniere](https://github.com/antoineauger/iqas-platform/blob/master/src/main/resources/web/figures/banniere.png?raw=true "Banniere")
