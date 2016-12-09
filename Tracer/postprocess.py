import sys
import json

session_id = sys.argv[1]

keylog = json.load(open('results/{}/keylog.json'.format(session_id)))

window_positions = [json.loads(line) for line in open('results/{}/window_positions.txt'.format(session_id))]

json.dump({
	"keystrokes": keylog,
	"window_positions": window_positions
}, open('output/{}/events.json'.format(session_id), 'w'))
