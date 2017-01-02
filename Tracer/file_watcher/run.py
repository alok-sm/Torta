from ProcessEntity import ProcessEntity
from watch_processes import get_processes_gen

from multiprocessing import Pool

import time
import json
import subprocess
import os
import sys
import traceback
import threading

fd_dict = {}
process_gen = get_processes_gen()
filetracer_cmd = "sudo bash file_watcher/filetracer.sh"
stop = False
session_id = sys.argv[1]

filetracer = subprocess.Popen(
	filetracer_cmd, 
	stdout=subprocess.PIPE, 
	stderr=subprocess.PIPE,
	shell=True)


def normalize_fd(line):
	if line['syscall'] == 'open' and line['status'] == 'return':
		fd_dict[(line['pid'], line['fd'])] = line['path']

	if line['syscall'] == 'close':
		line['path'] = fd_dict.get( (line['pid'], line['fd']), None)

def to_be_copied(line):
	return (line['syscall'] == 'open' and line['status'] == 'entry') or line['syscall'] == 'close'

def to_be_logged(line):
	return (line['syscall'] == 'open' and line['status'] == 'return') or line['syscall'] == 'close' or line['syscall'] == 'write'

def handle_line(raw_line):
	try:
		timestamp = int(time.time())

		launched_processes, watched_processes = next(process_gen)

		line = json.loads(raw_line)
		line['timestamp'] = timestamp

		normalize_fd(line)

		if line['pid'] not in watched_processes:
			return

		if 'fd' in line and line['fd'] < 0:
			return

		if to_be_logged(line):
			print raw_line,

		if to_be_copied(line):
			if line['path'] == None or not os.path.isfile(line['path']):
				return

			cmd = 'cp "{}" "raw_data/{}/filetrace/{}.{}"'.format(line['path'], session_id, line['path'].split('/')[-1], line['key'])
			# print cmd
			os.system(cmd)
			pass

		pass
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		print >> sys.stderr, "path", raw_line
		traceback.print_exception(exc_type, exc_value, exc_traceback,
		                          limit=2, file=sys.stderr)

pool = Pool(5)

for line in filetracer.stdout:
	pool.apply_async(handle_line, args=(line,))
	if stop:
		break

def stop_monitor():
	while not os.path.isfile("stop_key_stroke_watcher"):
		time.sleep(1)
	stop = True
	pool.terminate()
	os.remove("stop_key_stroke_watcher")
	sys.exit()

threading.Thread(target=stop_monitor).start()


