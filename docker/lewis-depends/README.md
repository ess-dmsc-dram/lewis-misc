# Lewis Dependencies

The purpose of this image is to serve as a base for [dmscid/lewis](https://hub.docker.com/r/dmscid/lewis/). It contains all dependencies that require lengthy compilation or heavy build-time dependencies to allow the Lewis image build to be as quick and lightweight as possible.

This image is based on [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) and additionally provides:
- Python
- Pip
- PCASpy
- PyZMQ

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

PCASpy provides [Python bindings for the Portable Channel Access Server](https://pcaspy.readthedocs.io/en/latest/).

Resources:
- [GitHub](https://github.com/DMSC-Instrument-Data/lewis-misc/tree/master/docker/lewis-depends)
- [DockerHub](https://hub.docker.com/r/dmscid/lewis-depends/)
- [Dockerfile](https://github.com/DMSC-Instrument-Data/lewis-misc/blob/master/docker/lewis-depends/Dockerfile)


## Usage

This image is intended to be used as a base image. To to extend it, create a new Dockerfile and reference it using the `FROM` directive.

To make use of the init system, you should keep the provided `ENTRYPOINT` or use `/init.sh` as the first field if you want to provide a different `ENTRYPOINT`.

We recommend setting up any required environment variables by providing an `/etc/profile.d/*.sh` script and following the `XY-some-name.sh` naming convention, where `XY` is a two-digit number. Since the scripts are sourced in alphabetical order, that number can be used to control execution order.

See [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) for details.

See [dmscid/lewis](https://hub.docker.com/r/dmscid/lewis/) for a usage example.

