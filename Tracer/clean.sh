if [ $1 = "all" ]; then
	rm -rf output/*
	rm -rf raw_data/*
	rm running
	rm stop_screen_recorder
	rm key_stroke_watcher/stop_key_stroke_watcher
	ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
	ps -e | grep python | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
	ps -e | grep applescript | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done

elif [ $1 = "files" ]; then
	rm -rf output/*
	rm -rf raw_data/*
	rm running
	rm stop_screen_recorder
	rm key_stroke_watcher/stop_key_stroke_watcher

elif [ $1 = "data" ]; then
	rm -rf output/*
	rm -rf raw_data/*

elif [ $1 = "meta" ]; then
	rm running
	rm stop_screen_recorder
	rm key_stroke_watcher/stop_key_stroke_watcher

elif [ $1 = "proc" ]; then
	ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
	ps -e | grep python | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
	ps -e |  grep applescript | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done

else
	echo "bash clean.sh [ all | files | data | meta | proc ]"
fi

