from collections import defaultdict
import os
import json


def create_node(name):
    return {
        'text': name, 
        'children': [],
        'state': {
            'opened': True,
            'disabled': False,
            'selected': False
        }
    }

def add_path(node, path):
    parts = path.split('/', 1)
    if len(parts) == 1:
        name = parts[0]

        child_with_name = [child for child in node['children'] if child['text'] == name]
        if not any(child_with_name):
            child = create_node(parts[0])
            if name[0] == '.':
                child['state']['opened'] = False
            node['children'].append(child)

    else:
        name, remaining = parts
        child_with_name = [child for child in node['children'] if child['text'] == name]
        if not any(child_with_name):
            child = create_node(name)
            if name[0] == '.':
                child['state']['opened'] = False
            node['children'].append(child)
        else:
            child = child_with_name[0]
        add_path(child, remaining)

def create_root(paths):
    paths = [path.strip('/') for path in paths]
    root = create_node('/')
    for path in paths:
        add_path(root, path)
    return root

def main():
    data = json.load(open('data.json'))
    data = [item for item in data if 'path' in item.keys()]
    paths = [item['path'] for item in data]

    print json.dumps(create_root(paths), indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
