#!/usr/bin/env bash

# Donot run this on local,
# this is supposed to be run inside docker

set -e
set -o pipefail

if [ -e "/docker-build.d" ] && ls -d /docker-build.d/*.sh 1> /dev/null 2>&1; then
  for ent_file in /docker-build.d/*.sh; do
    echo Executing $ent_file
    . $ent_file
  done
fi
