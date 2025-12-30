## An Autokey specific guide 
- This is Not an Autokey comprehensive guide, it is a general help for implementing the Widelands specific functions needed for using the widelands package.

## Overview
Basically you unzip the widelands-autokey.zip somewhere, copy/move it to your  ~/.config/autokey/data/Scripts/ directory , i.e. you now have the extracted Widelands directory in there.

Technically that is all that is needed. But when is anything easy in this world...

## First
Install autokey if you haven't got it. I have version 0.95.10 so that version and higher should work.
For those that have little idea of how to do this, try your distros' package manager such as synaptic. If your old school use apt-get install autokey if your on a ubuntu based system. As for the rest do a little research on how to install apps.

## Next
Once installed, as stated above, unzip the widelands-autokey.zip somewhere and move the widelands directory it created into the ~/.config/autokey/data/Scripts/

## After, Run autokey
If you use autokey for other stuff like I do then you will already have it running on startup, so reboot it so it can load the widelands folder. If not you either manually start autokey every time you want to play the Widelands game or set it to be on all the time..

## First Time Autokey Run.
- Open autokey and see 'Scripts', left side, it's a directory. if you successfully moved the Widelands into the directory above it should be seen inside there, if not check the path etc.
- Now click on the Widelands fold in the Scripts directory. On the right side there should be three `set` options. Abbreviations:, Hotkey: and Window Filter:
- Window Filter should state "widelands.widelands'. If this is not so, then make sure widelands is running , doesn't have to be full screen mode. Click the set button next to window filter and it will give you a dialog , click "Detect Window Properties" and then click on the game window.  This should set the Window Filter to the "widelands.widelands' window.

## Individual autokey scripts. There should be

00-Reload_module
00-Test_script
00-Toggle_tab
Build-long-road-1-New
Build-long-road-2-Connect
Build-road-3-zigzag
Building_end_Sawmill1
Building_equal_Tower
Building_F01_Stone
Building_F02_Woodcutter
Building_F03_Forester
Building_F04_Well
Building_F05_Baker
Building_F06_Smoke
Building_F07_Mill
Building_F08_Smelt
Building_F09_Weaponsmith
Building_F10_Armoursmith
Building_F11_Fish
Building_F12_Breader
Building_hyphen_Guardhouse
Building_plus_Liana_cutter
Destroy_Something
Dismantle_Something
Double_Click
Pause
Upgrade_Something
z-space-building-show


## What to do with them.
- Technically there should be no problems but incase the hotkey was lost the script themselves have comments and tell you #key = # key, 
- example: Building_F01_Stone #key = # F1 , you can see the file name has F1 (f01 ignore the leading 0) and the key it sends is 'F1' as seen in the module call of widelands.core.call_shortcut('F1',keyboard) I tried hard to make it intuitive.
- Now at the bottom right you have three `set` options, your only interested in the "Hotkey" option. it should be set, i.e. the Hotkey in the left panel should show <f1> to the left of Building_F01_Stone.
- If this is not so and clear Hotkey is not an option, that means the Hotkey is not set. So click `set` in the dialog choose "Press to Set" once button is clicked, choose your hotkey i.e. F1 and press it. then select OK. 
- Obviously if my keys are not your choice, reset the hotkeys to what you want.

## BUGS and Limitations.
- autokey has many limitations and so does using it with widelands. 
- autokey when Setting Hotkeys will freeze sometimes when you press "Press to Set" button. To get out of this, click the close window icon on the window. It should after 5 seconds give you an option to kill the autokey app. Open it again after and set the hotkey again. This is a frustrating bug but once autokey is set it's a case of set and forget... 

## Hotkey Suggestions.
- Because I use pause unpause as a feedback. Any use of shift or ctrl stuffs this up and no feedback is seen. So don't use modifier keys unless you want to forgo feedback pause unpause. I play the game by myself so pause the game and make all the buildings, roads etc in pause mode, each time anything is added it is unpaused then paused again to show that the building is under construction.

## A Run Down on some of the Scripts.

- 00-Reload_module: I've hooked this to the `backtick` key. Critical for development if you play the game and don't want to improve the code, disable this or use the shortcut for something else. If you are working on the Package then hit this hotkey after each modification and it reloads the widelands package/modules. Autokey has a limitation, modify a module and it won't recognise the modification you either reboot autokey or use something like this that reloads the modules..

- 00-Test_script: set to nothing for Debug and Dev working simple_tst() isn't even in the core module now. Use this for testing stuff.

- 00-Toggle_tab: I've hooked this to the `tab` key. It is hooked to a assend and decend sound. If up then toggle_tab is true. If down then False. Think of it as a fake shiftlock. I over used it at one stage now with the latest code it is only associated with Amazon , Liana and Rope, if up liana is built, down rope is built. Same for the end key which has Stone_Workshop toggle_tab Furnace. I chose these two sets as they are not that common to build, not like stonecutters and woodcutters etc. There are only so many free keys and I've taken some of the game F-keys already.

## The next 3 are Road building options.

- Build-long-road-1-New
- Build-long-road-2-Connect
- Build-road-3-zigzag

## These are all specific Buildings to build
Building_end_Sawmill1
Building_equal_Tower
Building_F01_Stone
Building_F02_Woodcutter
Building_F03_Forester
Building_F04_Well
Building_F05_Baker
Building_F06_Smoke
Building_F07_Mill
Building_F08_Smelt
Building_F09_Weaponsmith
Building_F10_Armoursmith
Building_F11_Fish
Building_F12_Breader
Building_hyphen_Guardhouse
Building_plus_Liana_cutter

## These have specialized functions.



Destroy_Something
Dismantle_Something
Double_Click
Pause
Upgrade_Something
z-space-building-show






