#!/usr/bin/env bash

set -e
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purposes

if [ -e "/docker-entrypoint.d" ] && ls -d /docker-entrypoint.d/*.sh 1> /dev/null 2>&1; then
  for ent_file in /docker-entrypoint.d/*.sh; do
    echo Executing $ent_file
    . $ent_file
  done
fi

exec $@
