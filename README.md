
# Widelands AutoKey Macros

Macros for faster building, road laying, and common actions in **Widelands 1.3+** (Linux only).

Tested on Linux Mint 2025 with native AutoKey. Expect to get your hands a little dirty as you'll need to manually set stuff up. I've made comprehensive Guides so it shouldn't be that hard. 

### Quick Start

1. Install required Python packages:
`pip3 install python-xlib pillow mss`
 
2. Copy `widelands` directory(package) to your AutoKey modules folder [Tutorials/Install_Instructions.md](Tutorials/Install_Instructions.md).

3. Set hotkeys in AutoKey, widelands-autokey.zip is supplied, unzip it, put the `Widelands` diretory in your `~/.config/autokey/data/Scripts/` directory. Possibly need to update the keybindings, see [Tutorials/Autokey_GUIDE.md](Tutorials/Autokey_GUIDE.md).

4. **Important**: Personalise your paths and desired **Tribe Selection** that you are playing via the user_config.py file — these settings are tuned to my file system CPU etc. see [Tutorials/user_config.md](Tutorials/user_config.md)

5. GUI edit has been added, in the game, Hotkey `Shift `` ` to access it.

- One-key building placement (hover mouse + Hotkey)
- Road helpers: zigzag, connect, long roads
- Tab switching as a fake Shift Lock key to double potential key uses.
- Dismantle/Destroy/Upgrade Hotkeys
- Visual/audio feedback (unpause-pause, optional sounds)

### Detailed Guides
- [Tutorials/GUIDE.md](Tutorials/GUIDE.md): The Springboard to all the Tutorials.
- [Tutorials/Autokey_GUIDE.md](Tutorials/Autokey_GUIDE.md): All you need to know about the autokey files in the widelands-autokey.zip that you need to install.
- [Tutorials/Building_Roads.md](Tutorials/Building_Roads.md): A guide on how to use the Hotkeys to build roads
- [Tutorials/Developers_Guide.md](Tutorials/Developers_Guide.md) Overview on my code and how you can improve on it.
- [Tutorials/Hotkey_Quick_Guide.md](Tutorials/Hotkey_Quick_Guide.md) As it says.
- [Tutorials/Install_Instructions.md](Tutorials/Install_Instructions.md) As it says
- [Tutorials/Unpause_Pause.md](Tutorials/Unpause_Pause.md): The Pause feedback feature and how to disable if need be.
- [Tutorials/user_config.md](Tutorials/user_config.md): How to customise some settings, what and where they are. Specifically set what tribe you are playing as.

- See Tutorials Directory for [Tutorials](Tutorials/) incase I added files and didn't update this README.md.


### Warnings

- Macros are personal — adjust to your setup
- Only Amazon & Atlantean are fully tuned (others are skeletons)
- Works best in paused game (most actions use unpause-pause feedback)
- No Windows/Mac support planned
- This macro suite requires X11 (not Wayland). At your login screen, choose Cinnamon on Xorg (not Cinnamon on Wayland). I have no intentions of a Wayland upgrade, someone else may fork this and work on it.

Feedback / issues? Post in the [Widelands forum thread](https://www.widelands.org/forum/topic/6574/?page=1).

Enjoy faster Widelands!
