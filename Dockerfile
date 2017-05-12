# A shippable 'virtual app' for the iQAS platform
# VERSION: 1.0

FROM debian:jessie
MAINTAINER Antoine Auger <antoine.auger@isae.fr>

# To pass in arguments rather than here
ENV HTTP_PROXY http://proxy.isae.fr:3128
ENV http_proxy http://proxy.isae.fr:3128
ENV HTTPS_PROXY http://proxy.isae.fr:3128
ENV https_proxy http://proxy.isae.fr:3128
ENV NO_PROXY isae.fr 
ENV no_proxy isae.fr 
ENV NO_PROXY 10.161.3.181
ENV no_proxy 10.161.3.181

# create user
RUN groupadd web
RUN useradd -d /home/bottle -m bottle

# make sure packages are up to date
RUN apt-get update && apt-get install -y \ 
	net-tools \
	python3-pip
RUN apt-get upgrade -y

# install python 3 and pip3
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install kafka-python
RUN pip3 install python-logstash

# copy directories
COPY . /home/bottle/virtualApp

# in case you'd prefer to use links, expose the port
WORKDIR /home/bottle/virtualApp/src
ENTRYPOINT ["/usr/bin/python3", "-u", "/home/bottle/virtualApp/src/main.py"]
USER bottle
