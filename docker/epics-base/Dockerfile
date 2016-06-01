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
    && git clone https://github.com/krallin/tini \
    && cd /tini \
    && cmake . \
    && make \
    && mv tini-static /init \
    && rm -rf /tini \
\
    && apk del --purge .build-deps

# Environment setup
COPY epics.sh /etc/profile.d/epics.sh
COPY init.sh /init.sh

# Force all interactive shells to load profile (this is only for "--entrypoint sh" overrides)
ENV ENV=/etc/profile

# Entering via init.sh ensures environment is sourced and passed in command executed via /init
ENTRYPOINT ["/init.sh"]

