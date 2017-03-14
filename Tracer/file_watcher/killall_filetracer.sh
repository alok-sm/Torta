#!/bin/bash

ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
printf "done\n"