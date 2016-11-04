from ProcessEntity import ProcessEntity
from get_all_processes import get_all_processes
import os
import re

#hello

def filter_app_list(app_list_fd):
	return [path.split('/')[-1].replace('.app', '').lower() for path in app_list_fd.read().split('\n')[:-1]]


def get_applications():
	return filter_app_list(os.popen('find /Applications -iname *.app | grep "/Applications/[a-zA-Z0-9 ]*\.app$"'))


def get_utilities():
	return filter_app_list(os.popen('find /Applications/Utilities -iname *.app | grep "/Applications/Utilities/[a-zA-Z0-9 ]*\.app$"'))


def get_my_processes(apps):
	processes = get_all_processes()
	return [
		process for process in processes
		if process.application in apps or process.application == 'finder' 
	]	


def get_user_process_gen():
	apps = get_applications() + get_utilities()
	original_processes = [process for process in get_my_processes(apps) if process.application != "finder"]
	while True: 
		yield [process for process in get_my_processes(apps) if process not in original_processes]


def main():
	import time
	process_gen = get_user_process_gen()
	while True:
		processes = next(process_gen)
		for process in processes: print process
		print '-'
		time.sleep(1)


if __name__ == '__main__':
	main()