# Detailed Guide - Widelands AutoKey Macros

## Background
Back many years ago I worked on an AutoKey script for this game in Solydx. It worked kind of, and was far better than not at all. One key for each build site, i.e. F1 was for red Quarry, F2 was for Orange Quarry. My objective was to cut down on the number of mouse clicks that were driving me crazy — love the game but it was wearing out my click finger. Hover Mouse over site and hit the keyboard shortcut and the building is built. This is a far better improvement on that simplistic version with more features.
- This Guide is meant to help you through the hardest parts and show you the way to your own edits. Even if your new to python it should be simple enough to understand what and why. 

## Environment it was Tested on.
- **Widelands version**: 1.3  
  Run command: `flatpak run org.widelands.Widelands` 
- **OS**: Current upgraded Linux Mint 2025
- **Screen** 1920x1080
- **AutoKey**: Natively installed from repo (v 0.95.10)
- **Note**: This is a Linux setup. If anyone ever wishes to use Microsoft and this stuff, go right ahead — I doubt it will translate directly, but at least the general idea may help.

## Overview
In the end, with the help of Grok, I got a fairly efficient system setup. Unfortunately AutoKey has its quirks and so does the game itself. It would have been so much better if I could have just collected the simplest of info from the game, but crying about it doesn't help.

## Contents of repo.
- AutoKey_data : this is the contents of my autokey/data/Scripts/Widelands/ directory. If they don't work for you make sure Widelands Window Filter is set to widelands.widelands, this is done by clicking `set` and then on the widelands window. 
- AutoKey_data individual files : fore each in autokey select them and click `Hotkey`, then define it by clicking `set` in the dialog and then press the actual keyboard key such as F1. make sure you save. This is not a tutorial on autokey, passed this do your own research if your stumped, tell grok it'll help.
- Notification directory: This is all the sounds I use for you to try if you want. Save it somewhere and set the NOTIFICATIONS_DIR = '/new/notifications/path'. I have it as the dir above the current module directory and then into Sounds blah blah.

## General Shortcuts (set in AutoKey)
I'm using F1 to F12, `[]\;',-/(tab), end and scroll_lock for individual buildings and some functions. The feedback is a quick **pause-unpause**. So you can build during a game pause. This obviously, like all code, can be modified. I've labeled all functions as friendly as possible.

**Keep in mind**: ONLY Amazon and Atlantean have functioning macros. The other three have not been done — just Python functions have been created for ease of modification when ready.

## Some Important Notes

The **detect icon under the mouse** only works on clean icons, not ones under trees or such, so it is limited by that. In general however: hover mouse over build icon and it will figure if it is **Red**, **Orange** or **Green**. From there it will build whatever that 'key' is associated with. Since this was originally created when I was obsessed with Atlantean, it has a good setup for it — example: hover over a build icon and hit F1 it will build a Quarry. F2 builds a woodcutter etc. Since this version was designed using Amazon there are more functions for them.

## The Module Itself

- `DEBUG = False`  
  If this is `True` it will be very slow as it is writing images to your 'temp' dir. Be patient this is for getting things honed in, not for game play.
