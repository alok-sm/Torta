from ProcessEntity import ProcessEntity
from watch_user_processes import get_user_process_gen 
from watch_bash_processes import get_bash_process_gen
from threading import Thread
import time

class ProcessStore:
	def __init__(self):
		self.user_process_gen = get_user_process_gen()
		self.bash_process_gen = get_bash_process_gen()
		self.update_processes()

	def update_processes(self):
		self.processes = next(self.user_process_gen) + next(self.bash_process_gen)

	def get_processes(self):
		return self.processes


def get_processes_gen():
	process_store = ProcessStore()

	def process_update_daemon_function():
		while True:
			process_store.update_processes()
			time.sleep(1)

	process_update_daemon = Thread(target=process_update_daemon_function)
	process_update_daemon.start()

	while True:
		yield process_store.get_processes()



def main():
	import time
	process_gen = get_processes_gen()
	while True:
		# print len(next(process_gen))
		for process in next(process_gen): print process
		print '-'
		time.sleep(0.5)


if __name__ == '__main__':
	main()