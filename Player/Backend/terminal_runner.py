import os

def terminal_run(command, cwd, user):
    os.system("osascript windowScripts/runcommand.applescript \"{}\" \"{}\"".format(command, cwd))