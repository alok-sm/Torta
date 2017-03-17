import sys
import json
import os
import subprocess
import string
import random

ffmpeg_commands = []

chars = string.printable[: 36]
def rand_str(n):
	return "".join([random.choice(chars) for _ in range(n)])

session_id = sys.argv[1]

tracer_path = os.environ['TRACER_PATH']

keylog = json.load(open('raw_data/{}/keylog.json'.format(session_id)))

start_time = int(open('raw_data/{}/start_time.txt'.format(session_id)).readline().strip())
end_time = int(open('raw_data/{}/end_time.txt'.format(session_id)).readline().strip())

window_positions = [json.loads(line) for line in open('raw_data/{}/window_positions.txt'.format(session_id))]

filetrace = [json.loads(line) for line in open('raw_data/{}/filetrace.txt'.format(session_id))]

def format_command_line(line):
	return json.loads(line.replace("\"", "\\\"").replace("####", "\""))

commands = [format_command_line(line) for line in open('raw_data/{}/command_log.txt'.format(session_id))]

grouped_positions = []

first_timestamp = window_positions[0]['timestamp']

x = window_positions[0]['x']
y = window_positions[0]['y']
width = window_positions[0]['width']
height = window_positions[0]['height']
app = window_positions[0]['app']

current_set = [window_positions[0]]

for item in window_positions[1:] + [None]:
	# print item
	if item != None and item['x'] == x and item['y'] == y and item['width'] == width and item['height'] == height and item['app'] == app:
		current_set.append(item)
	else:
		start_position = current_set[0]
		end_position = current_set[-1]

		grouped_positions.append({
			'timestamp': {
				'start': start_position['timestamp'],
				'end': end_position['timestamp']
			},
			'position':{
				'x': start_position['x'],
				'y': start_position['y'],
				'h': start_position['height'],
				'w': start_position['width']
			},
			'app': start_position['app'],
			'screencast': '{}.mp4'.format(rand_str(10))
		})


		if item == None:
			continue

		x = item['x']
		y = item['y']
		width = item['width']
		height = item['height']
		app = item['app']

		current_set = [item]

grouped_positions = grouped_positions[:-1]
		

# json.dump({
# 	"keystrokes": keylog,
# 	"window_positions": grouped_positions,
# 	"commands": commands
# }, open('output/{}/events.json'.format(session_id), 'w'), sort_keys=True, indent=4)

def get_commands(position):
	start = position['timestamp']['start']
	end =   position['timestamp']['end']

	filtered_commands = [{
		'cmd': command['cmd'],
		'collapsedDirectories': [],
		'files': [],
		'host': command['host'],
		'pwd': command['pwd'],
		'screencast':{
			'playbackrate': 1,
			'src': ''
		},
		'summary': '',
		'timestamp': command['timestamp'],
		'user': command['user'],
		'validationScript': '',
		'visibility': 'hide' if command['cmd'] in ['ls', 'pwd', 'date', 'time'] else 'show'
	} for command in commands if start <= command['timestamp'] <= end]

	if len(filtered_commands) > 0:

		for i in list(xrange(len(filtered_commands)))[1: -1]:
			filtered_commands[i]['screencast']['src'] = (filtered_commands[i - 1]['timestamp'], filtered_commands[i + 1]['timestamp'])

		second_time = end if len(filtered_commands) == 1 else filtered_commands[1]['timestamp']
		second_last_time = start if len(filtered_commands) == 1 else filtered_commands[-2]['timestamp']

		filtered_commands[ 0]['screencast']['src'] = (start, second_time)	
		filtered_commands[-1]['screencast']['src'] = (second_last_time, end)

	for command in filtered_commands:
		filename = '{}.mp4'.format(rand_str(10))
		duration = command['screencast']['src'][1] - command['screencast']['src'][0]
		duration = max(duration, 5)
		ffmpeg_commands.append(
			'ffmpeg -i output/{session_id}/screen_recording.mov -ss {start_time} -t {duration} -filter:v "crop={width}:{height}:{x}:{y}" output/{session_id}/{screencast} -y'.format(
				session_id = session_id,
				# start_time = position['timestamp']['start'] - start_time,
				start_time = command['screencast']['src'][0] - start_time,
				# duration = position['timestamp']['end'] - position['timestamp']['start'],
				duration = command['screencast']['src'][1] - command['screencast']['src'][0],
				width = position['position']['w'],
				height = position['position']['h'],
				x = position['position']['x'],
				y = position['position']['y'],
				screencast = filename
			)
		)
		command['screencast']['src'] = filename

	return filtered_commands

