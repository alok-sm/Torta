function prompt() {
osascript <<EOT
	    tell app "System Events"
	      text returned of (display dialog "$1" default answer "" buttons {"OK"} default button 1 with title "$2")
	    end tell
EOT
}

function prompt_password() {
osascript <<EOT
	    tell app "System Events"
	      text returned of (display dialog "$1" default answer "" buttons {"OK"} default button 1 with title "$2" with hidden answer)
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
echo $(prompt "Recording Name (no spaces allowed):" "Torta - Create a new recording" ) > meta/session.txt

# create raw_data folder
mkdir raw_data/$(cat meta/session.txt)
mkdir raw_data/$(cat meta/session.txt)/filetrace

# create output folder
mkdir output/$(cat meta/session.txt)

# print session ID
echo "starting session ID $(cat meta/session.txt)"

pw=$(prompt_password "Root Password:" "Torta - Creating a new recording")

echo $pw | sudo -S bash sudo_start.sh