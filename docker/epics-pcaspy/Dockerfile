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
    && git checkout 5d0f3f19df90ba585f8206f3a635e342158d092c \
    && python setup.py install \
    && cd / \
    && rm -rf /pcaspy \
    && apk del build-dependencies

