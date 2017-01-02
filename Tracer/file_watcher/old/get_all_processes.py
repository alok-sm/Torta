from ProcessEntity import ProcessEntity
from misc import ps_cmd
import os


def get_all_processes():
	return [ ProcessEntity(line) for line in os.popen(ps_cmd).read().split('\n')[1:-1] ]