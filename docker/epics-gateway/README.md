# EPICS Gateway

EPICS is the [Experimental Physics and Industrial Control System](http://www.aps.anl.gov/epics/).

EPICS Gateway is the [Process Variable Gateway](http://www.aps.anl.gov/epics/extensions/gateway/) extension.

This image is based on [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) and additionally provides [EPICS Extensions Top 2012-09-04](https://www.aps.anl.gov/epics/download/extensions/index.php) and the Gateway Extension version 2.0.5.1 with PCRE support.

The purpose of this image is to provide a ready-to-use EPICS gateway that is preconfigured to allow all traffic.

Among other things, this is useful for forwarding Channel Access (CA) between the `docker0` network and the host machine when using docker via DockerMachine on Windows and Mac.

Resources:
- [GitHub](https://github.com/DMSC-Instrument-Data/plankton-misc/tree/master/docker/epics-gateway)
- [DockerHub](https://hub.docker.com/r/dmscid/epics-gateway/)
- [Dockerfile](https://github.com/DMSC-Instrument-Data/plankton-misc/blob/master/docker/epics-gateway/Dockerfile)


## Image Layout

Location | Contents
-------- | --------
`/EPICS/base/` | EPICS Base source and build
`/EPICS/extensions/` | EPICS Extensions Top
`/EPICS/extensions/src/gateway/` | EPICS Gateway source
`/gateway/` | Gateway home directory, contains the access, command and pvlist files
`/etc/profile.d/10-epics-gateway.sh` | Sets up environment for Gateway use


## Usage

The image is set up to run `gateway` as the `ENTRYPOINT`, so you can pass Gateway arguments directly through `docker run`. Generally, it should be invoked with the `--net=host` docker argument to give it full access to the network stack.

The client IP (`-cip`) defaults to 172.17.255.255 by means of the `EPICS_CA_ADDR_LIST` environment variable. The server IP (`-sip`) has no default and must be provided.

The `-access`, `-command` and `-pvlist` parameters are preset to `/gateway/GATEWAY.access`, `/gateway/GATEWAY.command` and `/gateway/GATEWAY.pvlist`, respectively, by the `ENTRYPOINT`. Those files are set up to configure Gateway to allow all traffic by default.

General usage:
```
$ docker run -it --net=host dmscid/epics-gateway -sip 192.168.99.100 [...]
```

This launches a Gateway -- optionally passing through any additional gateway parameters provided -- that will attempt to listen for CA requests on 192.168.99.100 and forward any it receives by broadcasting to the 172.17.0.0/16 network (by default, if no `-cip` parameter was provided).

To launch a shell in the container instead of Gateway, you can use the `--entrypoint` docker argument. Using `/init.sh` as the entrypoint will ensure the environment is set up correctly (see [dmscid/epics-base](https://hub.docker.com/r/dmscid/epics-base/) for details):
```
$ docker run -it --net=host --entrypoint /init.sh dmscid/epics-gateway
```

To launch a shell inside an already running epics-gateway container, you can use the following (ID or image name can be found using `docker ps`):
```
$ docker exec -it [ID|image_name] /init.sh
```
This can be very useful for debugging. Exiting this shell will not shut down the container or its main process.

## Routing EPICS CA Between VM and Host

The main motivation for creating this image was to enable talking EPICS CA to docker containers running [plankton](https://hub.docker.com/r/dmscid/plankton/) IOC simulators on Windows and OSX (where they run inside of a Virtual Machine) from the (real, non-VM) host machine.

To make this work, the VM needs to have an adapter that provides an IP the VM can listen on and the host can connect to. VirtualBox provides host-only and bridged adapters for this purpose (host-only typically recommended, as it avoids exposing the Gateway to any and all networks the host machine is connected to).

Once the VM is running, the following steps are required in order to enable CA communication between host and containers in the VM:

1. Determine the IP of the VM on the bridge network
2. Configure EPICS on the host to send requests to this IP
3. Run epics-gateway in the VM, passing this IP as its `-sip` parameter

#### Determining IP of the VM

If using DockerMachine, this IP can be found by simply using its `ip` command. E.g.:
```
$ docker-machine ip
1.2.3.4
```

A more general approach would be to run `ifconfig` in a terminal inside the VM, to identify the correct adapter and its IP.

#### Configuring EPICS on Host

To talk to the Gateway and IOCs behind it from the host machine, you must also ensure that EPICS is set up to use this IP when sending requests. E.g.:
```
$ export EPICS_CA_ADDR_LIST=1.2.3.4
$ export EPICS_CA_AUTO_ADDR_LIST=NO
$ export EPICS_CAS_INTF_ADDR_LIST=localhost
```

#### Running epics-gateway

When you run epics-gateway, pass it the IP of the VM as its Server IP (`-sip`) and pass docker the `--net=host` parameter to ensure the gateway can see the bridging adapter. Note that docker parameters must be passed after the docker command (`run` in this case) but before the image name. Parameters meant for gateway must be passed after the image name.

Here, we launch a gateway in detached mode, tell it to listen on 1.2.3.4, and also tell it to use "gateway" as a prefix for its own PVs:
```
$ docker run -itd --net=host dmscid/epics-gateway -sip 1.2.3.4 -prefix gateway
```

Now you should be able to caget/caput PVs inside the VM from the host machine. Here, we use the previously set "gateway" prefix, and also have another container running that is serving PVs with a "SIM" prefix:
```
$ caget gateway:load
gateway:load                   0
$ caget SIM:State
SIM:State                      init
$ caput gateway:quitFlag 1
Old : gateway:quitFlag               0
New : gateway:quitFlag               1
```
Setting the `quitFlag` to 1 will, predictably, shut down the gateway and its container.

