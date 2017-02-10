from ProcessEntity import ProcessEntity
from get_all_processes import get_all_processes
import os
import re

def get_bash_processes():
	return {process for process in get_all_processes() if process.application == '-bash'}


def get_bash_process_gen():
	original_processes = get_bash_processes()
	while True: 
		yield {process for process in get_bash_processes() if process not in original_processes}


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
