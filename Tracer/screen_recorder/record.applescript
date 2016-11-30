#!/usr/bin/osascript
on run argv
	
	
	set filename to "default"
	
	if (count of argv) > 0 then
		set filename to item 1 of argv
	end if
	
	set filePath to (path to movies folder as string) & filename & ".mov"
	set fileTarget to "stop"
	
	-- do shell script "rm " & fileTarget
	
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
			set break to 0
			repeat until break = 1
				delay 1
				try
					POSIX file fileTarget as alias
					do shell script "rm " & fileTarget
					set break to 1
				end try
			end repeat
			stop
		end tell
		
		export document 1 in (file filePath) using settings preset "720p"
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