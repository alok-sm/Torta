import os
import pwd
import json
import random
import string
import subprocess

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from fstree import treeify
from terminal_runner import terminal_run

app = Flask(__name__)
CORS(app)



@app.route('/eventlog/<recording_id>', methods=['GET', 'POST'])
def eventlog(recording_id):
    if request.method == 'GET':
        with open('recordings/{}/events.json'.format(recording_id)) as eventlog_file:
            return jsonify(json.load(eventlog_file))
    elif request.method == 'POST':
        with open('recordings/{}/events.json'.format(recording_id), 'w') as eventlog_file:
            eventlog_file.write(json.dumps(request.get_json(), indent=4, sort_keys=True))
            return jsonify({
                'success': True
            })

@app.route('/treeify', methods=['POST'])
def create_tree():
    data = request.get_json()
    # print data
    return jsonify(
        treeify( 
            data.get('files', None), 
            data.get('collapsedDirectories', []) , 
            data.get('editable', False)
        )
    )
    # return jsonify(treeify(data.get('files', None), ['/Users'] ))
    # print data

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    home = data.get('home', '~')
    script = data.get('script', '')
    script_filename = ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.sh'
    script_path = os.path.expandvars(os.path.join(home, script_filename))
    with open(script_path, 'w') as script_file:
        script_file.write(script)
    proc = subprocess.Popen(
        ['bash', script_path],
        cwd=os.path.expandvars(home),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
    res_code = proc.wait()
    os.remove(script_path)

    return jsonify({
        'returncode': res_code,
        'stdout': proc.stdout.read(),
        'stderr': proc.stderr.read()
    })

@app.route('/runcommand', methods=['POST'])
def runcommand():
    data = request.get_json()
    command = data['command']
    cwd = data['cwd']
    user = data.get('user', pwd.getpwuid(os.getuid())[0])
    terminal_run(command, cwd, user)
    return jsonify({
        'status': 'success'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)