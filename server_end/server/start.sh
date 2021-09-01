#!/bin/bash


run_tornado() {
    /root/.pyenv/versions/3.6.8/bin/python3.6  /data/app/wedding/server_end/server/main.py -port=8500 >> /data/logs/tornado0.log 2>&1 &
    }

cd /data/app/wedding
git pull
run_tornado