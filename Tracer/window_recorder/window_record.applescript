set fileTarget to (do shell script "pwd") & "/stop_window_recorder"
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