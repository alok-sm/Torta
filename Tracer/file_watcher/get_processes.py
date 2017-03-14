import psutil
import json
import time
from misc import run_cmd
from threading import Thread

osascript_cmd = '''osascript -e 'tell application "System Events" 
    repeat with proc in (processes where background only is false)
        set pname to name of proc
        log pname
    end repeat
end tell' 2>&1'''

def get_psutil_proc(pid):
    try:
        return psutil.Process(pid)
    except Exception as e:
        return None

def get_pids_by_app_name(app_name):
    cmd = "ps -A | grep '{}' | awk '{{print $1}}'".format(app_name)
    all_pids = set()
    base_pids = sorted(map(int, run_cmd(cmd)))[: -2]
    for pid in base_pids:
        if pid not in all_pids:
            psutil_proc = get_psutil_proc(pid)
            if psutil_proc is None:
                continue
            all_pids.add(pid)
            all_pids.update([proc.pid for proc in psutil_proc.children(recursive=True)])

    return all_pids

def get_processes():
    apps = {app_name: set() for app_name in run_cmd(osascript_cmd)}
    for proc in psutil.process_iter():
        matched_keys = [key for key in apps.keys() if key.lower() in proc.name().lower()]
        if any(matched_keys):
            key = matched_keys[0]
            if proc.pid not in apps[matched_keys[0]]:
                apps[key].add(proc.pid)
                apps[key].update([child.pid for child in proc.children(recursive=True)])

    processes = {}

    for app, pids in apps.iteritems():
        for pid in pids:
            processes[pid] = app
    
    return processes

class ProcessItr:
    def processes_update_daemon_function(self):
        while True:
            self.processes = get_processes()
            time.sleep(0.5)

    def __init__(self):
        self.processes = get_processes()
        self.processes_update_daemon = Thread(target=self.processes_update_daemon_function)
        self.processes_update_daemon.start()

    def __iter__(self):
        return self

    def next(self):
        return self.processes

if __name__ == '__main__':
    process_iter = ProcessItr()
    for processes in process_iter:
        print processes
        time.sleep(0.1)
