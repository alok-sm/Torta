from threading import Thread
import subprocess
import re
import os
import sys

O_RDONLY = int("0x0000", 16)
O_WRONLY = int("0x0001", 16)
O_RDWR = int("0x0002", 16) 

pattern = "open_nocancel\(\"(.+?)\", 0x([0-9abcdefABCDEF]+), 0x([0-9abcdefABCDEF]+)\)"

#comment 
#another comment

def is_file(path):
	return not os.path.isdir(path)

def mkdirs(path):
	try:
		os.makedirs(path)
	except:
		pass

def path_encode(path):
	return path.replace(" ", "\ ")


def watch_file_opens(pid):

	basepath = "/Users/alokmysore/watcher/{}/".format(pid)

	mkdirs("{}read".format(basepath))
	mkdirs("{}write".format(basepath))
	mkdirs("{}meta".format(basepath))

	read_log = open("{}meta/readlog.txt".format(basepath), "w")
	write_log = open("{}meta/writelog.txt".format(basepath), "w")

	cmd = ["sudo", "dtruss", "-t", "open_nocancel", "-p"] + [pid]

	dtruss = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	while True:
		line = dtruss.stderr.readline()
		file_open_params = re.match(pattern, line)
		
		if file_open_params == None:
			continue

		filepath = file_open_params.group(1).replace("\\0", "")
		mode = int(file_open_params.group(2), 16)

		if not is_file(filepath):
			continue

		if (mode & O_WRONLY) | (mode & O_RDWR):
			os.system("cp {} {}write/".format(path_encode(filepath), path_encode(basepath)))
			write_log.write(filepath + "\n")
			print "write", filepath

		else:
			os.system("cp {} {}read/".format(path_encode(filepath), path_encode(basepath)))
			read_log.write(filepath + "\n")
			print "read", filepath

def get_file_watch_thread(pid):
	thread = Thread(target=watch_file_opens, args=(str(pid), ))
	thread.start()
	return thread


if __name__ == '__main__':
	# thread = get_file_watch_thread("5577")
	watch_file_opens(sys.argv[1])