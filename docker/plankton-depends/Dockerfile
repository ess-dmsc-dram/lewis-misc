FROM dmscid/epics-base:latest

# Install runtime dependencies and cleanup
RUN apk --no-cache add \
    libstdc++ \
    python \
    py-pip \
    readline \
    && find \( -name '*.pyc' -o -name '*.pyo*' \) -exec rm -rf '{}' +

# Install dependencies that require building and cleanup
RUN apk --no-cache add --virtual .build-deps g++ swig readline-dev python-dev \
    && . /etc/profile \
    && pip install pcaspy \
    && pip install pyzmq \
    && rm -rf /root/.cache/pip/* \
    && find \( -name '*.pyc' -o -name '*.pyo*' \) -exec rm -rf '{}' + \
    && apk del --purge .build-deps

