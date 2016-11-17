import subprocess
import signal
import time
import sys
import os
import re


log_file_path = "/var/log/keystroke.log"

sticky_flags = {
	"cmd": False, 
	"ctrl": False, 
	"option": False, 
	"shift": False,
	"fn": False
}

os.system("sudo sh -c 'echo > {}'".format(log_file_path))
subprocess.Popen(["sudo", "./keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

raw_input("hit enter to stop\n")

subprocess.Popen(["sudo", "killall", "keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

raw_data = open(log_file_path).read().split("\n\n")

if len(raw_data) < 3:
	print "something went wrong while recording..."
	sys.exit()

raw_data = raw_data[2]

keystrokes = re.findall(r"(\[.*?\]|.)", raw_data)


for keystroke in keystrokes:
	keystroke = keystroke.replace("[", "").replace("]", "").strip()
	sticky_key_found = False
	for sticky_key in sticky_flags.keys():
		if sticky_key in keystroke:
			sticky_flags[sticky_key] = not sticky_flags[sticky_key]
			sticky_key_found = True
			break

	if sticky_key_found:
		continue

	sticky_keys = [sticky_key.strip() for sticky_key, status in sticky_flags.iteritems() if status]
	
	if sticky_keys == ["shift"] and keystroke.islower():
		print keystroke.upper()
		continue

	if re.match(r"f\d{1,2}", keystroke):
		sticky_keys.remove("fn")


	if any(sticky_keys):
		print " ".join(sorted(sticky_keys)),

	print keystroke
