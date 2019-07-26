#!/bin/bash

set -e

cd /apps/whyis
python3 manage.py test --ci

if [ "$(grep -c 'failure ' test-results/py/results.xml)" -ge 1 ]; then
    exit 1
else
    exit 0
fi
