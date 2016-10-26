from ProcessEntity import ProcessEntity
from watch_user_processes import get_user_process_gen 
from watch_bash_processes import get_bash_process_gen


def get_processes_gen():
	user_process_gen = get_user_process_gen()
	bash_process_gen = get_bash_process_gen()
	while True:
		yield next(user_process_gen) + next(bash_process_gen)


def main():
	import time
	process_gen = get_processes_gen()
	while True:
		processes = next(process_gen)
		for process in processes: print process
		print '-'
		# time.sleep(1)


if __name__ == '__main__':
	main()