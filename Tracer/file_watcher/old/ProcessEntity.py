import re

class ProcessEntity:
	def __init__(self, line):
		self.line = line
		line = re.split(' +', line.strip())
		self.pid = line[0].strip()
		self.uid = line[1].strip()
		self.ppid = line[2].strip()
		self.application = " ".join(line[3:]).strip().lower()

	def __str__(self):
		return "<ProcessEntity   pid={:>5}   application={}>".format(self.pid, self.application)

	def __eq__(self, other): 
		return self.pid == other.pid

	def __hash__(self):
		try:
			return int(self.pid)
		except Exception as e:
			return -1