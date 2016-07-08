# EPICS Base Image

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

This image contains build and source of "EPICS base" version R3.14.12.5, the core EPICS software.

The purpose of this image is to provide a bare-bones, minimalistic EPICS base for other images to build upon.

This image itself is based on [Alpine](https://hub.docker.com/_/alpine/), to minimize image size and overhead.

Resources:
- [GitHub](https://github.com/DMSC-Instrument-Data/plankton-misc/tree/master/docker/epics-base)
- [DockerHub](https://hub.docker.com/r/dmscid/epics-base/)
- [Dockerfile](https://github.com/DMSC-Instrument-Data/plankton-misc/blob/master/docker/epics-base/Dockerfile)


## Image Layout and Contents

`/EPICS/base/` contains both a build and the source of EPICS base.

[`/etc/profile.d/01-epics-base.sh`](https://github.com/DMSC-Instrument-Data/plankton-misc/blob/master/docker/epics-base/copyroot/etc/profile.d/01-epics-base.sh) sets up environment variables for serving EPICS CA.

`/init` and `/init.sh` provide a minimalistic init system, which is described in the next section.


## INIT System

Docker containers lack an init or supervisor system by default. This leads to issues with rampant root zombie processes and signals sent to the container not being passed through as expected. 

These issues are described in detail [here](https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/) and [here](http://blog.dscpl.com.au/2015/12/issues-with-running-as-pid-1-in-docker.html).

Additionally, since...

1. The `ENV` directive in Dockerfiles does not currently support variable values
2. `/etc/profile` and `~/.profile` will not be sourced unless you explictly start a login shell
3. `/etc/bash.bashrc` and `~/.bashrc` will not be sourced unless you run `bash` in interactive but not login mode

... it can be tricky to reliably ensure environment variables are correctly set up with values that must be determined at runtime (such as a variable IP or hostname).

To resolve these issues, this image provides a combination of [tini](https://github.com/krallin/tini) (a tiny init system that solves the zombie and signal issues) and an `/init.sh` script (that sources `/etc/profile` and ensures tini is launched correctly). This script is used as the `ENTRYPOINT` of this image, and most derived images should do the same.

The script has the following usage:
```
/init.sh [command [arguments]]
```

This will do the following:
- `/etc/profile` is `source`d to set up the environment (which in turn `source`s `/etc/profile.d/*.sh`)
- `[command]` is run with `[arguments]`, via tini (`/init -s -g`)
- If no command was provided, `/bin/sh` is used as a default
- Assuming the script is run as the `ENTRYPOINT` or `CMD`, or by a shell that is PID 1, tini will have PID 1 so that it will receive any signals the container receives from the host
- tini will reap child processes so they don't turn into zombies and forward any signals it receives to all child processes

The init script (or any `ENTRYPOINT`) may be circumvented using the `--entrypoint` argument of `docker run`. When running a container like that, you can switch to "init mode" by sourcing `init.sh`:
```sh
$ docker run -it --entrypoint sh dmscid/epics-base
/ # ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 sh
    7 root       0:00 ps aux
/ # . /init.sh
ac28333e09e1:/# ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 /init -s -g /bin/sh
   11 root       0:00 /bin/sh
   12 root       0:00 ps aux
ac28333e09e1:/# exit
$
```
Note that `/init` has replaced `sh` as the PID 1 process, and you are now in a new shell (which defaulted to `/bin/sh` because no parameters were passed to `/init.sh`). Nevertheless, a single `exit` shuts down the container since the old shell is gone.


## Usage

This image is intended to be used as a base image. To to extend it, create a new Dockerfile and reference it using the `FROM` directive.

To make use of the above init system, you should keep the provided `ENTRYPOINT` or use `/init.sh` as the first field if you want to provide a different `ENTRYPOINT`.

We recommend setting up any required environment variables by providing an `/etc/profile.d/*.sh` script and following the `XY-some-name.sh` naming convention, where `XY` is a two-digit number. Since the scripts are sourced in alphabetical order, that number can be used to control execution order.

Example Dockerfile:
```
FROM dmscid/epics-base:latest

RUN apk --no-cache add python

COPY 10-setup-environment.sh /etc/profile.d/10-setup-environment.sh

ENTRYPOINT ["/init.sh", "python"]
```

This will create an image that drops straight into a python shell, with the environment already set up by sourcing `/etc/profile`, `/etc/profile.d/01-epics-base.sh` and `/etc/profile.d/10-setup-environment.sh` in that order.

For a real-world example, see [dmscid/epics-gateway](https://hub.docker.com/r/dmscid/epics-gateway/).

