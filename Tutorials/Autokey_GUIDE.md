## An Autokey specific guide 
- This is Not an Autokey comprehensive guide, it is a general help for implementing the Widelands specific functions needed for using the widelands package.

## Overview
- It is assumed you followed the [Install_Instructions.md](Install_Instructions.md) Before reading this. If not check it out first.
- Technically that is all that is needed. But when is anything easy in this world...

## First Time Autokey Run.
- Open autokey and see 'Scripts', left side, it's a directory structure like a file browser. If you successfully moved the Widelands into the directory it should be seen inside the Scripts tree. If not check the path etc.
- Now click on the Widelands fold in the Scripts directory. On the right side there should be three `set` options. Abbreviations:, Hotkey: and Window Filter:
- Window Filter should state `widelands.widelands`. If this is not so, then make sure widelands is running , not full screen mode for this unless you have more than one monitor. Click the set button next to window filter and it will give you a dialog , click "Detect Window Properties" and then click on the game window.  This should set the Window Filter to the "widelands.widelands' window. This is an autokey essential so it knows these macros are for the widelands game ONLY!

## Individual autokey scripts.
- You will find the following scripts inside the Widelands directory:

- 00-Reload_module
- 00-Test_script
- 00-Toggle_tab
- Build-long-road-1-New
- Build-long-road-2-Connect
- Build-road-3-zigzag
- Building_end_Sawmill1
- Building_equal_Tower
- Building_F01_Stone
- Building_F02_Woodcutter
- Building_F03_Forester
- Building_F04_Well
- Building_F05_Baker
- Building_F06_Smoke
- Building_F07_Mill
- Building_F08_Smelt
- Building_F09_Weaponsmith
- Building_F10_Armoursmith
- Building_F11_Fish
- Building_F12_Breader
- Building_hyphen_Guardhouse
- Building_plus_Liana_cutter
- Destroy_Something
- Dismantle_Something
- Double_Click
- Pause
- Upgrade_Something
- z-space-building-show


## What to do with them.
- Technically there should be no problems but incase the hotkey was lost the script themselves have comments and tell you `#key = # "keyname"` and most have file names that tell you what the hotkey is.
- example: Building_F01_Stone #key = # F1 (click on Building_F01_Stone and see code in the right textbox), you can see the file name Building_F01_Stone has F1 (f01 ignore the leading 0) and the key it sends is 'F1' as seen in the module call of widelands.core.call_shortcut('F1',keyboard) I tried hard to make it intuitive.
- Now at the bottom right you have three `set` options, you're only interested in the "Hotkey" option. it should be set. To verify, look to the file name it should have `<f1>` to the right of the name in the file list on the left side of the app. Each file should have its associated Hotkey label showing. If there is nothing there it looks like you'll have to set them yourself. 
- To set a hotkey. Click the desired script, click `set` that is next to the Hotkey: in the right bottom section of the app. When the dialog pops up choose "Press to Set" once button is clicked, choose your hotkey i.e. F1 and press it. then select OK. Then click 'save' (top left of app) autokey needs you to press 'save' all the time.
- Obviously if my keys are not your choice, reset the hotkeys to what you want. Though to make life easy do not change the in-code script example 'F1' this is only a handle and is NOT the Hotkey, it sends to function F1() in the modules if you change to 'g' there is no g() function. So unless you know what your doing with this leave it alone. It is only the Hotkey `set` that can be modified without issues.

## BUGS and Limitations.
- autokey has many limitations and so does using it with widelands. 
- autokey when Setting Hotkeys will freeze sometimes when you press "Press to Set" button. To get out of this, click the close window icon on the window. It should after 5 seconds give you an option to kill the autokey app. Open it again after and set the hotkey again. This is a frustrating bug but once autokey is set it's a case of set and forget... 
- After modifications if you forget to press `save` the update is not recognised and you'll be wondering why it isn't working as expected, so press `save` before you test changes.

## Hotkey Suggestions.
- I suggest that you not use key modifiers such as Alt Ctrl and Shift when creating hot keys. This may play havoc with the feedback I've setup. Though technically it should Not effect the Build , Dismantle, Destroy and Upgrade system. Experiment you'll decide what you want.

## A Run Down on some of the Scripts.

