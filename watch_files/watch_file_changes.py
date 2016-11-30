from threading import Thread
from FileWriters import SyncFileWriters

import subprocess
import re
import os
import sys

O_RDONLY = 0
O_WRONLY = 1
O_RDWR   = 2 

#comment2

pattern = r"(open_nocancel|open)\(\"(.+?)\", 0x([0-9abcdefABCDEF]+), 0x([0-9abcdefABCDEF]+)\)"

def is_file(path):
	return not os.path.isdir(path)

def mkdirs(path):
	try:
		os.makedirs(path)
	except:
		pass

def path_encode(path):
	return path.replace(" ", "\ ")

def get_abs_path(path, pid):
	if os.path.isabs(path):
		return path

	cmd = "lsof -p {} | grep cwd".format(pid)
	lsof = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

	output = lsof.stdout.read().split('\n')[0]
	cwd = re.findall("\/.*$", output)[0]

	return os.path.join(cwd, path)

def watch_file_opens(pid, syscall, file_writers):
	# print "starting thread for", syscall
	basepath = "/Users/alokmysore/watcher/{}/".format(pid)

	read_log_path = "{}meta/readlog.txt".format(basepath)
	write_log_path = "{}meta/writelog.txt".format(basepath)

	mkdirs("{}read".format(basepath))
	mkdirs("{}write".format(basepath))
	mkdirs("{}meta".format(basepath))

	cmd = ["sudo", "dtruss", "-t", syscall, "-p"] + [pid] 

	dtruss = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	while True:
		line = dtruss.stderr.readline()
		file_open_params = re.match(pattern, line)
		
		if file_open_params == None:
			continue

		filepath = get_abs_path(file_open_params.group(2).replace("\\0", ""), pid)

		mode = int(file_open_params.group(3), 16)

		if not is_file(filepath):
			continue

		if (mode & O_WRONLY) | (mode & O_RDWR):
			os.system("cp {} {}write/".format(path_encode(filepath), path_encode(basepath)))
			file_writers.write(write_log_path, filepath + "\n")

		else:
			os.system("cp {} {}read/".format(path_encode(filepath), path_encode(basepath)))
			file_writers.write(read_log_path, filepath + "\n")

def get_file_watch_threads(pid, file_writers):
	thread_open = Thread(target=watch_file_opens, args=(str(pid), "open", file_writers))
	thread_open_nocancel = Thread(target=watch_file_opens, args=(str(pid), "open_nocancel", file_writers))

	thread_open.start()
	thread_open_nocancel.start()

	return (thread_open, thread_open_nocancel)


if __name__ == '__main__':
	file_writers = SyncFileWriters()
	thread_open, thread_open_nocancel = get_file_watch_threads(sys.argv[1], file_writers)
	thread_open.join()
	thread_open_nocancel.join()
