function prompt_password() {
osascript <<EOT
	    tell app "System Events"
	      text returned of (display dialog "$1" default answer "" buttons {"OK"} default button 1 with title "$2" with hidden answer)
	    end tell
EOT
}

cd $TRACER_PATH/

rm running

pw=$(prompt_password "Root Password:" "Torta - Creating a new recording")
echo $pw | sudo -S bash sudo_end.sh
