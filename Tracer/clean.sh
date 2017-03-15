rm -rf output/*
rm -rf raw_data/*
rm running
rm stop_screen_recorder
rm key_stroke_watcher/stop_key_stroke_watcher

ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
ps -e | grep python | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
ps -e | grep applescript | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done