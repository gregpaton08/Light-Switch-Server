#!/usr/bin/env bash

# get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}/..

venv_dir="venv"
if [ ! -d "$venv_dir" ]; then
    virtualenv venv
    sh ${DIR}/install_rf24.sh

    venv/bin/pip install -r ${DIR}/requirements.txt
fi