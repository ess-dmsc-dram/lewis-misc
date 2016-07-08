# EPICS base image

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

This image contains "EPICS base", the core EPICS software. 

The purpose of this image is primarily to be used as a base for other images to build upon.

This image itself is based on [Alpine](https://hub.docker.com/_/alpine/), to minimize image size and overhead.


## Image layout and contents

`/EPICS/base` contains both a build and the source of EPICS base.

`/etc/profile.d/01-epics-base.sh` sets up the environment as follows:
```sh
EPICS_HOST_ARCH="linux-x86_64"
EPICS_BASE="/EPICS/base"
EPICS_CA_ADDR_LIST="127.0.0.1"
EPICS_CA_AUTO_ADDR_LIST="NO"
EPICS_CAS_INTF_ADDR_LIST="${ETHERNET_IPS}"

PATH="${EPICS_BASE}/bin/${EPICS_HOST_ARCH}:${PATH}"
```

`/init` and `/init.sh` provide a minimalistic init system, which is described in the next section.


## INIT System

Docker containers lack an init or supervisor system by default. This leads to issues with rampant zombie processes and signals sent to the container not being passed through as expected. These issues are described in detail [here](https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/) and [here](http://blog.dscpl.com.au/2015/12/issues-with-running-as-pid-1-in-docker.html).

Additionally, since...

1) The `ENV` directive in Dockerfiles does not currently support variable values
2) `/etc/profile` and `~/.profile` will not be sourced unless you explictly start a login shell
3) `/etc/bash.bashrc` and `~/.bashrc` will not be sourced unless you run `bash` in interactive but not login mode

... it can be quite difficult to reliably ensure environment variables are correctly set up with values that must be determined at runtime (such as a variable IP or hostname).

To resolve these issues, this image uses a combination of [tini](https://github.com/krallin/tini) (a tiny init system that solves the zombie and signal issues) and an `/init.sh` script (that sources `/etc/profile` and ensures tini is launched correctly). This script is used as the `ENTRYPOINT` of this image, and most derived images should do the same.

The script has the following usage:
`/init.sh [command [arguments]]`

This will do the following:
- `/etc/profile` is `source`d to set up the environment (which in turn `source`s `/etc/profile.d/*.sh`)
- `[command]` is run with `[arguments]`, via tini (`/init -s -g`)
- If no command was provided, `/bin/sh` is used as a default
- Assuming the script is run as the `ENTRYPOINT` or `CMD`, tini will have PID 1 so that it will receive any signals the container receives from the host
- tini will reap child processes so they don't turn into zombies and forward any signals it receives to all child processes

The init script (or any `ENTRYPOINT`) may be circumvented using the `--entrypoint` argument of `docker run`. When running a container like that, you can switch to "init-mode" by sourcing `init.sh`:
```sh
$ docker run -it --entrypoint sh dmscid/epics-base
ac28333e09e1:/# ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 sh
   11 root       0:00 ps aux
ac28333e09e1:/# . /init.sh 
ac28333e09e1:/# ps aux
PID   USER     TIME   COMMAND
    1 root       0:00 /init -s -g /bin/sh
   15 root       0:00 /bin/sh
   19 root       0:00 ps aux
ac28333e09e1:/# exit
$
```

## Usage

This image is intended to be used as a base image. To to extend it, create a new Dockerfile and reference it using the `FROM` directive.

To make use of the provided init system, you should keep the provided `ENTRYPOINT` or use `/init.sh` as the first field if you provide a different `ENTRYPOINT`.

We recommend setting up any required environment variables by providing an `/etc/profile.d/*.sh` script and following the `XY-some-name.sh` naming convention, where `XY` is a two-digit number. Since the scripts are sourced in alphabetical order, that number can be used to control execution order.

Example Dockerfile:
```
FROM dmscid/epics-base:latest

RUN apk --no-cache add python

COPY 10-setup-environment.sh /etc/profile.d/10-setup-environment.sh

ENTRYPOINT ["/init.sh", "python"]
```

This will create an image that drops straight into a python shell, with the environment set up by sourcing `/etc/profile`, `/etc/profile.d/01-epics-base.sh` and `/etc/profile.d/10-setup-environment.sh` in that order.