- 00-Reload_module: I've hooked this to the `backtick` key. Critical for development if you play the game and don't want to improve the code, disable this or use the shortcut for something else. If you are working on the Package then hit this hotkey after each modification and it reloads the widelands package/modules. Autokey has a limitation, modify a module and it won't recognise the modification you either reboot autokey or use something like this that reloads the modules..

- 00-Test_script: set to nothing for Debug and Dev working simple_tst() isn't even in the core module now. Use this for testing stuff. It doesn't even have a Hotkey.

- 00-Toggle_tab: I've hooked this to the `tab` key. It is hooked to a ascend and descend sound. If up then toggle_tab is true. If down then False. Think of it as a fake shiftlock. I overused it at one stage during construction. Now with the latest code it is only associated with Amazon , Liana and Rope, if up liana is built, down rope is built. Same for the end key which has Stone_Workshop toggle_tab Furnace. I chose these two sets as they are not that common to build, not like stonecutters and woodcutters etc. There are only so many free keys and I've taken some of the game F-keys already.

## The next 3 are Road building options.

- Build-long-road-1-New
- Build-long-road-2-Connect
- Build-road-3-zigzag
- full guide here [Building_Roads.md](Building_Roads.md) 

## These are all specific Buildings to build
- I originally created this for Atlantean, hence the Atlantean building names for the hotkeys but those names are irrelevent as a F1 will build a Quary in Atlantean, if the game is set for Amazon it will build a Stonecutter. See [user_config.md](user_config.md) for how to change tribes and other settings.
- These just launch the associated function names. If your technical, open a tribe.py eg: atlantean.py and see the function names are F1() F2() etc, end() for the end key , it is all intuitive I hope and makes for ease of following the code.
- Here I tried to be consistent. Example F1 makes stonecutter or quary, the same building just different names, obviously when setting up empire or barbarians the F1 will have their quary type buildings.
- **Special Feature** Example F7 Builds an Amazon Charcoal Kiln. IF the building is built. An F7 on that building will toggle the "Produce Indefinately" option. IF it is a woodcutter that is already built, and F2 will evict the worker, same with the Jungle Preservers , so they can go to Rare Tree Cutters/Plantation. F10 will toggle the "Produce Indefinately" on the Rare Tree Plantation..

- Building_end_Sawmill1
- Building_equal_Tower
- Building_F01_Stone
- Building_F02_Woodcutter
- Building_F03_Forester
- Building_F04_Well
- Building_F05_Baker
- Building_F06_Smoke
- Building_F07_Mill
- Building_F08_Smelt
- Building_F09_Weaponsmith
- Building_F10_Armoursmith
- Building_F11_Fish
- Building_F12_Breader
- Building_hyphen_Guardhouse
- Building_plus_Liana_cutter (np_add(+) is Numpad Plus key)

## These have specialized functions.


- Destroy_Something: Here again I tried to be consisten. I hit on a pattern. The `scrol_lock` key being a pain to reach is set to destroy a building, that is select destroy with the ctrl key held down so no mucking around and no safety (no confirm dialog).
- Dismantle_Something: Same with Dismantle the `/` key. I got sick of manually dismantling buildings. This doesn't do them all, but does enough of the most common dismantles.
- Double_Click `]` Yeh, I'm lazy. I hover over the roads that connect the built Forresters and hit this button. It does a fake double click that will delete the road. Saves a damn lot of mouse clicking.
- Pause: Here I over-ride the spacebar and have it pause the game, you can keep or disable it. If you keep it you'll have to go into game options shortcut keys, find `Toggle Show Build` and replace the `space` with a key, I used the Numpad * as I turn this on once and leave it on all game.
- Upgrade_Something: `[` this will upgrade Tower or Woodcutter and the like with one hotkey press. 



## First Test
- Start Widelands (paused is best).
- Hover over a build site (e.g. red Quary icon).
- Press F1 (or your set hotkey) → it should build the Quary.
- Make sure user_config.py has usr['race_number'] = 0 (Amazon) Hover over a woodcutters building, Hit F2 hotkey, the worker should be ejected.
- If nothing happens: check AutoKey is running, hotkeys set, tribe number correct in user_config.py.
- Have Fun :)
