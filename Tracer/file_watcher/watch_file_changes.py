from threading import Thread
from FileWriters import SyncFileWriters

import subprocess
import re
import os
import sys
import signal

debug = False
debug = True

def is_file(path):
	return not os.path.isdir(path)

def log(msg):
	msg = str(msg).strip()
	if not debug: return
	if msg == '' or msg == None: return
	print msg

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

class FileWatcherThread(Thread):
	def __init__(self, sessionid, pid, syscall, file_writers):
		super(FileWatcherThread, self).__init__()
		self.sessionid = sessionid
		self.pid = pid
		self.syscall = syscall
		self.file_writers = file_writers
		self.cmd = ["sudo", "dtruss", "-f","-t", self.syscall, "-p"] + [self.pid]

		self.basepath = "/Users/alokmysore/watcher/{}/{}/".format(self.sessionid, self.pid)

		self.read_log_path = "{}meta/readlog.txt".format(self.basepath)
		self.write_log_path = "{}meta/writelog.txt".format(self.basepath)

		mkdirs("{}read".format(self.basepath))
		mkdirs("{}write".format(self.basepath))
		mkdirs("{}meta".format(self.basepath))

		self.stop = False

	def run(self):
		pattern = r".*(open_nocancel|open)\(\"(.+?)\", 0x([0-9abcdefABCDEF]+), 0x([0-9abcdefABCDEF]+)\)"

		O_RDONLY = 0
		O_WRONLY = 1
		O_RDWR   = 2 

		dtruss = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		while not self.stop:
			line = dtruss.stderr.readline()

			log(line)

			file_open_params = re.match(pattern, line)
			
			if file_open_params == None:
				# log('line not matched')
				continue

			filepath = get_abs_path(file_open_params.group(2).replace("\\0", ""), self.pid)

			mode = int(file_open_params.group(3), 16)

			if not is_file(filepath):
				continue

			if (mode & O_WRONLY) | (mode & O_RDWR):
				os.system("cp {} {}write/".format(path_encode(filepath), path_encode(self.basepath)))
				self.file_writers.write(self.write_log_path, filepath + "\n")

			else:
				os.system("cp {} {}read/".format(path_encode(filepath), path_encode(self.basepath)))
				self.file_writers.write(self.read_log_path, filepath + "\n")

		try:
			os.killpg(os.getpgid(dtruss.pid), signal.SIGTERM)
		except Exception as e:
			pass
		

		print "stopping"

def get_file_watch_threads(sessionid, pid, file_writers):
	thread_open = FileWatcherThread(sessionid, str(pid), "open", file_writers)
	thread_open_nocancel = FileWatcherThread(sessionid, str(pid), "open_nocancel", file_writers)

	thread_open.start()
	thread_open_nocancel.start()

	return (thread_open, thread_open_nocancel)


if __name__ == '__main__':
	debug = True
	file_writers = SyncFileWriters()
	thread_open, thread_open_nocancel = get_file_watch_threads(sys.argv[1], sys.argv[2],file_writers)
	thread_open.join()
	thread_open_nocancel.join()
