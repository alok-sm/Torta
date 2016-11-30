from ProcessEntity import ProcessEntity
from get_all_processes import get_all_processes
import os
import re

def get_bash_processes():
	processes = []
	for process in get_all_processes():
		process_parent = [parent for parent in processes if process.ppid == parent.pid]
		if (process.application == '-bash' or any(process_parent)) and process.application != 'ps':
			processes.append(process)

	return processes


def get_bash_process_gen():
	original_processes = get_bash_processes()
	while True: 
		yield [process for process in get_bash_processes() if process not in original_processes]


def main():
	import time
	process_gen = get_bash_process_gen()
	while True:
		processes = next(process_gen)
		for process in processes: print process
		print '-'
		time.sleep(1)


if __name__ == '__main__':
	main()