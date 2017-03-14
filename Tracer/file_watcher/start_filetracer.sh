#!/bin/bash

ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
sudo killall python

sudo file_watcher/filetracer.dtrace | python file_watcher/run.py $1