ps_cmd = "ps xao pid,ruid,ppid,command -c"

def look(x):
	print x
	return x

def eprint(pid, *strings):
	print >> sys.stderr, "[{}]".format(pid), " ".join(strings)