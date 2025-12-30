
# Widelands AutoKey Macros

Macros for faster building, road laying, and common actions in **Widelands 1.3+** (Linux only).

Tested on Linux Mint 2025 with native AutoKey. Expect to get your hands dirty as you'll need to modify the module and work a little on autokey. I've made  comprehensive Guides so it shouldn't be that hard. 

### Quick Start

1. Install required Python packages:
pip3 install python-xlib pyautogui pillow mss
 
2. Copy `widelands` directory to your AutoKey Module folder.

3. Set hotkeys in AutoKey widelands-autokey.zip supplied, put the unzipped directory  in your autokey/data/Scripts/ directory. Possibly need to update the keybindings, see Tutorials Directory

4. **Important**: Personalise coordinates and paths in the file — these are tuned to my cpu etc.

5. Tribe selection: Edit current_tribe.py and Put the correct number in (help is provided)

### Features

- One-key building placement (hover mouse + F-key)
- Road helpers: zigzag, connect, long roads
- Tab switching as a fake Shiftlock key to double potential key uses.
- Dismantle/upgrade shortcuts
- Visual/audio feedback (pause-unpause, optional sounds)

### Detailed Guide

See Tutorials [GUIDE.md](GUIDE.md) for full shortcut list, toggle keys, debug notes, known limitations, and in-depth explanation.

### Warnings

- Macros are personal — adjust to your setup
- Only Amazon & Atlantean are fully tuned (others are skeletons)
- Works best in paused game (most actions use pause-unpause feedback)
- No Windows/Mac support planned

Feedback / issues? Post in the [Widelands forum thread](link-to-forum-post-if-you-make-one).

Enjoy faster Widelands!
