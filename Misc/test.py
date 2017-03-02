from collections import defaultdict
import os
import json


def create_node(name, original=None, leaf=False):
    base = {
        'leaf': leaf,
        'text': name, 
        'state': {
            'opened': name[0] == '.',
            'disabled': False,
            'selected': False
        }
    }

    if leaf:
        base['validate'] = 'none'

        base['syscall'] = {
            'unlink': 'delete',
            'rename': 'rename',
            'open'  : 'write'
        }[original['syscall']]

    else:
        base['children'] = []
    
    return base

def add_path(node, path, original):
    parts = path.split('/', 1)
    leaf = len(parts) == 1
    name = parts[0]
    child_with_name = [child for child in node['children'] if child['text'] == name]
    child = None

    if any(child_with_name):
        if not leaf:
            child = child_with_name[0]
    else:
        child = create_node(name, original, leaf=leaf)
        node['children'].append(child)

    if not leaf:
        add_path(child, parts[1], original)


def create_root(data):
    data = [item for item in data if 'path' in item.keys()]
    for obj in data:
        obj['path'] = obj['path'].strip('/')

    root = create_node('/')
    for obj in data:
        add_path(root, obj['path'], obj)
    return root

def main():
    data = json.load(open('data.json'))
    print json.dumps(create_root(data), indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
