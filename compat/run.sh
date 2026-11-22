#!/bin/sh
# Inside the compat image: run both suites; exit non-zero if either fails.
set -u
status=0
cd /src/python && /venv/bin/pytest -q -p no:cacheprovider test_examples.py || status=1
cd /src/js && node --test --test-concurrency=1 --test-reporter=dot test.mjs || status=1
exit $status
