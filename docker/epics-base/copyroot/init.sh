#!/bin/sh
# Launches passed in arguments via /tini (https://github.com/krallin/tini)
# It acts as a miniature init system to pass through signals and reap zombies.
# Usage: . /init.sh [command [arguments]]

# Set up environment
. /etc/profile

# First argument is command to be run via /tini
if [ $# -gt 0 ]; then
    CMD="$1"
    shift
else
    # Default to shell if no arguments provided
    CMD="/bin/sh"
fi

# Replace this shell with passed in command and arguments, if available
exec /tini -s -g -- "${CMD}" "$@"

