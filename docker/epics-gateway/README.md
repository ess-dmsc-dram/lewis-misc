# EPICS Gateway

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

EPICS Gateway is the [Process Variable Gateway](http://www.aps.anl.gov/epics/extensions/gateway/) extension.

This image is based on [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) and additionally provides [EPICS Extensions Top 2012-09-04](https://www.aps.anl.gov/epics/download/extensions/index.php) and the Gateway Extension version 2.0.5.1 with PCRE support.

The purpose of this image is to provide a ready-to-use EPICS gateway that is preconfigured to allow all traffic.

Among other things, this is useful for forwarding Channel Access between the `docker0` network and the host machine when using docker via DockerMachine on Windows and Mac.

Resources:
- [GitHub](https://github.com/DMSC-Instrument-Data/plankton-misc/tree/master/docker/epics-gateway)
- [DockerHub](https://hub.docker.com/r/dmscid/epics-gateway/)
- [Dockerfile](https://github.com/DMSC-Instrument-Data/plankton-misc/blob/master/docker/epics-gateway/Dockerfile)


## Image Layout and Contents

`/EPICS/base/` contains EPICS Base.

`/EPICS/extensions/` contains EPICS Extensions Top.

`/EPICS/extensions/src/gateway/` contains EPICS Gateway source.

`/gateway/` is set as the Gateway home directory. It contains the access, command and pvlist files, and any logs or reports will be written here.


## Usage

The image is set up to run `gateway` as the `ENTRYPOINT`, so you can pass Gateway arguments directly through `docker run`. Generally, it should be invoked with the `--net=host` docker argument to give it full access to the network stack.

The client IP (`-cip`) defaults to 172.17.255.255 by means of the `EPICS_CA_ADDR_LIST` , so the gateway



