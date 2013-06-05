#!/usr/bin/env bash
set -e

cd "$(dirname $0)"

virtualenv --python=python3 --distribute env
source env/bin/activate
pip install -r requirements.txt

ln -sf ~/etc/config.py config.py

release=$(pwd)
cd ~
if [[ -f current ]]; then
    mv -f current previous
fi
ln -s "$release" current