- In this game I use `/dev/shm/` (WORK_PATH). Your choice — I have an SSD.
- `WORK_PATH` is a **Must**! It is not only for debugging — it is also where the module saves its transient info on whether you are selecting the first flag of a road or is this your second (destination) selection. `;'/` are my most common used keys and if you use AutoKey's remember state, it writes it to the user's disk which is not healthy for SSD as there are literally thousands of read/writes involved with this system.
- `def race()`: Here you manually select which race you are playing. Just change the number in `num = `.
- `debug_save_shm_append(text)`: is Always on. If you want to stop this, obviously 'return' the function before the write.
- `stable_click` and `stable_click_relative` use Xlib, as AutoKey was constantly giving me race conditions resulting in very flaky functions.
- `NOTIFICATIONS_DIR` and `PLAY_SOUND` are yours to play with — if you want audio feedback. If not, disable  `_play_sound()` with a return. I've uploaded my sounds in the `Notification`
- `def detect_icon_type`: Here we have the core of defining what build site is under the mouse. It uses `pyautogui.screenshot` to take a snapshot of what is under the mouse. Runs a colour comparison on it and determines what 'colour' the icon is. This is a new innovation and has **only** been tested on a green background, no desert or anything else. So how it works in Desert games or other terrain? Trying to determine 'shape' instead of colour was useless as far as I could see — too many issues...
- `transient_store_get` and `set` are the essentials for road build and my 'tab' toggle. Where it acts as a kind of 'shift lock' because the actual use of shift or ctrl on F keys ended up messing the pause-unpause which I find essential for feedback as most of my 'creating' is done in pause mode.
- `ctrl_press()` and `release` are Xlib direct functions because AutoKey is not made for precise work. It constantly had race conditions that would sometimes have ctrl held and others not — it was maddening. It works now...
- `_save_snapshot`: this is for creation and debug only. Turn DEBUG on and it will save the images in the WORK_PATH so you can see where the 'click' was made. Extremely slow but great for getting things setup.
- `build_item` and `build_item_tab_change` are relatively self-explanatory. If you are opening on the tab you want then it is `build_item`, if you need to tab to a different build size then it is `tab_change`.
- `def err_no_col()`: **SPECIAL NOTE!!!!!** this is MY personal feedback system. Here you will have to modify the script to `print(stuff)` or whatever you want to use.
- `in_building_dialog`: Actions on building dialogs, e.g. Amazon Woodcutter upgrade the building to Rare Tree Cutter. Or Dismantle with ctrl held. This can be very dangerous if you don't pay attention.
- `call_shortcut()`: is the main engine for sending to 'race' defined functions. If 'Amazon' is selected in `race()` then a call to this with "Shortcut" key e.g. if the AutoKey is F1 `widelands.call_shortcut('F1',keyboard)`, then it will call `Amazon_F1`. If race is "1" which is Atlantean then function will be `Atlantean_F1` — all logical.

## Creating Your Own Functions
- I tried my best to use unused game keys but obviously some of the F keys are used by the game but now my macro is capturing them instead. I was using the 'dot' key as well until my last build where I use the space bar for pause instead. The `.` is no longer used but for those who want to You can use it to build, dismantle, upgrade or other. Pass 'dot' from the autokey script, in the widelands.py call it Amazon_dot and Atlantean_dot etc and you have a new function, it can be Two functions in one if you use toggle_tab. 
- Extra note on `toggle_tab` this can be expanded if the user wants to define 0,1,2 instead of true false. I attached an audio assending sound to toggle on, and an audio decending sound to off so that the user can hit the toggle(tab) key and know the state they just set themselves. There is a lot of potential here but also needless complexity in my opinion. Two states are bad enough as there is no visual 'It is On/Off' 

## Keyboard Shortcuts

