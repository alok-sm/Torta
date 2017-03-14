function ask_user_for_sessionid() {
  osascript <<EOT
    tell app "System Events"
      text returned of (display dialog "Session ID" default answer "" buttons {"OK"} default button 1 with title "Torta - Create a new recording")
    end tell
EOT
}

cd $TRACER_PATH

# store current user for applescript
whoami > meta/user.txt

# store tracer path
echo $TRACER_PATH > meta/tracer_path.txt

# touch the "running" file
touch running

# generate session id
echo $(ask_user_for_sessionid) > meta/session.txt

# create raw_data folder
mkdir raw_data/$(cat meta/session.txt)
mkdir raw_data/$(cat meta/session.txt)/filetrace

# create output folder
mkdir output/$(cat meta/session.txt)

# print session ID
echo "starting session ID $(cat meta/session.txt)"

/usr/bin/osascript -e 'do shell script "bash sudo_start.sh" with administrator privileges'