from watch_user_processes import get_user_process_gen
from watch_file_changes import get_file_watch_threads
from ProcessEntity import ProcessEntity
from FileWriters import SyncFileWriters
import sys

# new subl comment


def run_file_watcher():
	process_gen = get_user_process_gen()
	prev_processes = []
	file_watchers = []
	file_writers = SyncFileWriters()
	sessionid = sys.argv[1]
	
	while True:
		all_processes = next(process_gen)

		new_processes = [process for process in all_processes if process not in prev_processes]

		for process in new_processes:
			print >> sys.stderr, "[new]", process
			file_watchers += get_file_watch_threads(sessionid, process.pid, file_writers)

		prev_processes = all_processes

if __name__ == '__main__':
	run_file_watcher()
