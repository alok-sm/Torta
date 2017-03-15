function prompt() {
osascript <<EOT
	    tell app "System Events"
	      text returned of (display dialog "$1" default answer "" buttons {"OK"} default button 1 with title "$2")
	    end tell
EOT
}

cd $TRACER_PATH/

rm running

# /usr/bin/osascript -e 'do shell script "bash sudo_end.sh" with administrator privileges'
# /usr/bin/osascript -e 'do shell script "bash sudo_end.sh" with administrator privileges'

pw=$(prompt "root password:" "Torta - Creating a new recording")
echo $pw | sudo -S bash sudo_end.sh





# sleep 20
# echo "after sleep"
# reset
# bash -c "python postprocess.py $(cat meta/session.txt)"

# stop file watcher
# ps -e | grep dtrace | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
# ps -e | grep python | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done
# ps -e | grep applescript | awk '{print $1}' | while read CMD; do sudo kill -9 $CMD; done