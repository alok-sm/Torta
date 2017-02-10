from ProcessEntity import ProcessEntity
from watch_user_processes import get_user_process_gen 
from watch_bash_processes import get_bash_process_gen
from threading import Thread
from get_all_processes import list_parent_processes
import time
import psutil
import sys

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
			parent = None
			try:
				parent = psutil.Process(int(proc.pid))
			except Exception as e:
				continue
			children = {parent_proc.pid for parent_proc in parent.children(recursive=True)}

			print >> sys.stderr, children
			print >> sys.stderr, proc.pid
			watched_processes = watched_processes | children
			self.watched_processes = watched_processes

	def get_processes(self):
		return self.processes

	def get_watched_processes(self):
		return self.watched_processes

class ProcessItr:
	def process_update_daemon_function(self):
		while True:
			self.process_store.update_processes()
			time.sleep(0.1)

	def watched_process_update_daemon_function(self):
		while True:
			self.process_store.update_watched_processes()
			time.sleep(0.1)

	def __init__(self):
		self.process_store = ProcessStore()

		self.process_update_daemon = Thread(target=self.process_update_daemon_function)
		self.watched_process_update_daemon = Thread(target=self.watched_process_update_daemon_function)
		self.process_update_daemon.start()
		self.watched_process_update_daemon.start()

	def __iter__(self):
		return self

	def next(self):
		return self.process_store.get_processes(), self.process_store.get_watched_processes()

def main():
	import time
	process_itr = ProcessItr()
	while True:
		launched_processes, watched_processes = next(process_itr)
		print watched_processes
		print launched_processes
		print '-'
		time.sleep(0.5)


if __name__ == '__main__':
	main()