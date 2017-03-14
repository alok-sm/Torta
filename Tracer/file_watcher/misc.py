import subprocess

def run_cmd(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return [line.strip() for line in proc.communicate()[0].split('\n')[:-1]]
