#!/bin/sh

poetry run python initdb.py solveme.py && rm initdb.py
gunicorn -b '0.0.0.0:8001' -w 4 -k gevent app:app