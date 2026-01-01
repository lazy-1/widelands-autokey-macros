## A Simple? Developers Guide
- coding is not simple. This started out with using autokey native keyboard and mouse events and the frustrating race conditions that autokey natively has. It is not made for fine intergration. So I eventually took a deep dive of X11 and found mss which is 10x better than the eventual pyautogui that I used. So many iterations I could write a book but won't.


### General
- `` ` `` = Development, reloads the widelands module for AutoKey, so module modifications take affect. autokey will not recognise any changes to modules unless you reboot it or use this reload package function.
- Space = Pause game (set via game shortcuts — my personal like) This is unpause_pause() code as well so if you want this feature, then make sure that your using the same 'pause' or 'space' or whatever you have pause set to.
- Tab = Toggles 'tab toggle' Basically gives you double the keys available, acts as a defacto ShiftLock. The game will not accept shift F1 etc without pause issues. But if you want to use 'shift' etc have a try. eg. Amazon with shift-F1 would have a function named `shift_F1` when as a label passed from the autokey script.
  - * = Toggle Show Build sites (NUM PAD * — set via game shortcuts pref — my personal like) This is replacing the 'space' default for Toggle show building. As I set and forget this at start of game. 



## Creating Your Own Functions
- I tried my best to use unused game keys but obviously some of the F keys are used by the game but now my macro is capturing them instead. I was using the 'dot' key as well until my last build where I use the space bar for pause instead. The `.` is no longer used but for those who want to You can use it to build, dismantle, upgrade or other. Pass 'dot' from the autokey script, in the widelands.py call the function `dot()` for compatability. 
- Extra note on `toggle_tab` this can be expanded if the user wants to define 0,1,2 instead of true false. I attached an audio assending sound to toggle on, and an audio decending sound to off so that the user can hit the toggle(tab) key and know the state they just set themselves. There is a lot of potential here but also needless complexity in my opinion. Two states are bad enough as there is no visual 'It is On/Off' 

## I assume you know Python.
If not this is going to be a struggle.

## Editing an existing function, tracing the flow.
- in user_setting.py set USR['race_number'] = 2 and save it. Barbarian
- in user_setting.py set USR['work_path'] = to a valid/creatable path if /dev/shm is not to your liking. Remember the game when playing will constantly write to this path.
- if you want audio feedback set the USR['sound_dir'] to where you saved the Notification directory you downloaded.
- essencial set USR['debug'] = True
- essencial set USR['log_enabled'] = True 
- Open a Widelands game, it is recommended not be in Fullscreen for ease of debug etc.
- Load or create a Barbarian Game. Pause game and 'show buildings' the `space` bar if you have the default in game macros, or whatever you set it to.
- Hit the Hotkey `` ` `` backtick and you should get a 'meep meep' audio that is feedback that the widelands modules have been reloaded. If you have disabled sound, then maybe exit autokey. Open a terminal and launch autokey from there so you can see the print statements.
- Once you know the reload modules works. we go into working building a building.

## Building a Building. 
- Hover mouse over a 'Green'(large) build site.
- Hit F1 once only. Congrats you built a Quarry.
- Now open the USR['work_path'] , in it you will find 4 similar named files.

- 145648_03_Quarry-T-green-4164_RGB018_087_008.png
- 145648_09_tab_selection-F-(93, 50, 40, 7510)-7510_RGB093_050_040.png
- 145648_35_build_selection-F-(72, 58, 42, 2691)-2691_RGB072_058_042.png
- Barbarian_debug.txt

- Opening Barbarian_debug.txt , this is the log `USR['log_enabled']` it will have the three image file names minus the .png. This makes life easy if your not making images but want the information, it is readaly at hand.

## What those images mean.
- I've supplied them in [example_snapshots/](example_snapshots/)
- 145648_03_Quarry-T-green-4164_RGB018_087_008.png
- What is happening. My script (common.py) does a fake mouse click where your mouse was hovering and a dialog pops up as expected. It snapshots the region around where the mouse is now hovering over the `Green` tab in the build Dialog.
- This snapshot is passed through a filter to id if it is a red,orange,green or blue (seafaring) tab.
- follow the script now we are working on barbarian.py in the tribe directory inside the module package `widelands`
- find the `def F1()` funtion. It says btype = 'Quarry', should be Quary so you get to edit my spelling mistake. btype is short for building type.
- next line is build, site = analyze_dialog(btype) , what that does is what I just described above. Take a snapshot of the dialog where the mouse is now (widelands moves the mouse to the tab of the dialog).
- In this case `build` will be `True` and `site` will be `green`.
- update_USR(btype, site): this updates the USR globals USR['building'] and USR['icon'] so I am not forever passing these variables around.

- item_pos = (5, 45) we'll get to that in a second.
- elif site == 'green': I've skipped the others for the moment, this is the `True` condition and it will use the function build_item_L_S(*item_pos) passing the item_pos to that function.
- Now open common.py and search for that function.
  - def build_item_L_S(x_bldg, y_bldg): # Move Large to Small Tab
    - x_tab, y_tab = (-70, 0)
    - build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)




