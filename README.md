
# Widelands AutoKey Macros

Macros for faster building, road laying, and common actions in **Widelands 1.3+** (Linux only).

Tested on Linux Mint 2025 with native AutoKey. Expect to get your hands dirty as you'll need to modify the module and work a little on autokey. I've made  comprehensive Guides so it shouldn't be that hard. 

### Quick Start

1. Install required Python packages:
pip3 install python-xlib pyautogui pillow mss
 
2. Copy `widelands` directory(package) to your AutoKey Module folder.

3. Set hotkeys in AutoKey widelands-autokey.zip supplied, put the unzipped directory `widelands` in your autokey/data/Scripts/ directory. Possibly need to update the keybindings, see [Tutorials](Tutorials/) Directory

4. **Important**: Personalise coordinates and paths in the user_settings.py file — these are tuned to my file system cpu etc [user_settings.md](Tutorials/user_settings.md)

5. Tribe selection: You will have to tell the Package which Tribe you are playing as in order to get the best out of the functions as each tribe has a different tailored module. This is done in the  user_settings.py module near the top, In the function  load_USR_defaults(). It is heavilly commented for user convenience or see [user_settings.md](Tutorials/user_settings.md) for a comprehensive guide.

### Features

- One-key building placement (hover mouse + Hotkey)
- Road helpers: zigzag, connect, long roads
- Tab switching as a fake Shiftlock key to double potential key uses.
- Dismantle/Destroy/Upgrade Hotkeys
- Visual/audio feedback (pause-unpause, optional sounds)

### Detailed Guides
- [Tutorials/GUIDE.md](Tutorials/GUIDE.md): The Springboard to all the Tutorials.
- [Tutorials/Autokey_GUIDE.md](Tutorials/Autokey_GUIDE.md): All you need to know about the autokey files in the widelands-autokey.zip that you need to install.
- [Tutorials/Building_Roads.md](Tutorials/Building_Roads.md): A guide on how to use the Hotkeys to build roads
- [Tutorials/Developers_Guide.md](Tutorials/Developers_Guide.md) Overview on my code and how you can improve on it.
- [Tutorials/Hotkey_Quick_Guide.md](Tutorials/Hotkey_Quick_Guide.md) As it says.
- [Tutorials/Install_Instructions.md](Tutorials/Install_Instructions.md) As it says
- [Tutorials/Pause_Unpause.md](Tutorials/Pause_Unpause.md): The Pause feedback feature and how to disable if need be.
- [Tutorials/user_settings.md](Tutorials/user_settings.md): How to customise some settings, what and where they are. Specifically set what tribe you are playing as.

- See Tutorials Directory for [Tutorials](Tutorials/) incase I added files and didn't update this README.md.


### Warnings

- Macros are personal — adjust to your setup
- Only Amazon & Atlantean are fully tuned (others are skeletons)
- Works best in paused game (most actions use unpause-pause feedback)
- No Windows/Mac support planned
- "This macro suite requires X11 (not Wayland). At login screen choose Cinnamon on Xorg (not Cinnamon on Wayland). I have no intentions of a Wayland upgrade, someone else my fork this and work on it.

Feedback / issues? Post in the [Widelands forum thread](link-to-forum-post-if-you-make-one).

Enjoy faster Widelands!
