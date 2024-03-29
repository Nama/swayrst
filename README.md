# swayrst
Called *sway-workspaces* before  
Restore workspaces in sway to displays and move already open windows to their workspaces.  

## Setup
1. Download
    * Either from [AUR](https://aur.archlinux.org/packages/swayrst-git) with `yay -S swayrst-git`
    * Or download from [Actions](https://github.com/Nama/sway-workspaces/actions) or [Releases](https://github.com/Nama/sway-workspaces/releases)
      * `unzip` and `chmod +x` the file
1. Setup displays, e.g. with `swaymsg output ...` or a [GUI tool](https://github.com/swaywm/sway/wiki/Useful-add-ons-for-sway#displayoutputs)
1. Move the windows to your desired workspaces
1. Run `swayrst save <profilename>`
1. Repeat with another `profilename` for every display setup (desk, mobile, work)
1. Run `swayrst load <profilename>` to restore
1. Make [kanshi](https://sr.ht/~emersion/kanshi/) or [shikane](https://gitlab.com/w0lff/shikane) run this command for more automation


## Development
### Used objects in tree
* `output` in `workspace` is replaced with the display name
* The `nodes` list is used. All workspaces are in outputs (displays)
  * Windows are in a list in workspaces
* Windows can be nested indefinitely, so `node_getter()` is used
  * This can happen if the user changes the layout of single windows, hence creates a new container
* Workspace to output mapping are saved separately from the sway tree json
* We get the information about which window is in which workspace from the tree: `i3.get_tree()`, `swaymsg -t get_tree`
* There is no known way (to me) to identify the exact same windows after a reboot (to move multiple windows of the same tool)
  * `window` is only set for Xwayland windows - and is reset after a reboot
  * node IDs reset after a reboot
