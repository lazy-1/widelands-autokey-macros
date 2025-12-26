
# Widelands AutoKey Macros

Macros for faster building, road laying, and common actions in **Widelands 1.3+** (Linux only).

Tested on Linux Mint 2025 with native AutoKey. Expect to get your hands dirty as you'll need to modify the module and work a little on autokey. I've made a comprehensive Guide so it shouldn't be that hard. 

### Quick Start

1. Install required Python packages:
pip3 install python-xlib pyautogui pillow
 
2. Copy `widelands.py` to your AutoKey Module folder (or create a new script and paste the content).

3. Set hotkeys in AutoKey AutoKey_data/Widelands supplied, put it in your autokey/data/Scripts/ directory.

4. **Important**: Personalise coordinates and paths in the file — these are tuned to my screen/resolution 1920x1080.

5. Race selection: Edit `def race()` at the top to match your current game (0=Amazon, 1=Atlantean, etc.).

### Features

- One-key building placement (hover mouse + F-key)
- Road helpers: zigzag, connect, long roads
- Tab switching as a fake Shiftlock key to double potential key uses.
- Dismantle/upgrade shortcuts
- Visual/audio feedback (pause-unpause, optional sounds)

### Detailed Guide

See [GUIDE.md](GUIDE.md) for full shortcut list, toggle keys, debug notes, known limitations, and in-depth explanation.

### Warnings

- Macros are personal — adjust to your setup
- Only Amazon & Atlantean are fully tuned (others are skeletons)
- Works best in paused game (most actions use pause-unpause feedback)
- No Windows/Mac support planned

Feedback / issues? Post in the [Widelands forum thread](link-to-forum-post-if-you-make-one).

Enjoy faster Widelands!
