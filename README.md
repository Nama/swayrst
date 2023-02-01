# sway-workspaces
Restore workspaces in sway to displays and move applications to their workspaces.  

## Setup
1. Setup displays, e.g. with `wdisplay`
1. Download from [Actions](https://github.com/Nama/sway-workspaces/actions) or [Releases](https://github.com/Nama/sway-workspaces/releases)
<<<<<<< HEAD
1. `unzip` and `chmod +x` the file
1. Run after setting up your displays `./sway_workspaces save <profilename>`
=======
1. `unzip` the file
1. Run after setting up your displays `sway-workspaces save <profilename>`
>>>>>>> a8cbc09 (Use setup.py scripts option)
1. Repeat for every display setup
1. Setup kanshi and make it run `sway-workspaces load <profilename>`

## Development
### Used objects in tree
* `output` in `workspace` is replaced with the display name
* The `nodes` list is used. All workspaces are in outputs (displays)
  * Windows are in a list in workspaces
* Windows can be nested indefinitely, so `node_getter()` is used
  * This can happen if the user changes the layout of single windows, hence creates a new container
* Workspace to output mapping are saved seperately from the sway tree json
* We get the information about which window is in which workspace from the tree: `i3.get_tree()`, `swaymsg -t get_tree`

### Notes
Had to alter the default tree, so the outputs are not the ports (display name instead of DP-1).
Now it doesn't matter if more ports appear after docking.
