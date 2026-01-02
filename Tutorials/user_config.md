## user_config.py is your friend ;^)

## File Path ~/.config/widelands_autokey/user_config.py

## First Things First.
- Run autokey with the macros setup and the `widelands` module intalled. Then open a widelands game, any game. Press one of the Hotkeys, any Hotkey. This auto creates the ~/.config/widelands_autokey/user_config.py file.

### Overview
- This file is created on the first use of an autokey Hotkey press.
- It is permanant and does not change between module upgrades (unless the config file itself needs changing and notes will be supplied for that upgrade)
- To edit you need to be able to see Hidden files in your home directory. Turn that feature on in your file browser, and search for that file.
- It is a literal python module so has more scope than a simple text file. Be careful when editing as corrupting it will disable the macros.
- Primary use is when you want to be Atlantean instead of Amazon. You will find the usr['race_number'] = 0 , and change that 0 (Amazon) to 1 (Atlantean) reload the package via the `` ` `` (backtick) key (alternate, close and open autokey so it sees the change). And away you go, the Hotkeys are now tuned to building Atlantean buildings etc. Probably I'll make a GUI interface but for now it is manual handling.
- Yet that is not all that this file can do. From change the 'work_path' to how quick the 'warp_settle' is. So have a browse through it and see the comments, they should be very helpful.
- **Important** before you run this and use it, you should edit a few things. Number one is usr['work_path'] this is where the transient save file goes and I strongly suggest you leave it as /dev/shm as described in [Building_Roads.md](Building_Roads.md) "Coding Overview/Reasons"
- Another suggestion is edit the usr['sound_dir'] with the path you saved the Notifications in that way you'll have sound, although I don't have a lot of sound, just the `tab` Toggle_tab and the `` ` `` Reload_module nowadays, I did start out with a lot of feedback when I was constructing but dropped a lot of it, you can insert them at will in the code if you want `_play_sound('your_defined_str')` with obviously the entry update in user_config with the sound path.

- The usr['sound_files'] is created on the sound files I provided, you can edit the sound_dir and the sound_files to your liking.

- Pause on off: usr['enable_pause'] this is my favorite feedback because I am in pause and want to know the building is being built when I hit the Hotkey. If you don't want this unpause/pause function turn it off here
- usr['debug'] set this true if you're developing and want to see the screenshots.
- usr['log_enabled'] keep this true if you want to keep a log.
- those two, log and debug use the work_path directory.
- Now it is nitty gritty time and micro manage the dwell times between clicks and dialog rendering etc. These settings can be traced to their functions in common.py If for example you have troubles because the dialogs are not rendering properly before the 'fake mouse click' clicks, then modify usr['wait_to_register variables, there are 3 , it will probably be the last one that will help, bump it up to 0.1 shouldn't need more than that..
## Final Note!
This file is yours. If someone decides to do the empire, barbarian and frisian and you want the upgrade and you download and install them, this file is not effected. It is meant to be a users personal config file.