on run {command, cwd}
    tell application "Terminal"
        -- set command to "echo hello; sleep 10"
        set filteredWindows to (every window whose name contains "Torta Execution Window")

        if filteredWindows = {} then
            do script "echo -n -e '\\033]0;Torta Execution Window\\007'; clear"
            activate
            delay 1
            set executionWindow to item 1 of (every window whose name contains "Torta Execution Window")
        else
            set executionWindow to item 1 of filteredWindows
            activate executionWindow
            set miniaturized of executionWindow to false
        end if

        
        set miniaturized of (every window whose name does not contain "Torta Execution Window") to true
        do script("cd " & cwd) in first tab of front window
        do script(command) in first tab of front window
    end tell
end run