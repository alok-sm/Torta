import re

class FileOpenEntity:
	def __init__(self, line):
		line = line.strip()
		self.is_valid = False
		if line[0].isdigit():
			try:
				parts = re.split(' *', line)
				self.line = line
				self.uid = parts[0].strip()
				self.pid = parts[1].strip()
				self.path = re.search('\/.*$', line).group(0)
				self.is_valid = True
			except:
				pass
			print '-'

	def __str__(self):
		if not self.is_valid:
			return "<FileOpenEntity Invalid/>"
		return "<FileOpenEntity   pid={:>5}   path={}/>".format(self.pid, self.path)