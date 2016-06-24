#!/bin/sh
# Launches passed in arguments via /init (https://github.com/krallin/tini)
# It acts as a miniature init system to pass through signals and reap zombies.

# Set up environment
. /etc/profile

# Passed in arguments will run via init
if [ $# -gt 0 ]; then
    CMD="$1"
    shift
else
    # Default to shell if no arguments provided
    CMD="/bin/sh"
fi

# Replace this shell with passed in command and arguments, if available
exec /init -s -g "${CMD}" "$@"