def is_parent(directory, file):
	common_path = '/'.join(os.path.commonprefix([directory.rstrip('/').split('/'), file.split('/')]))
	#todo: disable
	# return False
	return common_path == directory

def set_files(positions, k):

	position = positions[k]

	if len(position['commands']) > 0:
		for i in list(xrange(len(position['commands'])))[:-1]:
			position['commands'][i]['files'] = [file for file in filetrace if position['commands'][i]['timestamp'] <= file['timestamp'] < position['commands'][i + 1]['timestamp'] and file.get('app', '').lower() == position['app'].lower() and 'path' in file and os.path.isfile(file['path']) and not is_parent(tracer_path, file['path'])]

		position['commands'][-1]['files'] = [file for file in filetrace if position['commands'][-1]['timestamp'] <= file['timestamp'] < position['timestamp']['end'] and file.get('app', '').lower() == position['app'].lower() and 'path' in file and os.path.isfile(file['path']) and not is_parent(tracer_path, file['path'])]


	# end_timestamp = [pos for pos in positions[i:] if pos['app'] == position['app']]
	# if len(end_timestamp) == 0:
	# 	end_timestamp = positions[i]['timestamp']['end']
	# else:
	# 	end_timestamp = end_timestamp[0]['timestamp']['start']

	
	end_timestamp = positions[k]['timestamp']['end']
	
	if k != len(positions) - 1:
		end_timestamp = positions[k + 1]['timestamp']['end']

	position['files'] = [file for file in filetrace if position['timestamp']['start'] <= file['timestamp'] <= end_timestamp and file.get('app', '').lower() == position['app'].lower() and 'path' in file and os.path.isfile(file['path']) and not is_parent(tracer_path, file['path'])]
	for command in position['commands']:
		position['files'] = [file for file in position['files'] if file not in command['files']]


windows = []

for position in grouped_positions:
	if position['timestamp']['end'] - position['timestamp']['start'] >= 5: 
		visibility = 'show'
	else:
		visibility = 'hide'
	windows.append({
		'app': position['app'],
		'collapsedDirectories': [],
		'commands': get_commands(position),
		'position': position['position'],
		'screencast': {
			'src': position['screencast'],
			'playbackrate': 1
		},
		'summary': '',
		'timestamp': position['timestamp'],
		'validationScript': '',
		'visibility': visibility
	})

for i in xrange(len(windows)):
	set_files(windows, i)

json.dump({
	'windows': windows,
	'projectroot': '$HOME',
	'introduction': ''
}, open('output/{}/events.json'.format(session_id), 'w'), sort_keys=True, indent=4)

for i, position in enumerate(grouped_positions):
	ffmpeg_commands.append(
		'ffmpeg -i output/{session_id}/screen_recording.mov -ss {start_time} -t {duration} -filter:v "crop={width}:{height}:{x}:{y}" output/{session_id}/{screencast} -y'.format(
			session_id = session_id,
			start_time = position['timestamp']['start'] - start_time,
			duration = position['timestamp']['end'] - position['timestamp']['start'],
			width = position['position']['w'],
			height = position['position']['h'],
			x = position['position']['x'],
			y = position['position']['y'],
			screencast = position['screencast']
		)
	)

print "\n".join(ffmpeg_commands)

for ffmpeg_command in ffmpeg_commands:
	os.system(ffmpeg_command)

