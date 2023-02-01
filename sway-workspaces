#!/usr/bin/python

import os
import sys
import json
import i3ipc
import pickle
from time import sleep
from difflib import SequenceMatcher

try:
    import sh
except ModuleNotFoundError:
    sh = None
if sh:
    try:
        from sh import dunstify
    except ImportError:
        dunstify = None
        notifysend = sh.Command('notify-send')
else:
    dunstify = None
    notifysend = None

PATH = None
home_folder = os.path.expanduser('~')
try:
    config_folder = os.environ['XDG_CONFIG_HOME']
except KeyError:
    config_folder = home_folder + '/.config/'
paths = [
    home_folder + '.sway/',
    config_folder + 'sway/',
    home_folder + '.i3/',
    config_folder + 'i3/'
]
for path in paths:
    if os.path.isdir(path):
        PATH = path + 'workspace_'
        break

appname = sys.argv[0]
workspace_mapping = None
debug = False
defaulted = []
couldnt_find = []
touched = []

sleep(2)


def notify(headline, text):
    if dunstify:
        dunstify(f'--appname={appname}', headline, text)
    elif notifysend:
        notifysend(headline, text)


def node_getter(nodes):
    if 'app_id' in nodes['nodes'][0].keys():
        return nodes
    return node_getter(nodes['nodes'][0])


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def have_touched(tree_app):
    return tree_app in touched


def touch_app(tree_app):
    if not have_touched(tree_app):
        touched.append(tree_app)


def get_app(tree, app):
    if app.get('app_id'):
        # wayland
        app_class = app['app_id']
    elif app.get('window'):
        # xwayland
        app_class = app.get('window_properties').get('class')
    else:
        return None
    found_apps = tree.find_classed(app_class)
    found_apps = [tree_app for tree_app in found_apps if not have_touched(tree_app)]
    if len(found_apps) == 0:
        return None
    elif len(found_apps) == 1:
        return found_apps[0]
    name = app.get('name')
    for tree_app in found_apps:
        if tree_app.name == name:
            return tree_app
    found_apps.sort(key=lambda tree_app: similar(tree_app.name, name))
    tree_app = found_apps[-1]
    defaulted.append(tree_app)
    return tree_app


if __name__ == '__main__':
    try:
        command = sys.argv[1]
    except IndexError:
        command = None
    try:
        profile = sys.argv[2]
    except IndexError:
        profile = None

    if not command or not profile:
        notify('Not enough parameters!', 'Exiting')
        print(f'Usage: {sys.argv[0]} <load|save> <profilename>')
        sys.exit(1)
    elif not PATH:
        notify('Sway config not found!', 'Make sure to use a default config path (man sway)')
        print(f'Sway config not found! Make sure to use a default config path (man sway)')
        sys.exit(1)

    i3 = i3ipc.Connection()
    tree = i3.get_tree()
    if command == 'save':
        # save current tree
        tree_file = open(f'{PATH}{profile}_tree.json', 'w')
        json.dump(tree.ipc_data, tree_file, indent=4)
        # save workspaces
        profile = sys.argv[2]
        workspaces = i3.get_workspaces()
        outputs = i3.get_outputs()
        for i, ws in enumerate(workspaces):
            for output in outputs:
                if output.name == ws.output:
                    make = output.make
                    model = output.model
                    serial = output.serial
                    output_identifier = f'{make} {model} {serial}'
                    workspaces[i].output = output_identifier
                    break
        pickle.dump(workspaces, open(PATH + profile, 'wb'))
        notify('Saved Workspace Setup', profile)
    elif command == 'load':
        try:
            workspace_mapping = pickle.load(open(PATH + profile, 'rb'))
        except FileNotFoundError:
            workspace_mapping = None
        if not workspace_mapping:
            notify('Can\'t find this mapping', profile)
            sys.exit(1)

        # Move applications to the workspaces
        tree_file = open(f'{PATH}{profile}_tree.json')
        tree_loaded = json.load(tree_file)
        for output in tree_loaded['nodes']:
            if output['name'] == '__i3_scratch':
                continue
            for ws in output['nodes']:
                ws_name = ws['name']
                ws_orientiation = ws['orientation']
                if len(ws['nodes']) == 0:  # empty workspace
                    continue
                apps = node_getter(ws)  # in case of nested workspace, can happen indefinitely
                for app in apps['nodes']:
                    tree_app = get_app(tree, app)
                    if not tree_app:
                        couldnt_find.append(app)
                        continue
                    elif tree_app.workspace().name == ws_name:
                        continue
                    touch_app(tree_app)
                    if ws_orientiation == 'horizontal':
                        o = 'h'
                    else:
                        o = 'v'
                    tree_app.command(f'split {o}')
                    tree_app.command(f'move --no-auto-back-and-forth container to workspace {ws_name}')

        # Move workspaces to outputs
        for workspace in workspace_mapping:
            i3.command(f'workspace {workspace.name}')
            i3.command(f'move workspace to output "{workspace.output}"')
        for workspace in filter(lambda w: w.visible, workspace_mapping):
            i3.command(f'workspace {workspace.name}')
        notify('Loaded Workspace Setup', profile)

        if not debug:
            sys.exit(0)
        if len(defaulted) != 0:
            print(f'chose {len(defaulted)} heuristically')
        total = len(tree.leaves())
        num_touched = len(touched)
        if num_touched != total:
            print(f'left {total - num_touched} untouched')
        if len(couldnt_find) != 0:
            print(f'couldn\'t find {len(couldnt_find)}')
