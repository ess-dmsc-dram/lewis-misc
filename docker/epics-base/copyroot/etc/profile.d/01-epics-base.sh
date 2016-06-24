ETHERNET_IPS="`ifconfig | awk -v ORS=" " '/inet addr/{print substr(\$2,6)}'`"

export EPICS_HOST_ARCH="linux-x86_64"
export EPICS_BASE="/EPICS/base"
export EPICS_CA_ADDR_LIST="127.0.0.1"
export EPICS_CA_AUTO_ADDR_LIST="NO"
export EPICS_CAS_INTF_ADDR_LIST="${ETHERNET_IPS}"

export PATH="${EPICS_BASE}/bin/${EPICS_HOST_ARCH}:${PATH}"

