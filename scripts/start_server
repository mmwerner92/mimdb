#!/bin/bash

cd /
pip install -r requirements.txt
nohup uwsgi --http :80 --module evaly.wsgi > /dev/null 2>&1 &