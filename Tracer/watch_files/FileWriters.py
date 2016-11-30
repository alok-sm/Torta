from threading import Lock

class SyncFileWriters:
	def __init__(self):
		self.file_locks = {}

	def write(self, path, data):
		if path not in self.file_locks:
			self.file_locks[path] = Lock()

		with self.file_locks[path]:
			with open(path, "a") as fd:
				fd.write(data)