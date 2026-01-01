## The are 3 Road Building Options.

- A typical road build goes like this. Hover mouse over a Road Flag, it has to be active flag of a road you have already built or the start (active) flag of the Headquarters. Press one of the three road Hotkeys that you want to do, example build long road new. Then move mouse to where you want that road to end. hover mouse at destination and hit the Hotkey a second time. And there you have it, the full road with flags. A few experiments should get you going.

## More Details.
- Build-long-road-New:`;` Intended use. Hotkey on existing road flag, move mouse to destination and Hotkey again. It will build from point A to B with flags set inbetween. If your a perfectionist like me you want even number of segments. So try this Hotkey on flag, move to where you think you want it, left click mouse button and it will say 10 or 11 , whatever the distance, if it is uneven move mouse to hover at the even point, then hit Hotkey. 
- Build-long-road-Connect:`'` You have two roads made already. You Hotkey on one flag, move to the other road and Hotkey on the second flag. This will join the two roads flagging the road. Great if you have a mass of roads to join up.
- Build-road-zigzag:`/` This is for joining roads 2 spaces apart. Hotkey on first flag, then on second flag. I call it zigzag because you do a lot of zigzag road building for huge games and I like huge games. This is intended for 2 spaces but if you do a road 10 spaces it will join but Not have the ctrl key held so no flags, that is what the `'` is used for. 

## Annoying Bugs.
- Sometimes the user Double hits the Hotkey as the 'Firt Press' and the code thinks it is the second Press so things go wonky. You'll notice this at times when it behaves wrong. You will eventually recognise it is going '2 - 1' not '1 - 2' and realise you need to click a third time , usually in a harmless place. To get the rhythm back again. No major biggy, just be aware.

## Coding Overview/Reasons.
- There is no way to know if this is your first or second Hotkey Press without saving something somewhere.
- Autokey has a native save state function that will save a True or False so that you can read it to find out if your comming or going. Trouble is that function is saved to disk and when building roads, especially zigzag you litterally do hundred and hundreds of writes to the same file on disk.
- Since I have ssd and do Not like the constant disk writes I've made my own Transient file that saves the Boolen value needed to remember if this is your first or second click.
- I save this file to the RAM instead of the file system. For those that do not know, in linux the /dev/shm is actually a ram disk. So you are not writing to the system but to the ram and if you writing hundreds and sometimes thousands of times in a game, then RAM is the best place to do it on a modern system.