### Development & General
- `` ` `` = Development, reloads the widelands module for AutoKey, so module modifications take affect.
- Space = Pause game (set via game shortcuts — my personal like) This is unpause_pause() code as well so if you want this feature, then make sure that your using the same 'pause' or 'space' or whatever you have pause set to.
- Tab = Toggles 'tab toggle' Basically gives you double the keys available, acts as a defacto ShiftLock. The game will not accept shift F1 etc without issues. But if you want to use 'shift' etc have a try. eg. Amazon with shift-F1 would have a function named Amazon_shift_F1 when as a label passed from the autokey script. Be aware feedback is confused as the hold of shift interfears with the autokey send of 'pause'..
  Sound Down = False (default state on startup)  
  Sound Up = True, for keys defined with Tab Toggle sets different task
- * = Toggle Show Build sites (NUM PAD * — set via game shortcuts pref — my personal like) This is replacing the 'space' default for Toggle show building. As I set and forget this at start of game. 

### Road Building
- ; = Hover on the 'flag', then press the key, then move the mouse to the end location 'flag' where you want the road to end. Hit the key again. It will flag all the road. Clicking the mouse after the first keyboard hit will tell you how many spaces. When you are hovering over the exact spot you want and hit key it will build the road to there.
- ' = Build long road, connecting, begin on flagged road, end on flagged road. Hover mouse over begin flagged road, hit the key then move mouse to the flagged road you want to 'join', hit the key again. This will join the two with optimum flags.
- / = Build single road, joining parallel roads zigzag. Optimum for 2 space joining of roads. Must start and end on an already flagged road flag. If the distance is more than 2 spaces it will **not** put flags in the road you are creating.

### Amazon
**Tab toggle Down (normal, false, default state)**  
- end = Stone_Workshop  
- - = Patrol_Post  
- = = Tower  
- np_add(+) = Liana_Cutter  

**Tab toggle Up (true)**  
- end = Furnace "GOLD"  
- - = Upgrades 'currently' Building Woodcutter to Rare  
- = = Warriors_Dwelling  
- np_add(+) = Rope_Weaver  

**F-keys**  
F1 = Stonecutter  
F2 = Woodcutter (toggle_tab: remove worker)  
F3 = Jungle_Preserver (toggle_tab: remove worker)  
F4 = Water_Gatherer  
F5 = Cassava_Root_Cooker (Bread)  
F6 = Chocolate_Brewery  
F7 = Charcoal_Kiln (toggle_tab: infinite coal)  
F8 = Food_Preserver  
F9 = DressMakery  
F10 = Rare_Tree_Plantation (toggle_tab: infinite Rare/StoneMine)  
F11 = Hunter_Gatherer  
F12 = Wilderness_Keeper (inner radii is for fish)

**Other**  
[ = Double Click (Delete road under mouse, clean up foresters area)  
] = Dismantles Stonecutter, UPGRADES BUILT woodcutter  
\ = Dismantles Patrol, Tower and Fortress  
scroll_lock = Dismantles Woodcutter

### Atlantean
F1 = Quarry  
F2 = Woodcutter  
F3 = Forester  
F4 = Well  
F5 = Bakery  
F6 = Smokery  
F7 = Mill  
F8 = Smelter  
F9 = Weaponsmith  
F10 = Armoursmith  
F11 = Fish  
F12 = Fish Breader  

end = SawMill  
- = Guardhouse  
= = Tower  

] = Dismantle StoneCutter/Woodcutter  
\ = Dismantle Tower Guardhouse

### Barbarian / Empire / Frisian
(These are placeholders — functions created but not yet tuned. Edit `btype` and `item_pos` as needed.)

## General Gameplay Shortcuts (from Widelands — may be wrong/outdated)
Space: Toggle the build icons.  
C: Toggle census display (shows information about buildings and workers).  
S: Toggle statistics display (e.g., resource or economy stats).  
B: Toggle building window (for placing or managing buildings).  
M: Show/hide the minimap.  
P: Open the objectives window.  
W: Open the wares window (to manage resources).  
T: Open the transport window (to manage economy and logistics).  
G: Go to the selected location (centers the view on a specific point).  
H: Go to the headquarters or starting position.  
Ctrl + S: Save the game.  
Ctrl + L: Load a saved game.  
Ctrl + Enter: Immediately leave the game (suggested in development discussions, may not be fully implemented in all versions).  
+/-: Adjust game speed (increase or decrease).  
Home: Center the view on the starting position or headquarters.  
Arrow Keys: Scroll the map.  
Ctrl + Arrow Keys: Scroll the map faster.

## Map Editor Shortcuts
N: Create a new map.  
Shift + [Tool Key]: Modify editor tools (e.g., terrain editing, placing objects). Specific tool shortcuts may vary, but recent updates unified tools to use Shift as a modifier.  
Z: Zoom in.  
Shift + Z: Zoom out (or minimal/maximal zoom in some versions).  
Ctrl + S: Save the map.  
Ctrl + L: Load a map.

## Additional Shortcuts
Esc: Bring up the main menu or cancel an action. In some contexts, it opens the "are you sure" dialog for exiting.  
Ctrl + F: Toggle full-screen mode.  
Ctrl + F10: Take a screenshot.  
I: Open the inventory window (for managing wares at a specific building).  
O: Open the objectives menu (alternative to P in some cases).  
R: Toggle road-building mode.  
D: Destroy/remove a selected building or road.  
E: Toggle the economy window.  
F: Toggle fog of war visibility (in scenarios or multiplayer where applicable).
