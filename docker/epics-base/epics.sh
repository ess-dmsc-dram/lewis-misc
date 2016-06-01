ETH0_IP="`ifconfig eth0 | awk '/inet addr/{print substr(\$2,6)}'`"

export EPICS_HOST_ARCH="linux-x86_64"
export EPICS_BASE="/EPICS/base"
export EPICS_CA_ADDR_LIST="localhost"
export EPICS_CA_AUTO_ADDR_LIST="NO"
export EPICS_CAS_INTF_ADDR_LIST="localhost ${ETH0_IP}"

export PATH="${EPICS_BASE}/bin/${EPICS_HOST_ARCH}:${PATH}"

