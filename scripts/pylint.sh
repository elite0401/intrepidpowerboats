#!/bin/bash

set -e
DIR=$(dirname "$0")
cd ${DIR}/..

echo "Running pylint"
pylint -f parseable intrepidboats --rcfile=.pylintrc
echo "pylint OK :)"
