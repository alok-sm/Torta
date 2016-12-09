#!/usr/bin/osascript
on run argv
	
	
	set filename to "default"
	
	if (count of argv) > 0 then
		set filename to item 1 of argv
	end if
	
	set filePath to (path to movies folder as string) & filename & ".mov"
	set fileTarget to (do shell script "pwd") & "/stop_screen_recorder"
	
	tell application "QuickTime Player"
		activate
		set newScreenRecording to new screen recording
		delay 1
		tell application "System Events"
			tell process "QuickTime Player"
				set frontmost to true
				key code 49
				do shell script "/usr/local/bin/cliclick c:1,2"
			end tell
		end tell
		
		tell newScreenRecording
			start
			repeat
				delay 1
				try
					POSIX file fileTarget as alias
					do shell script "rm " & fileTarget
					exit repeat
				end try
			end repeat
			stop
		end tell
		
		export document 1 in (file filePath) using settings preset "1080p"
		close document 1 saving no
		
		tell application "QuickTime Player"
			try
				set miniaturized of windows to true -- most apps
			end try
			try
				set collapsed of windows to true -- Finder
			end try
		end tell
	end tell
	
end run