#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=36000'

init_host() {
  sudo apt-get update
  sudo apt-get -yq install libnuma-dev numactl build-essential  \
                       python3 python3-pip python3-matplotlib \
                       python3-numpy git wget libevent-dev 
}

init_host
sudo python3 ${SCRIPT_DIR}/get-pip.py
sudo python ${SCRIPT_DIR}/get-pip.py

# Setup all applications
${SCRIPT_DIR}/../redis/setup.sh
${SCRIPT_DIR}/../metis/setup.sh
${SCRIPT_DIR}/../turi/setup.sh
