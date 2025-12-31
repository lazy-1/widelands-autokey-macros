## user_settings.py is your friend ;^)
- This file is found in the root of the widelands package. It is for you to edit to make sure that your experience is optimal.
- Primary use is when you want to be Atlantean instead of Amazon. You will find the USR['race_number'] = 0 , and change that 0 (Amazon) to 1 (Atlantean) reload the package via the `` ` `` (backtick) key. And away you go the Hotkeys are now tuned to building Atlantean buildings etc.
- Yet that is Not all that this file can do. From change the 'work_path' to how quick the 'warp_settle' is. So have a browse through it and see the comments, they should be very helpfull.
- **Important** before you run this and use it, you should edit a few things. Number one is USR['work_path'] this is where the transient save file goes and I strongly suggest you leave it as /dev/shm as described in [Building_Roads.md](Building_Roads.md) "Coding Overview/Reasons"
- Another suggestion is edit the USR['sound_dir'] with the path you saved the Notifications in that way you'll have sound, although I don't have a lot of sound, just the `tab` Toggle_tab and the `` ` `` Reload_module now days, I did start out with a lot of feedback when I was constructing but dropped a lot of it, you can insert them at will in the code if you want..

- The USR['sound_files'] is created on the sound files I provided, you can edit the sound_dir and the sound_files to your liking.

- Pause on off: USR['enable_pause'] this is my favorite feedback because I am in pause and want to know the building is being built when I hit the Hotkey. If you don't want this unpause/pause function turn it off here
- USR['debug'] set this true if your developing and want to see the screenshots.
- USR['log_enabled'] keep this true if you want to keep a log.
- those two, log and debug use the work_path directory.
- Now it is nitty gritty time and micro manage the dwell times between clicks and dialog rendering etc. These settings can be traced to their functions in common.py If for example you have troubles because the dialogs are not rendering properly before the 'fake mouse click' clicks, then modify USR['wait_to_register variables, there are 3 , it will probably be the last one that will help, bump it up to 0.1 shouldn't need more than that..
## Final Note!
This file will be yours. If someone decides to do the empire, barbarian and frisian and you want the upgrade. copy your user_setting.py somewhere before you upgrade, upgrade then copy your one over the new one. This is meant for keeping user stuff separate from coding. If someone does do Empire example, it will only be the empir.py and empire_rgbv.py that are modified, the main code should be stable enough and have little to no need for updates, having said that I've most likely jinxed it..