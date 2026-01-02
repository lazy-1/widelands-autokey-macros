## A Simple? Developers Guide
- coding is not simple. This started out with using autokey native keyboard and mouse events and the frustrating race conditions that autokey natively has. It is not made for fine intergration. So I eventually took a deep dive of X11 and found mss which is 10x better than the eventual pyautogui that I used. So many iterations I could write a book but won't.

### File Path ~/.config/widelands_autokey/user_config.py
- referenced so you know where the config file is.

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
- in user_config.py set usr['race_number'] = 2 and save it. Barbarian
- in user_config.py set usr['work_path'] = to a valid/creatable path if /dev/shm is not to your liking. Remember the game when playing will constantly write to this path.
- if you want audio feedback set the usr['sound_dir'] to where you saved the Notification directory you downloaded.
- essencial set usr['debug'] = True
- essencial set usr['log_enabled'] = True 
- Open a Widelands game, it is recommended not be in Fullscreen for ease of debug etc.
- Load or create a Barbarian Game. Pause game and 'show buildings' the `space` bar if you have the default in game macros, or whatever you set it to.
- Hit the Hotkey `` ` `` backtick and you should get a 'meep meep' audio that is feedback that the widelands modules have been reloaded. If you have disabled sound, then maybe exit autokey. Open a terminal and launch autokey from there so you can see the print statements.
- Once you know the reload modules works. we go into working building a building.

## Building a Building. 
- Hover mouse over a 'Green'(large) build site.
- Hit F1 once only. Congrats you built a Quarry.
- Now open the usr['work_path'] , in it you will find 4 similar named files.

- 145648_03_Quarry-T-green-4164_RGB018_087_008.png
- 145648_09_tab_selection-F-(93, 50, 40, 7510)-7510_RGB093_050_040.png
- 145648_35_build_selection-F-(72, 58, 42, 2691)-2691_RGB072_058_042.png
- Barbarian_debug.txt

- Opening Barbarian_debug.txt , this is the log `usr['log_enabled']` it will have the three image file names minus the .png. This makes life easy if your not making images but want the information, it is readaly at hand.

## What those images mean.
- I've supplied them in [example_snapshots/](example_snapshots/)
- 145648_03_Quarry-T-green-4164_RGB018_087_008.png
- What is happening. My script (common.py) does a fake mouse click where your mouse was hovering and a dialog pops up as expected. It snapshots the region around where the mouse is now hovering over the `Green` tab in the build Dialog.
- This snapshot is passed through a filter to id if it is a red,orange,green or blue (seafaring) tab.
- follow the script now we are working on barbarian.py in the tribe directory inside the module package `widelands`
- find the `def F1()` funtion. It says btype = 'Quarry', should be Quary so you get to edit my spelling mistake. btype is short for building type.
- next line is build, site = analyze_dialog(btype) , what that does is what I just described above. Take a snapshot of the dialog where the mouse is now (widelands moves the mouse to the tab of the dialog).
- In this case `build` will be `True` and `site` will be `green`.
- update_USR(btype, site): this updates the USR globals usr['building'] and usr['icon'] so I am not forever passing these variables around.

- item_pos = (5, 45) we'll get to that in a second.
- elif site == 'green': I've skipped the others for the moment, this is the `True` condition and it will use the function build_item_L_S(*item_pos) passing the item_pos to that function.
- Now open common.py and search for that function.
  - def build_item_L_S(x_bldg, y_bldg): # Move Large to Small Tab
    - x_tab, y_tab = (-70, 0)
    - build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg)

## The fun begins
- the long name is build_item_large_tab_must_go_to_small_dialog_tab(): I've called it build_item_L_S() for short.
- x_bldg, y_bldg are obviously 5 and 45 as that is what item_pos is for this F1() function.
- x_tab, y_tab = (-70, 0) this is a standard for Atlantean and Amazon and I assum all others, if not I'll have to fiddle the code here add a if zebra tribe it is (-122,0) or some such, but for now it seems to work. What it says is from the `green` icon move 70 pixels to the left and 0 pixels up and down. This is the `red tab` where we find Quary, Lumberjack and other small builds.

## Now the Action Function. build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg):
- build_item_tab_change(x_tab, y_tab, x_bldg, y_bldg): you know the `tab` x,y and the item pos x,y , they are passed to the work function: Which I will not labour over other than to give a brief outline.
- usr['debug'] is on so the second screenshot 145648_09_tab_selection-F-(93, 50, 40, 7510)-7510_RGB093_050_040.png is made on the `destination` click. i.e. where you are about to click , the `red` tab. So you know that it is going to click the red tab. hence the name `tab_selection` in the image file name , i'll explain the rest later.
- the line stable_click_relative(x_tab,y_tab) , says it all, it clicks the `tab` red in this case, moving the mouse to that position, the dialog opens on the `red` tab. a wait_time is requiered or the dialog won't be fully rendered when we make the third snapshot and click.

- Third snapshot here. Since it is now open on the `red` tab and you want to click on the `Quary` icon, the snapshot is 5 pixels to the right and 45 pixels down. Hence the item_pos is where the building icon is relitive to where the mouse is when it is sitting on the building relavant tab. i.e. if it is an Orange (M,medium) building it is relative from the mouse hovering over the Orange tab.
- Here we have a click_relative(x_bldg, y_bldg) which is 5,45. so clicking on the actual `Quary` icon
- Action done.
145648_03_Quarry-T-green-4164_RGB018_087_008.png
## Now back to the images. Image 1
- First click 145648_03 is a rough time stamp, makes it easy to follow the flow.
- `Quarry` the btype name so you know you hit the F1 key not F2 
- `T` is the `build` variable T=True F=False more on this later
- `green` the tab was a green icon.
- Variance of 4164, simply put, the icon has a variance of 4164 a little bit of noise.
- the AVERAGE RGB of the image, average colour. red, green, blue chanel. 18,87,8 in this case. if you search common.py id_site_tab_color you'll find the filter method.
- id_site_tab_color look to  if (abs(r - 18) <= 5 and abs(g - 87) <= 5 and abs(b - 8) <= 5 and variance < 6000):
- you'll see an exact match 18,87,8 , but occationally there is a pixel shift and it can range between 23 and 13 for r , etc, hence the <= 5 tolerance of plus and minus 5.
- The variance is 4164, is it less than 6000? yes, so it neatly falls in the `green` filter so returns `True` and the colour `green`

## Image 2: 145648_09_tab_selection-F-(93, 50, 40, 7510)-7510_RGB093_050_040.png
- Now we have half a grasp on the naming of them image 2 needs some explaining:
- The time stamp is obvious. The `tab_selection` tells me it had to select a tab it wasn't instantly open on the tab of the building you want to construct.
- Because it is a `tab_selection` the `F` is irrelavant to the name but for simplicities sake it is not removed. This has no actual name as the filter did NOT see the tab, as I have not defined the filter to look if it is right or wrong , it is the user who is developing this that sees , "yes it is the red tab like I wanted" or , dam I used M_S instead of L_S as a function (wrong image expected) , I hope that makes sense.

## Image 3:145648_35_build_selection-F-(72, 58, 42, 2691)-2691_RGB072_058_042.png
- Here again there is useless info on in the file name, but it is not about the file name that is the important part.
- `build_selection` this says this is the place I am clicking on to build the building. Your job is to center the `Quarry' on the image. 5, 45 is what the F1() function thinks it is. what if we changed it to 50 to the right and not 5 , 45 down remains the same. If you guessed it would show a lumberjack building then your right, a little off center but it would click it.

