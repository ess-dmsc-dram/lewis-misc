FROM dmscid/epics-base:latest

# Runtime dependencies
RUN apk --no-cache add \
    libstdc++ \
    python \
    py-pip \
    readline

# Build install dependencies and cleanup
RUN apk --no-cache add --virtual .build-deps g++ readline-dev git swig python-dev \
    && . /etc/profile \
    && pip install pcaspy \
    && pip install pyzmq \
    && apk del --purge .build-deps

