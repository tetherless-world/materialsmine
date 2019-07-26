#!/bin/bash

cd /apps/whyis
python3 manage.py test --ci

if [ ! -f "test-results/py/results.xml" ]; then
    exit 1
fi

cat test-results/py/results.xml

if [ "$(grep -c "failure "test-results/py/results.xml)" -ge 1 ]; then
    exit 1
else
    exit 0
fi