## Quick Review.
- Hover over build site, Hit Hotkey, dialog is opened. Snapshot to see what colour tab it opened at. If it needs to change tabs the code tells it to , i.e. elif 'orange' or 'red'. that type of thing. It changes tab, then clicks on the actual building you wanted. And that is the essencials of building..

## Advanced Functions. Stage 2 define your own Action.
- Building is stait forward now, I won't go into how many sleepless nights it took to get there but now it is relatively simple and generally reliable, if you move the mouse as your hitting the Hotkey this can cause errors and unexpected results.

- By now you should understand how the macro works and what is involved. You feed in co-ordinates and it opens the dialog, takes snapshots and clicks on the co-ordinate you entered.

- So what if I want to upgrade the Amazon Woodcutter. How does that work. Not that simple.

## Existing Function amazon.py leftbracket()
- as a pre cursor to this I expect the user to have changed the usr['race_number'] = to 0 so that we are working on the same thing. And opened an Amazon game.
- find that function and let us go through it.
- update_USR('leftbracket', 'none'): just updating the two USR variables for feedback purposes though I don't even think I bothered to use them but following a standard is good for future profing things.
- site = determine_dialog(): this is new and the core of this function. Go to common.py and find it and I'll do a step by step.


- capter the mouse position so later we can return the mouse to that spot so it doesn't stay where it last was and become a pain in the butt.
- stable_click() this just `left clicks` where the mouse is hovering and opens a dialog.
- the sleep here is to give time for the dialog to render, if your getting map images a lot your render time is too short, edit it in the user_config.py.
- build,site,var = get_screenshot_info(x=-62,y=-35,area=(30,17), method='building')
- I need to explain this a little. get_screenshot_info() we brushed passed when doing the Build Building tutorial. But now it is essencial for developers to understand as you could write your own `determine_X_dialog` and need specifics.

