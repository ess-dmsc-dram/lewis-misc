FROM dmscid/epics-base:latest

# Runtime dependencies
RUN apk --no-cache add \
    pcre \
    readline

# Retrieve source for Gateway and dependencies
RUN apk --no-cache add --virtual .temp-deps openssl \
    && cd /EPICS \
    && wget http://www.aps.anl.gov/epics/download/extensions/extensionsTop_20120904.tar.gz -O extensions.tar.gz \
    && tar xzf extensions.tar.gz \
    && rm extensions.tar.gz \
    && cd /EPICS/extensions/src \
    && wget https://github.com/epics-extensions/ca-gateway/archive/R2-0-5-1.tar.gz -O gateway.tar.gz \
    && tar xzf gateway.tar.gz \
    && rm gateway.tar.gz \
    && mv *gateway*/ gateway/ \
    && apk del --purge .temp-deps

# Build and cleanup
RUN apk --no-cache add --virtual .build-deps g++ make perl readline-dev pcre-dev \
    && cd /EPICS/extensions \
    && sed -i -- "s|#USE_PCRE=|USE_PCRE=|" src/gateway/Makefile \
    && make \
    && make clean \
    && apk del --purge .build-deps

# Copy additional files to image filesystem
COPY copyroot/ /

# Use gateway as Entrypoint
ENTRYPOINT ["/init.sh", "gateway", "-access", "/gateway/GATEWAY.access", "-command", "/gateway/GATEWAY.command", "-pvlist", "/gateway/GATEWAY.pvlist"]

