import subprocess
import signal
import time
import sys
import os
import re
import json

# location of the key log
log_file_path = "/var/log/keystroke.log"

# list of sticky key flags
sticky_flags = {
	"cmd": False, 
	"ctrl": False, 
	"option": False, 
	"shift": False,
	"fn": False
}

# clear the keylog before starting
os.system("sudo rm {}".format(log_file_path))

# start the keylogger exec
subprocess.Popen(["sudo", "./keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

while not os.path.isfile("stop_key_stroke_watcher"):
	time.sleep(1)
		
os.remove("stop_key_stroke_watcher")

# kill keylogger
subprocess.Popen(["sudo", "killall", "keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# read keylog and get the list of keystrokes
raw_data = open(log_file_path).read().split('\n')

output = []

for keystroke in raw_data:
	sticky_key_found = False

	keystroke = keystroke.split('\t')
	if len(keystroke) < 2:
		continue

	line = {}
	line["timestamp"] = int(keystroke[0])

	keystroke = keystroke[1]

	# toggle flags for sticky keys
	for sticky_key in sticky_flags.keys():
		if sticky_key == keystroke:
			sticky_flags[sticky_key] = not sticky_flags[sticky_key]
			sticky_key_found = True
			break

	# skip loop if the key was a sticky key.
	if sticky_key_found:
		continue

	# list all active sticky keys
	sticky_keys = [sticky_key for sticky_key, status in sticky_flags.iteritems() if status]
	
	# if [shift] + a, convert that to A
	if sticky_keys == ["shift"] and keystroke.isalpha() and keystroke.islower():
		keystroke = keystroke.upper()
		sticky_keys = []
		# continue

	# if [fn][f1], convert that to [f1] and remove [fn]
	if re.match(r"\[f\d{1,2}\]", keystroke):
		sticky_keys.remove("fn")
	
	line["keys"] = list(sorted(sticky_keys)) + [keystroke]

	output.append(line)

print json.dumps(output)
