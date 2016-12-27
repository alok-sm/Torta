import sys
import json
import os

session_id = sys.argv[1]

keylog = json.load(open('raw_data/{}/keylog.json'.format(session_id)))

window_positions = [json.loads(line) for line in open('raw_data/{}/window_positions.txt'.format(session_id))]

commands = [json.loads(line) for line in open('raw_data/{}/command_log.txt'.format(session_id))]

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
			'app': start_position['app']
		})

		if item == None:
			continue

		x = item['x']
		y = item['y']
		width = item['width']
		height = item['height']
		app = item['app']	

		current_set = [item]

json.dump({
	"keystrokes": keylog,
	"window_positions": grouped_positions,
	"commands": commands
}, open('output/{}/events.json'.format(session_id), 'w'), sort_keys=True, indent=4)


# for i, position in enumerate(grouped_positions):
# 	cmd = 'ffmpeg -i output/{session_id}/screen_recording.mov -ss {start_time} -t {duration} -filter:v "crop={width}:{height}:{x}:{y}" output/{session_id}/screen_recording.{i}.mp4 -y'.format(
# 		session_id = session_id,
# 		start_time = position['start_time'],
# 		duration = position['duration'],
# 		width = position['width'],
# 		height = position['height'],
# 		x = position['x'],
# 		y = position['y'],
# 		i = i
# 	)
# 	# print cmd
# 	os.system(cmd)
