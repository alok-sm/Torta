from ProcessEntity import ProcessEntity
from psutil import Process
import os

ps_cmd = "ps xao pid,ruid,ppid,command -c"


def get_all_processes():
	return [ ProcessEntity(line) for line in os.popen(ps_cmd).read().split('\n')[1:-1] ]

def list_parent_processes(pid):
	pid = int(pid)
	parents = {pid}

	try:
		proc = Process(pid)
		ppid = proc.ppid()

		while ppid > 0:
			parents.add(ppid)
			proc = Process(ppid)
			ppid = proc.ppid()
	except Exception:
		pass
		
	return parents

def main():
	import sys
	print list_parent_processes(sys.argv[1])

if __name__ == '__main__':
	main()