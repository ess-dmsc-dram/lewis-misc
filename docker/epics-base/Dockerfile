FROM alpine:latest

# Runtime dependencies
RUN apk --no-cache add \
    libstdc++ \
    readline

# Get EPICS source
RUN mkdir /EPICS \
    && cd /EPICS \
    && wget http://www.aps.anl.gov/epics/download/base/baseR3.14.12.5.tar.gz -O EPICS.tar.gz \
    && tar xzf EPICS.tar.gz \
    && mv base-*/ base/ \
    && rm EPICS.tar.gz

# Build and cleanup (EPICS + tini)
RUN apk --no-cache add --virtual .build-deps cmake bash git g++ make perl-dev readline-dev \
\
    && cd /EPICS/base \
    && make -j4 CFLAGS="-DIPPORT_USERRESERVED=5000 -fPIC" CXXFLAGS="-DIPPORT_USERRESERVED=5000 -fPIC" \
    && make clean \
\
    && cd / \
    && git clone --depth=1 https://github.com/krallin/tini /tini-src \
    && cd /tini-src \
    && cmake . \
    && make \
    && mv tini-static /tini \
    && rm -rf /tini-src \
\
    && apk del --purge .build-deps

# Copy additional files to image filesystem
COPY copyroot/ /

# Entering via init.sh ensures environment is sourced and passed in command executed via /tini
ENTRYPOINT ["/init.sh"]

