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

debug = True
# debug = False

number_of_threads = 20
if debug:
	number_of_threads = 1

fd_dict = {}
process_itr = ProcessItr()
stop = False
session_id = sys.argv[1]

class SyncUnbuffered(object):
	def __init__(self, stream):
		self.stream = stream
		self.lock = threading.RLock()
	def write(self, data):
		with self.lock:
			self.stream.write(data)
			self.stream.flush()
	def __getattr__(self, attr):
		return getattr(self.stream, attr)

sys.stdout = SyncUnbuffered(sys.stdout)
sys.stderr = SyncUnbuffered(sys.stderr)

def log(tag, *args):
	if debug:
		print >> sys.stderr, tag,"\t\t", "\t".join([str(obj) for obj in args])

def sync_print(string):
	print string

def normalize_fd(line):
	# log("before normalize_fd", line)
	if line["syscall"] == "open" and line["status"] == "return":
		fd_dict[(line["pid"], line["fd"])] = line

	if line["syscall"] == "close" or line["syscall"] == "write":
		stored_line = fd_dict.get( (line["pid"], line["fd"]), None )
		if stored_line != None:
			line["path"] = stored_line.get("path", None)
			line["cwd"] = stored_line.get("cwd", None)


	if (line.get("path", None) != None) and (not os.path.isabs(line["path"]) and (line.get("cwd", None) != None)):
		line["raw_path"] = line["path"]
		line["path"] = os.path.join(getcwd(line["pid"]), line["path"]) 
	# log("after normalize_fd", line)

def to_be_copied(line):
	syscall_valid = (line["syscall"] == "open" and line["status"] == "entry") or line["syscall"] == "close"
	data_valid = line.get("path", None) != None and os.path.isfile(line["path"])
	return syscall_valid and data_valid
	
def to_be_logged(line):
	if line["syscall"] == "open":
		return line["status"] == "return"

	return True

def to_be_ignored(line, watched_processes):
	file_not_torta_backup = backupfile_regex.match(line.get("path", ""))
	pid_not_in_watched_processes = line["pid"] not in watched_processes
	invalid_fd = line.get("fd", -1) < 0
	from_this_process = os.getpid() == line['pid']
	return file_not_torta_backup or pid_not_in_watched_processes or invalid_fd

def getcwd(pid):
	cwd = subprocess.Popen(
			"lsof -p {} | grep cwd | grep -o \"/.*\"".format(str(pid)), 
			shell=True, 
			stdout=subprocess.PIPE).communicate()[0].strip()

	return None if cwd == "" else cwd

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
			sync_print(json.dumps(line))

		if to_be_copied(line):
			cmd = 'cp "{}" "raw_data/{}/filetrace/{}.{}.torta" &'.format(line["path"], session_id, line["path"].split("/")[-1], line["key"])	
			os.system(cmd)

	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		log("raw_line", raw_line)
		traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

pool = Pool(number_of_threads)

while not stop:
	line = sys.stdin.readline()
	pool.apply_async(handle_line, args=(line,))


# def stop_monitor():
# 	while not os.path.isfile("stop_key_stroke_watcher"):
# 		time.sleep(1)
# 	stop = True
# 	pool.terminate()
# 	os.remove("stop_key_stroke_watcher")
# 	sys.exit()

# threading.Thread(target=stop_monitor).start()