## get_screenshot_info(x=0, y=0, desc='n-a', area=(29, 29), method='general'):
- x and y should be self evident, from the hover point of the mouse , move x,y and that is the center point of the snapshot I want.
- decs='Anything you want in the filename and debug file'
- area=(x,y) so a (30,17) in the determine_dialog() means we want a rectangle 30 pixels long and 17 high.
- method='general' : this points to where you want to get your filter info. If you scroll in the  get_screenshot_info() function you will see 'general','building','id_dialog_icon'. these point to three different functions that filter the rgb and variance and return a string description of what it found.


## so we are up to area=(30,17), method='building'
- the snapshot of that area and possition has been taken, the objective is to find out what it is. 
- 'building': This can be a bit ambiguous. It means 'building has been built' so this is a 'building' dialog vs a 'find building you want to build' dialog. So we clicked on a built building because the red, orange, green and blue filters didn't recognise the snapshot colours. I hope that is clear.(as mud probably)
- so elif method == 'building': uses id_building_via_dialog_tells(r, g, b, variance)
- go to that function and find a similar one to id_site_tab_color, but where is it, it's not in common.py. I'll save you the panic, this one is in amazon_rgbv.py, you've noticed the file but didn't worry till now.

## _rgbv what does it mean.
- open amazon_rgbv.py as this is the tribe we are working on remember.
- It has a huge comment block that should be helpful.
- Now the 'building' method wants to use id_building_via_dialog_tells. check it out. we will go through the most common `Garrison`
- find a built Patrol Post, Garrison. hover over it and hit the `[` hotkey or your version of it. Then look inside the debug directory and see simalar images 
- as a side note I usually delete all files in the debug directory before I do things as it gets full and confusing after a while.
- don't forget to have usr['race_number'] = 0 and `` ` `` reload modules for this tutorial.
- Two images this time: 
- 165725_29_n-a-F-Garrison-11512_RGB116_103_023.png
- 165725_30_n-a-F-(113, 102, 75, 4137)-4137_RGB113_102_075.png
- Have a look at them. You've got a handle on how to `debug` read the file name. So what have we got.
- The first is obviously recognised as a `Garrason`, if you see the tiny image and look at a fully opened Patrol Dialog , you will see where the snapshot was taken. If you look at the filter 
- if (abs(r - 118) <= 10 and abs(g - 106) <= 10 and abs(b - 26) <= 10
   - and 10000 < variance < 12500):# 'Gar' image
   - return (False, 'Garrison')
- You will see it is 116 in the image the filter has 118 +-10 so it is well within range. Next g(green) is 103, the filter is 106 with a range of 10 again. All rgb fall in the range so it is probably a Garrison. But to add extra checking we see if the variance falls into the variance range which it does. So it is a `Garrison`.
- False just means it is a Built building Dialog, not a 'we are making a building dialog', that should be clear by now.
- Now 165725_30_n-a-F-(113, 102, 75, 4137)-4137_RGB113_102_075.png is an interesting snapshot. It was taken with the method='id_dialog_icon'. filter, check that one in amazon_rgbv.py , it has several tests, is it a 'swirl' icon, is it a notable 'Charcoal_Kiln' tell. It is very hard to id a dialog at times as they are so generic at times yet ones like charcoal kiln are edge cases. 

## Moving on, lets try Upgrade on a woodcutter.
- still in amazon, and Hotkey `[` for upgrading. lets see what happens hovering over a built woodcutter and hit hotkey.
- site = determine_dialog() returns a 172154_28_n-a-F-Standard_brown-387_RGB088_068_040.png snapshot. Interesting.
- On Garrions the (x=-62,y=-35) offset snapshot returns a 'Gar' image. But on a woodcutter and some other but not all, that returns a brown image that I called 'Standard_brown', so you know a standard brown was snapshotted.
- Next is the in determine_dialog() if site == 'Standard_brown': it goes for a second snapshot.
- This is co-ordinates (x=-327,y=-67) of the dialog. and a tiny area=(22,22) and again we use the 'building' detect method.
- if you check that tiny image 172154_29_n-a-F-Woodcutter-10002_RGB105_081_056.png you will note it is uneque to woodcutters, top left, you'll find it.
- this image is passed through the id_building_via_dialog_tells and it found that that rgb and variance was all in the 'Woodcutter' range. 

- following the flow we come to the last image: 172154_40_in_building_dialog-F-upgrade_icon-568_RGB095_076_045.png which is an upgrade icon. The code clicks on it and the building is upgraded as expected.


## Wrapping Up.
- I could go on all day but I feel that the essence has been told and the picture painted. With the tools I provided and the Help files there should be enough info for a compitent person to figure out the next steps.
- Essencially snapshot the dialog, determine what it is which can be hard at times. Then click where you intend. and there you go. Hover mouse hit Hotkey and most labourious things can be streamlined.
- Hope this helped and enjoy the game.
