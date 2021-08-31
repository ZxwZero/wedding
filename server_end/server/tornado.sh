#!/bin/bash


run_tornado() {
    python3  /data/app/wedding/server_end/server/main.py -port=8500 >> /data/logs/tornado0.log 2>&1 &
    }
run_tornado