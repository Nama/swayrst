# sway-workspaces
Restore workspaces in sway to displays and move applications to saved workspaces.  
Multiple windows of an application/class aren't handled. No idea how to do so.

## Setup
1. Setup displays, e.g. with `wdisplay`
1. Run after setting up your displays `python sway_workspaces.py save <profilename>`
1. Repeat for every display setup
1. Setup kanshi and make it run `python sway_workspaces.py load <profilename>`

## Development
### Used objects in tree
 TODO

### Notes
Had to alter the default tree, so the outputs are not the ports (display name instead of DP-1).
Now it doesn't matter if more ports appeared after docking.
