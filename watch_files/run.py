from watch_user_processes import get_user_process_gen
from watch_file_changes import get_file_watch_threads
from ProcessEntity import ProcessEntity
from FileWriters import SyncFileWriters
import sys

# vim comment


def main():
	process_gen = get_user_process_gen()
	prev_processes = []
	file_watchers = []
	file_writers = SyncFileWriters()

	while True:
		all_processes = next(process_gen)

		new_processes = [process for process in all_processes if process not in prev_processes]

		for process in new_processes:
			# file_watchers[process.pid] = get_file_watch_threads(process.pid)
			print >> sys.stderr, "[new]", process
			file_watchers += get_file_watch_threads(pid, file_writers)

		prev_processes = all_processes

if __name__ == '__main__':
	main()
