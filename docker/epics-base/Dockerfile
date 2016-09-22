FROM alpine:latest

# Runtime dependencies
RUN apk --no-cache add \
    libstdc++ \
    tini \
    readline

# Get EPICS source -> Build -> Cleanup
RUN apk --no-cache add --virtual .build-deps cmake git g++ make perl-dev readline-dev \
\
    && mkdir /EPICS \
    && cd /EPICS \
    && wget http://www.aps.anl.gov/epics/download/base/baseR3.14.12.5.tar.gz -O EPICS.tar.gz \
    && tar xzf EPICS.tar.gz \
    && mv base-*/ base/ \
    && rm EPICS.tar.gz \
\
    && cd /EPICS/base \
    && make -j4 CFLAGS="-DIPPORT_USERRESERVED=5000 -fPIC" CXXFLAGS="-DIPPORT_USERRESERVED=5000 -fPIC" \
    && make clean \
\
    && apk del --purge .build-deps

# Copy additional files to image filesystem
COPY copyroot/ /

# Entering via init.sh ensures environment is sourced and passed in command executed via /tini
ENTRYPOINT ["/init.sh"]

