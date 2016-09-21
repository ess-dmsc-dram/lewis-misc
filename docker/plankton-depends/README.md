# EPICS with PCASpy

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

PCASpy provides [Python bindings for the Portable Channel Access Server](https://pcaspy.readthedocs.io/en/latest/).

This image is based on [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) and additionally provides Python, Pip and PCASpy v0.6.0.

The purpose of this image is primarily to be used as a base for other images to build upon.

Resources:
- [GitHub](https://github.com/DMSC-Instrument-Data/plankton-misc/tree/master/docker/epics-pcaspy)
- [DockerHub](https://hub.docker.com/r/dmscid/epics-pcaspy/)
- [Dockerfile](https://github.com/DMSC-Instrument-Data/plankton-misc/blob/master/docker/epics-pcaspy/Dockerfile)


## Usage

This image is intended to be used as a base image. To to extend it, create a new Dockerfile and reference it using the `FROM` directive.

To make use of the init system, you should keep the provided `ENTRYPOINT` or use `/init.sh` as the first field if you want to provide a different `ENTRYPOINT`.

We recommend setting up any required environment variables by providing an `/etc/profile.d/*.sh` script and following the `XY-some-name.sh` naming convention, where `XY` is a two-digit number. Since the scripts are sourced in alphabetical order, that number can be used to control execution order.

See [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) for details.

See [dmscid/plankton](https://hub.docker.com/r/dmscid/plankton/) for a usage example.

