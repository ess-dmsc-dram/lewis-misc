FROM dmscid/epics-base:latest

# Runtime dependencies
RUN apk --no-cache add \
    libstdc++ \
    python \
    py-pip \
    readline

# Build latest pcaspy and cleanup
RUN apk --no-cache add --virtual build-dependencies g++ readline-dev git swig python-dev \
    && . /etc/profile \
    && git clone https://github.com/paulscherrerinstitute/pcaspy.git \
    && cd /pcaspy \
    && git checkout f74a052c158688d8528a2620ce196d09f5355078 \
    && python setup.py install \
    && cd / \
    && rm -rf /pcaspy \
    && apk del build-dependencies

