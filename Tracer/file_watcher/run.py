from ProcessEntity import ProcessEntity
from watch_processes import ProcessItr
from multiprocessing.pool import ThreadPool as Pool

import time
import json
import subprocess
import os
import sys
import traceback
import threading
import re

backupfile_regex = re.compile(r".*\d+\.torta")

# debug = True
show_progress_flag = False

debug = False
# show_progress_flag = True

number_of_threads = 1
if debug:
	number_of_threads = 1

fd_dict = {}
process_itr = ProcessItr()
# filetracer_cmd = ["sudo", "bash", "file_watcher/filetracer.sh"]
stop = False
session_id = sys.argv[1]

# filetracer = subprocess.Popen(
# 	filetracer_cmd, 
# 	stdout=subprocess.PIPE, 
# 	stderr=subprocess.PIPE)

def log(tag, *args):
	if debug:
		print >> sys.stderr, tag, " ".join([str(obj) for obj in args])

def ShowProgressGen():
	i = 0
	symbols = ['|', '/', '-', '\\']

	while True:
		yield symbols[i]
		i = (i + 1) % len(symbols)
		

show_progress_gen = ShowProgressGen()

def show_progress():
	if show_progress_flag:
		print >> sys.stderr, next(show_progress_gen)

def normalize_fd(line):
	if line["syscall"] == "open" and line["status"] == "return":
		fd_dict[(line["pid"], line["fd"])] = line["path"]

	if line["syscall"] == "close" or line["syscall"] == "write":
		line["path"] = fd_dict.get( (line["pid"], line["fd"]), None)

def to_be_copied(line):
	return (line["syscall"] == "open" and line["status"] == "entry") or line["syscall"] == "close"

def to_be_logged(line):
	return (line["syscall"] == "open" and line["status"] == "return") or line["syscall"] == "close" or line["syscall"] == "write"

def to_be_ignored(line, watched_processes):
	file_not_torta_backup = backupfile_regex.match(line.get("path", ""))
	pid_not_in_watched_processes = line["pid"] not in watched_processes
	invalid_fd = line.get("fd", -1) < 0
	from_this_process = os.getpid() == line['pid']
	res = file_not_torta_backup or pid_not_in_watched_processes or invalid_fd

	# if not from_this_process:
	# 	log("\n***\nline=>", line, "\nfile_not_torta_backup =>", file_not_torta_backup, "\npid_not_in_watched_processes =>", pid_not_in_watched_processes, "\ninvalid_fd =>", invalid_fd, "\nfrom_this_process =>", from_this_process, "\n watched_processes =>", watched_processes, "\n****")

	return file_not_torta_backup or pid_not_in_watched_processes or invalid_fd

def handle_line(raw_line):
	try:
		timestamp = int(time.time())

		launched_processes, watched_processes = next(process_itr)

		line = json.loads(raw_line)
		line["timestamp"] = timestamp

		if to_be_ignored(line, watched_processes):
			return

		normalize_fd(line)

		if to_be_logged(line):
			print json.dumps(line)

		if to_be_copied(line):
			if line["path"] == None or not os.path.isfile(line["path"]):
				return

			cmd = 'cp "{}" "raw_data/{}/filetrace/{}.{}.torta" &'.format(line["path"], session_id, line["path"].split("/")[-1], line["key"])	
			os.system(cmd)

	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		log("path", raw_line)
		traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

pool = Pool(number_of_threads)

while not stop:
	# line = filetracer.stdout.readline()
	line = sys.stdin.readline()
	pool.apply_async(handle_line, args=(line,))
	# show_progress()

def stop_monitor():
	while not os.path.isfile("stop_key_stroke_watcher"):
		time.sleep(1)
	stop = True
	pool.terminate()
	os.remove("stop_key_stroke_watcher")
	sys.exit()

threading.Thread(target=stop_monitor).start()
