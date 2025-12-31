## An Autokey specific guide 
- This is Not an Autokey comprehensive guide, it is a general help for implementing the Widelands specific functions needed for using the widelands package.

## Overview
- Basically you unzip the widelands-autokey.zip somewhere, copy/move the resulting 'Widelands' directory to your  ~/.config/autokey/data/Scripts/ directory 

- Technically that is all that is needed. But when is anything easy in this world...

## First
- Install autokey if you haven't got it. I have version 0.95.10 so that version and higher should work.
- For those that have little idea of how to do this, try your distros' package manager such as synaptic. If your old school use `sudo apt-get install autokey` if your on a ubuntu based system. As for other O.S. do a little research on how to install apps. autokey or autokey-gtk or autokey-kde (depends on your OS and your platform)

## Next
- Once autokey is installed run it once to start so that it defines its' .config/autokey directory. Then close the autokey app.

- Then as stated above, unzip the widelands-autokey.zip somewhere and move the Widelands directory it created into the ~/.config/autokey/data/Scripts/ so that it is ready for autokey to load when it starts up.

## Then Run autokey
This will load the macros that you installed into autokey via copying the Widelands directory into it.

## First Time Autokey Run.
- Open autokey and see 'Scripts', left side, it's a directory structure. If you successfully moved the Widelands into the directory above it should be seen inside the Scripts tree. If not check the path etc.
- Now click on the Widelands fold in the Scripts directory. On the right side there should be three `set` options. Abbreviations:, Hotkey: and Window Filter:
- Window Filter should state "widelands.widelands'. If this is not so, then make sure widelands is running , not full screen mode for this unless you have more than one monitor. Click the set button next to window filter and it will give you a dialog , click "Detect Window Properties" and then click on the game window.  This should set the Window Filter to the "widelands.widelands' window. This is an autokey essencial so it knows these macros are for the widelands game ONLY!

## Individual autokey scripts.
- You will find the following scripts inside the Widelands directory:

* 00-Reload_module
* 00-Test_script
* 00-Toggle_tab
* Build-long-road-1-New
*Build-long-road-2-Connect
*Build-road-3-zigzag
*Building_end_Sawmill1
+ Building_equal_Tower
+ Building_F01_Stone
+ Building_F02_Woodcutter
+ Building_F03_Forester
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
- Technically there should be no problems but incase the hotkey was lost the script themselves have comments and tell you #key = # key and most have file names that tell you what the hotkey is.
- example: Building_F01_Stone #key = # F1 (click on it and see), you can see the file name has F1 (f01 ignore the leading 0) and the key it sends is 'F1' as seen in the module call of widelands.core.call_shortcut('F1',keyboard) I tried hard to make it intuitive.
- Now at the bottom right you have three `set` options, your only interested in the "Hotkey" option. it should be set. To verify, look to the file name it should have `<f1>` to the right of the name in the file list. Each file should have its' associated Hotkey label. 
- If this is not so and the clear Hotkey is not an option, that means the Hotkey is not set. So click `set` in the dialog choose "Press to Set" once button is clicked, choose your hotkey i.e. F1 and press it. then select OK. Then click 'save' autokey needs you to press 'save' all the time.
- Obviously if my keys are not your choice, reset the hotkeys to what you want. Though to make life easy do not change the incode script example 'F1' this is only a handle and is NOT the Hotkey, it sends to function F1() in the script if you change to 'g' there is no g() function. So unless you know what your doing with this leave it alone. It is only the Hotkey `set` that can be modified without issues.

## BUGS and Limitations.
- autokey has many limitations and so does using it with widelands. 
- autokey when Setting Hotkeys will freeze sometimes when you press "Press to Set" button. To get out of this, click the close window icon on the window. It should after 5 seconds give you an option to kill the autokey app. Open it again after and set the hotkey again. This is a frustrating bug but once autokey is set it's a case of set and forget... 
- After modifications if you forget to press `save` the update is not recognised and you'll be wondering why it isn't working as expected, so press `save` before you test changes.

## Hotkey Suggestions.
- I suggest that you not use key modifiers such as Alt Ctrl and Shift when creating hot keys. This may play havock with the feedback I've setup. Though technically it should Not effect the Build , Dismantle, Destroy and Upgrade system.

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






