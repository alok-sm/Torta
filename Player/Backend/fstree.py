from collections import defaultdict
import os
import json

syscall_mapping = {
    'unlink': 'delete',
    'rename': 'rename',
    'open'  : 'write',
    'close' : 'write',
    'write' : 'write'
}

icon_mapping = {
    'unlink': 'glyphicon glyphicon-file color_red',
    'rename': 'glyphicon glyphicon-file color_blue',
    'open'  : 'glyphicon glyphicon-file color_green',
    'close' : 'glyphicon glyphicon-file color_green',
    'write' : 'glyphicon glyphicon-file color_green'
}

def create_node(name, original):
    return {
        'original': original,
        'text': name, 
        'children': [],
        'state': {
            'opened': True,
            'disabled': False,
            'selected': False
        }
    }

def add_path(node, path, original):
    parts = path.split('/', 1)
    if len(parts) == 1:
        name = parts[0]

        child_with_name = [child for child in node['children'] if child['text'] == name]
        if not any(child_with_name):
            child = create_node(name, original)
            node['children'].append(child)

    else:
        name, remaining = parts
        child_with_name = [child for child in node['children'] if child['text'] == name]
        if not any(child_with_name):
            child = create_node(name, original)
            node['children'].append(child)
        else:
            child = child_with_name[0]
        add_path(child, remaining, original)

def clean(node, directories_to_be_collapsed, path_so_far, editable):

    original = node['original']
    del node['original']

    if node['children'] == []:
        node['icon'] = icon_mapping[original['syscall']]
        node['syscall'] = syscall_mapping[original['syscall']]
    else:
        node['icon'] = 'glyphicon glyphicon-folder-open'
        for child in node['children']:
            clean(child, directories_to_be_collapsed, path_so_far + [node['text']], editable)

    full_path = "/".join(path_so_far + [node['text']])
    full_path = "/" if full_path == "" else full_path

    node['data'] = {
        'fullpath': full_path,
        'leaf': node['children'] == []
    }

    if node['data']['leaf']:
        node['state']['disabled'] = original.get('disabled', False)
        if editable:
            if original.get('validateExact', False):
                node['text'] = '[Validate Exact] ' + node['text']
            elif original.get('validate', False):
                node['text'] = '[Validate] ' + node['text']

    if full_path in directories_to_be_collapsed:
        node['state']['opened'] = False

def to_be_pruned(node):
    # print json.dumps(node)
    disabled_leaf = node['data']['leaf'] and node['state']['disabled']
    no_children = not node['data']['leaf'] and node['children'] == []
    # print 'disabled_leaf', disabled_leaf
    # print 'no_children', no_children

    # print disabled_leaf or no_children

    # if disabled_leaf:
    #     print 'leaf ', node['data']['fullpath']
    # if no_children:
    #     print 'empty', node['data']['fullpath']
        # print json.dumps(node)

    return disabled_leaf or no_children

def prune(node):
    if not node['data']['leaf']:
        for child in node['children']:
            prune(child)
        node['children'] = [child for child in node['children'] if not to_be_pruned(child)]

def treeify(files, directories_to_be_collapsed, editable):
    if files == None or files == []:
        return None
    files = [file for file in files if 'path' in file.keys()]
    for obj in files:
        obj['path'] = obj['path'].strip('/')

    root = create_node('', None)
    for obj in files:
        add_path(root, obj['path'], obj)

    clean(root, directories_to_be_collapsed, [], editable)
    root['text'] = "/"

    # print json.dumps(root)

    if not editable:
        prune(root)

    # print json.dumps(root)

    return root



def main():
    data = json.load(open('data.json'))
    print json.dumps(treeify(data), indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
