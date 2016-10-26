from watch_processes.watch_processes import get_processes_gen
from FileOpenEntity import FileOpenEntity
import subprocess


def get_my_files_open_gen():
	process_gen = get_processes_gen()
	opensnoop = subprocess.Popen(["sudo", "opensnoop"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	for line in opensnoop.stdout:
		file_open = FileOpenEntity(line)
		print file_open
		if file_open.is_valid:
			if any([process for process in next(process_gen) if file_open.pid == process.pid]):
				yield file_open


def main():
	file_open_gen = get_my_files_open_gen()
	while True:
		file_open = next(file_open_gen)
		print file_open


if __name__ == '__main__':
	main()