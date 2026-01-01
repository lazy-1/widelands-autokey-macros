## A Simple Developers Guide












### Development & General
- `` ` `` = Development, reloads the widelands module for AutoKey, so module modifications take affect.
- Space = Pause game (set via game shortcuts — my personal like) This is unpause_pause() code as well so if you want this feature, then make sure that your using the same 'pause' or 'space' or whatever you have pause set to.
- Tab = Toggles 'tab toggle' Basically gives you double the keys available, acts as a defacto ShiftLock. The game will not accept shift F1 etc without issues. But if you want to use 'shift' etc have a try. eg. Amazon with shift-F1 would have a function named Amazon_shift_F1 when as a label passed from the autokey script. Be aware feedback is confused as the hold of shift interfears with the autokey send of 'pause'..
  Sound Down = False (default state on startup)  
  Sound Up = True, for keys defined with Tab Toggle sets different task
- * = Toggle Show Build sites (NUM PAD * — set via game shortcuts pref — my personal like) This is replacing the 'space' default for Toggle show building. As I set and forget this at start of game. 



## Creating Your Own Functions
- I tried my best to use unused game keys but obviously some of the F keys are used by the game but now my macro is capturing them instead. I was using the 'dot' key as well until my last build where I use the space bar for pause instead. The `.` is no longer used but for those who want to You can use it to build, dismantle, upgrade or other. Pass 'dot' from the autokey script, in the widelands.py call it Amazon_dot and Atlantean_dot etc and you have a new function, it can be Two functions in one if you use toggle_tab. 
- Extra note on `toggle_tab` this can be expanded if the user wants to define 0,1,2 instead of true false. I attached an audio assending sound to toggle on, and an audio decending sound to off so that the user can hit the toggle(tab) key and know the state they just set themselves. There is a lot of potential here but also needless complexity in my opinion. Two states are bad enough as there is no visual 'It is On/Off' 

## Keyboard Shortcuts








