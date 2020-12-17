#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo apt-get update

sudo python3 ${SCRIPT_DIR}/get-pip.py
sudo python ${SCRIPT_DIR}/get-pip.py

# Setup all applications
${SCRIPT_DIR}/../apps/redis/setup.sh
${SCRIPT_DIR}/../apps/metis/setup.sh
${SCRIPT_DIR}/../apps/turi/setup.sh
