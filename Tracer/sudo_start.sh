# check if user is sudo.
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run with sudo" 1>&2
   exit 1
fi

# create results folder
mkdir results/$(cat session.txt)

# start file watcher
# sudo python file_watcher/file_watcher.py $(cat session.txt)

# start screen recorder
su - $(cat user.txt) -c -m "cd $(pwd); osascript screen_recorder/record.applescript" &

# start key logger
cd key_stroke_watcher
sudo python keylog.py > ../results/$(cat ../session.txt)/keylog.txt &
