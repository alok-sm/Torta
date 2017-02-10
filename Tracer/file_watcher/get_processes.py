import subprocess
import psutil
import json

osascript_cmd = '''osascript -e 'tell application "System Events" 
    repeat with proc in (processes where background only is false)
        set pname to name of proc
        log pname
    end repeat
end tell' 2>&1'''


class Application:
    def __init__(self, name, process_trees=None):
        self.name = name
        self.process_trees = [] if process_trees == None else process_trees

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "process_trees": [json.loads(str(proc)) for proc in self.process_trees]
        })


class ProcessTree:
    def __init__(self, pid, children=None):
        self.pid = pid
        self.children = [] if children == None else children

    def get_subtree(self, pid):
        if self.pid == pid:
            return self
        for child in self.children:
            subtree = child.get_subtree
            if subtree is not None:
                return subtree
        return None

    def __contains__(self, pid):
        if self.pid == pid:
            return True
        return any([child.__contains__(pid) for child in self.children])

    def __str__(self):
        return json.dumps({
            "pid": self.pid,
            "children": [json.loads(str(child)) for child in self.children]
        })

def get_psutil_proc(pid):
    try:
        return psutil.Process(pid)
    except Exception as e:
        return None

def run_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return [line.strip() for line in proc.communicate()[0].split('\n')[:-1]]

def create_process_tree(psutil_proc):
    children = []
    for child_pid in psutil_proc.children():
        child_psutil_proc = get_psutil_proc(child_pid)
        if child_psutil_proc == None:
            continue
        children.append(create_process_tree(child_psutil_proc))
    return ProcessTree(psutil_proc.pid, children)

def get_application_from_name(app_name):
    cmd = "ps -A | grep '{}' | awk '{{print $1}}'".format(app_name)
    pids = sorted(map(int, run_cmd(cmd)))[: -2]
    process_trees = []

    for pid in pids:
        psutil_proc = get_psutil_proc(pid)
        
        if psutil_proc == None:
            continue

        if all(pid not in process_tree for process_tree in process_trees):
            process_trees.append(create_process_tree(psutil_proc))
    # print app_name, pids
    return Application(app_name, process_trees), pids


def get_applications():
    app_names = set(run_cmd(osascript_cmd))
    applications_and_processes = [get_application_from_name(app_name) for app_name in app_names]
    applications = []
    watched_process = []
    for app in applications_and_processes:
        applications.append(app[0])
        watched_process.extend(app[1])
    return applications, watched_process



if __name__ == '__main__':
    apps, procs = get_applications()
    print json.dumps([json.loads(str(app)) for app in apps], sort_keys=True, indent=4)

    # print json.dumps(procs, sort_keys=True, indent=4)
