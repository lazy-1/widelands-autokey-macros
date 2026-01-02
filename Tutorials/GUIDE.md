# A Guide - Widelands AutoKey Macros

## Background
Back many years ago I worked on an AutoKey script for this game in Solydx. It worked kind of, and was far better than not at all. One key for each build site, i.e. F1 was for red Quarry, F2 was for Orange Quarry etc. My objective was to cut down on the number of mouse clicks that were driving me crazy — love the game but it was wearing out my click finger. Hover Mouse over site and hit the keyboard shortcut and the building is built. This is a far better improvement on that simplistic version with more features.
- This Guide is meant to help you through the hardest parts and show you the way to your own edits. Even if you're new to python it should be simple enough to understand what and why. 

## Environment it was Tested on.
- **Widelands version**: 1.3  
  Run command: `flatpak run org.widelands.Widelands` 
- **OS**: Current upgraded Linux Mint 2025
- **Screen** 1920x1080
- **CPU** i7-13700
- **AutoKey**: Natively installed from repo (v 0.95.10)
- **Note**: This is a Linux setup. If anyone ever wishes to use Microsoft and this stuff, go right ahead — I doubt it will translate directly, but at least the general idea may help.

## Overview
In the end, with the help of Grok, I got a fairly efficient system setup. Unfortunately AutoKey has its quirks and so does the game itself. It would have been so much better if I could have just collected the simplest of info from the running game, but crying about it doesn't help.

## Contents of repo.
- widelands-autokey.zip : this contains the `Widelands` directory that needs to be placed in  ~/.config/autokey/data/Scripts/ directory. If they don't work for you make sure Widelands Window Filter is set to `widelands.widelands` see [Autokey_GUIDE.md](Autokey_GUIDE.md) for details
- Tutorials : Here you will find this GUIDE.md along with other files that should help in getting this to work in your linux system. Along with comprehensive info that should help you modify the code.
- Notification directory: This is all the sounds I use for you to try if you want. Save it somewhere and set the usr['sound_dir'] = '/new/notifications/path', see [user_config.md](user_config.md) for location and how to edit.

## General Shortcuts (set in AutoKey)
[Autokey_GUIDE.md](Autokey_GUIDE.md) I'm using F1 to F12, `[]\;',-/(tab), end and scroll_lock for individual buildings and some functions. The feedback is a quick **unpause-pause**. So you can build during a game pause. This obviously, like all code, can be modified. I've labeled all functions as friendly as possible.

**Keep in mind**: ONLY Amazon and Atlantean have properly defined functioning macros. The other three have not been done — just Python functions have been created for ease of modification when ready and I pasted the code from atlantean.py into those three as a starting place. Anyone keen enough and with a simple understanding of the code can refine those three tribes. Use [Developers_Guide.md](Developers_Guide.md) as a helper.

## Some Helpful Files:
- [Autokey_GUIDE.md](Autokey_GUIDE.md)
- [Building_Roads.md](Building_Roads.md)
- [Developers_Guide.md](Developers_Guide.md)
- [Hotkey_Quick_Guide.md](Hotkey_Quick_Guide.md)
- [Install_Instructions.md](Install_Instructions.md)
- [Unpause_Pause.md](Unpause_Pause.md)
- [user_config.md](user_config.md)
