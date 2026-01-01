# How to Download and Install the Macros

There are two ways to get the macros. Most people should use **Option 1 (ZIP)** — it's the easiest.

### Option 1: Download as ZIP (Recommended – No Software Needed)

1. Go to the repo main page:  
   https://github.com/lazy-1/widelands-autokey-macros

2. Click the green **Code** button (a little way from the top, roughly middle right).

3. Click **Download ZIP**.

4. Save the file (widelands-autokey-macros-main.zip or main.zip) to your computer.

5. Extract/unzip the folder anywhere (Desktop, Documents, etc.).

6. Inside you will see:
   - `Notification` folder (sounds I use)
   - `widelands/` folder (the main macros package)
   - `Tutorials/` folder (this guide and other help files)
   - README.md and other files
   - `widelands-autokey.zip` (autokey macros)
   - `LICENSE` (the usual crap)

That's it — no terminal or extra programs required.

### Option 2 is optional — use it only if you want easy updates later. Option 1 (ZIP) is enough for most people

If you want to update easily with one command when new versions come out:

1. Install Git (one-time):
   Open a terminal and run:   `sudo apt update && sudo apt install git`
2. Go to a folder where you want the files (e.g. Documents):`cd ~/Documents`
3. Download the repo: `git clone https://github.com/lazy-1/widelands-autokey-macros.git`
4. Enter the folder: `cd widelands-autokey-macros`
5. To update later (pull new changes): in the  widelands-autokey-macros folder `git pull` will update the contents.
6. Install the same way as Downloaded and extracted ZIP from Option 1: Instructions below.

 
## Install.
   - Installing python modules needed `pip3 install python-xlib pillow mss` to be done in a terminal.
   - Install autokey if not already on your system. Search synaptic or other package managers for autokey, or autokey-gtk or autokey-kde , it will be OS and platform specific. This is the engine that grabs the Hotkeys and accesses my modules.


## Now my specific Installs.
   - Make sure autokey has been run at least once and close it. This is so that it creates the `.config/autokey` standard hidden directories.

   - Starting with widelands-autokey.zip, extract the `Widelands` folder. This will need to be placed in your autokey data directory.  `~/.config/autokey/data/Scripts/` (press Ctrl+H in file manager to see hidden folders) or find a setting to show hidden files. 

   - Next is the  `widelands` specific module. Instructions assume you have an unzipped download or are in the git which is the same. In that dir you will find `widelands` inside is core.py , common.py, user_settings.py and other files etc.

   - So this `widelands` is the `Package` (modules) , we need to tell autokey where the Package is. Before we do that make sure, that the `widelands` directory is in a place not easilly deleted accidently. Copy/Move it somewhere safe or leave it where it is if that is a safe place.

   - Now run autokey. It usually launches as a system icon and doesn't open the window, if that happens find the system tray icon, usually an 'A' type outline font looking thing. Click it and 'show main window'. The app is open.

   - Edit -> Preferences -> Script Engine (its a tab), there is a drop down selector, it is a directory browser, find the directory that contains the mentions `widelands` package NOT the package itself, but the directory that contains the widelands directory.
   - IF you already use autokey, then copy or move `widelands` to your already defined modules directory.
   - Re-Start autokey to make sure it is loading the package. [Autokey_GUIDE.md](Autokey_GUIDE.md) is a comprehensive overview of My macros, what to do if they are not automatically set etc.

## That is the Install done.
   - Next are a few tweek of your user_settings.py which is inside the `widelands` package. see [user_settings.md](user_settings.md)




