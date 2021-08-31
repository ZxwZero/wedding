#!/bin/bash


run_tornado() {
    /bin/python3  /home/work/bin/server/main.py -port=8500 >> /home/work/log/tornado0.log 2>&1 &
    }
run_tornado