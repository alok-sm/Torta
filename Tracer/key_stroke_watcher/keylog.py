import subprocess
import signal
import time
import sys
import os
import re

# location of the key log
log_file_path = "/var/log/keystroke.log"

# list of sticky key flags
sticky_flags = {
	"[cmd]": False, 
	"[ctrl]": False, 
	"[option]": False, 
	"[shift]": False,
	"[fn]": False
}

# clear the keylog before starting
os.system("sudo sh -c 'echo > {}'".format(log_file_path))

# start the keylogger exec
subprocess.Popen(["sudo", "./keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

while True:
	time.sleep(1)
	if os.path.isfile("stop"):
		break

# kill keylogger
subprocess.Popen(["sudo", "killall", "keylogger"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# read keylog and get the list of keystrokes
raw_data = open(log_file_path).read().split("\n\n")

# sanity check
if len(raw_data) < 3:
	print "something went wrong while recording..."
	sys.exit()

# tokenize list
keystrokes = re.findall(r"(\[.*?\]|.)", raw_data[2])


for keystroke in keystrokes:
	sticky_key_found = False

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
	if sticky_keys == ["[shift]"] and keystroke.islower():
		print keystroke.upper()
		continue

	# if [fn][f1], convert that to [f1] and remove [fn]
	if re.match(r"\[f\d{1,2}\]", keystroke):
		sticky_keys.remove("[fn]")

	# if sticky keys present, print em out.
	if any(sticky_keys):
		print " ".join(sorted(sticky_keys)),

	# print the non sticky key
	print "({}) {}".format(str(int(time.time())), keystroke)
