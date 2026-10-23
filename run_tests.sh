#!/bin/sh
# Each test file sets its own env before importing app, so run them in separate processes.
cd "$(dirname "$0")" && P=.venv/bin/python && $P test_app.py | grep -c ^PASS && $P -m pytest -q test_v2.py && $P -m pytest -q test_google.py
