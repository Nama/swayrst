#!/usr/bin/python

import os
import sys
import json
import i3ipc
import pickle
from time import sleep

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

PATH = os.path.expanduser('~/.config/sway/workspace_')
workspace_mapping = None
appname = sys.argv[0]

sleep(2)

try:
    command = sys.argv[1]
except IndexError:
    command = None


def notify(headline, text):
    if dunstify:
        dunstify(f'--appname={appname}', headline, text)
    elif notifysend:
        notifysend(headline, text)


def node_getter(nodes):
    if 'app_id' in nodes['nodes'][0].keys():
        return nodes
    return node_getter(nodes['nodes'][0])


if __name__ == '__main__':
    try:
        profile = sys.argv[2]
    except IndexError:
        profile = None

    if not command or not profile:
        notify('Not enough parameters!', 'Exiting')
        print(f'Usage: {sys.argv[0]} <load|save> <profilename>')
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
                    if app['app_id']:
                        # wayland
                        app_class = app['app_id']
                    elif app['window']:
                        # xwayland
                        app_class = app['window_properties']['class']
                    found_apps = tree.find_classed(app_class)
                    if len(found_apps) == 0:
                        # no window of this application
                        # shouldn't happen anymore
                        continue
                    tree_app = found_apps[0]
                    if ws_orientiation == 'horizontal':
                        o = 'h'
                    else:
                        o = 'v'
                    tree_app.command(f'split {o}')
                    tree_app.command(f'move container to workspace {ws_name}')

        # Move workspaces to outputs
        for workspace in workspace_mapping:
            i3.command(f'workspace {workspace.name}')
            i3.command(f'move workspace to output "{workspace.output}"')
        for workspace in filter(lambda w: w.visible, workspace_mapping):
            i3.command(f'workspace {workspace.name}')
        notify('Loaded Workspace Setup', profile)
