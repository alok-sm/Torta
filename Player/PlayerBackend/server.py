import os
import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)