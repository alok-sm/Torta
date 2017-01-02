# from watch_user_processes import get_user_process_gen
from watch_processes import get_processes_gen
from watch_file_changes import get_file_watch_threads
from ProcessEntity import ProcessEntity
from FileWriters import SyncFileWriters
from time import sleep
import sys
import os

def run_file_watcher():
	process_gen = get_processes_gen()
	prev_processes = []
	file_watchers = []
	file_writers = SyncFileWriters()
	sessionid = sys.argv[1]
	tracer_path = sys.argv[2]
	
	while not os.path.isfile("stop_file_watcher"):
		sleep(1)
		all_processes = next(process_gen)

		new_processes = [process for process in all_processes if process not in prev_processes]

		for process in new_processes:
			print >> sys.stderr, "[new]", process
			file_watchers += get_file_watch_threads(sessionid, process.pid, tracer_path, file_writers)

		prev_processes = all_processes

	os.remove("stop_file_watcher")

	print "1"

	for thread in file_watchers:
		thread.stop = True

	print "2"

	for thread in file_watchers:
		thread.join()

	print "3"

if __name__ == '__main__':
	run_file_watcher()
