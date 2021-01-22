#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

pushd ${SCRIPT_DIR}

    if [ $# -eq 0 ]; then
        sudo python3 -m pip install -U turicreate
    else 
        echo "Setting up Turi for the pintools runs"
        # Install for python2
        pip install virtualenv
        virtualenv turienv
        source turienv/bin/activate
        pip install -U llvmlite==0.32.0
        pip install -U turicreate==5.7
        deactivate
    fi

    if [ ! -d "Twitter-dataset" ]; then
        # Twitter dataset has not been installed yet
        # Get dataset
        # We need he ASU Twitter dataset
        # https://archive.org/details/asu_twitter_dataset
        echo "Downloading Twitter dataset"
        wget https://archive.org/download/asu_twitter_dataset/Twitter-dataset.zip
        unzip Twitter-dataset.zip
    fi


popd
