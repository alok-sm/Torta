from watch_user_processes import get_user_process_gen
from watch_file_changes import get_file_watch_thread
from ProcessEntity import ProcessEntity

process_gen = get_user_process_gen()
prev_processes = []
file_watchers = {}

#comment

while True:
	all_processes = next(process_gen)

	new_processes = [process for process in all_processes if process not in prev_processes]

	for process in new_processes:
		file_watchers[process.pid] = get_file_watch_thread(process.pid)
		print "[new]", process

	prev_processes = all_processes


