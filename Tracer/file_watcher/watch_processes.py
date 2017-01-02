from ProcessEntity import ProcessEntity
from watch_user_processes import get_user_process_gen 
from watch_bash_processes import get_bash_process_gen
from threading import Thread
from get_all_processes import list_parent_processes
import time

class ProcessStore:
	def __init__(self):
		self.user_process_gen = get_user_process_gen()
		self.bash_process_gen = get_bash_process_gen()
		self.old_processes = next(self.user_process_gen) | next(self.bash_process_gen)
		self.watched_processes = set()
		self.update_processes()
		self.update_watched_processes()

	def update_processes(self):
		self.processes = next(self.user_process_gen) | next(self.bash_process_gen) - self.old_processes

	def update_watched_processes(self):
		watched_processes = set()
		for proc in self.processes:
			watched_processes = watched_processes | list_parent_processes(proc.pid)
			self.watched_processes = watched_processes

	def get_processes(self):
		return self.processes

	def get_watched_processes(self):
		return self.watched_processes


def get_processes_gen():
	process_store = ProcessStore()

	def process_update_daemon_function():
		while True:
			process_store.update_processes()
			time.sleep(1)

	def watched_process_update_daemon_function():
		while True:
			process_store.update_watched_processes()
			time.sleep(1)

	process_update_daemon = Thread(target=process_update_daemon_function)
	watched_process_update_daemon = Thread(target=watched_process_update_daemon_function)
	process_update_daemon.start()
	watched_process_update_daemon.start()

	while True:
		yield process_store.get_processes(), process_store.get_watched_processes()


def main():
	import time
	process_gen = get_processes_gen()
	while True:
		launched_processes, watched_processes = next(process_gen)
		print watched_processes
		print launched_processes
		print '-'
		time.sleep(0.5)


if __name__ == '__main__':
	main()