#!/usr/bin/osascript
on run argv
	set filename to "default"

	repeat
		tell application "System Events"
			set activeApp to name of first application process whose frontmost is true
		end tell

		tell application "System Events" to tell application process activeApp
			try
				set appPosition to position of first window
				set appSize to size of first window
				exit repeat
			end try
		end tell
	end repeat

	
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
				do shell script "screen_recorder/cliclick c:" & (item 1 of appPosition + (item 1 of appSize)/2 as integer) & "," & (item 2 of appPosition + 5)
				do shell script "screen_recorder/cliclick c:" & (item 1 of appPosition + (item 1 of appSize)/2 as integer) & "," & (item 2 of appPosition + 5)
				do shell script "screen_recorder/cliclick c:" & (item 1 of appPosition + (item 1 of appSize)/2 as integer) & "," & (item 2 of appPosition + 5)
			end tell
		end tell
		
		tell newScreenRecording to start

		do shell script "date +%s > raw_data/$(cat meta/session.txt)/start_time.txt"

		repeat
			tell application "System Events"
				set activeApp to name of first application process whose frontmost is true
			end tell

			tell application "System Events" to tell application process activeApp
				try
					set appSize to size of first window
					set appPosition to position of first window

					set output to 			"{ \"x\": " 		& (item 1 of appPosition)
					set output to output & 	", \"y\": " 		& (item 2 of appPosition)
					set output to output & 	", \"width\": " 	& (item 1 of appSize)
					set output to output & 	", \"height\": " 	& (item 2 of appSize)
					set output to output & 	", \"app\": \"" 	& activeApp & "\""
					set output to output & 	", \"timestamp\": " & (do shell script "date +%s") & " }"

					log output
				end try
			end tell


			delay 0.2
			try
				POSIX file fileTarget as alias
				do shell script "rm " & fileTarget
				exit repeat
			end try
		end repeat

		do shell script "date +%s > raw_data/$(cat meta/session.txt)/end_time.txt"

		tell newScreenRecording to stop
		
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