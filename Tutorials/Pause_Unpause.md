## Overview
- I personally run the game as a Single Player. I've changed the in game option
- "Toggle Building Spaces" from `space` to Notepad `*` , I toggle this on at the begining of the game and leave it on.
- For whatever reason the in Game Hotkey options would not accept the changing of `pause` to the spacebar press. So I cheeted. I left that alone in the game and used the autokey intercept which grabs `space` and sends that as a keypress of the `pause` button to the game. 
- My code relies on `pause` as the pause button and I did not change that so unless you have modified the in game hotkeys for pause to something else all should be fine.
- I usually do mass building setup while the game is paused so I can take my sweet time. Hence in `Pause` I hover mouse over build site, hit F1 and the Quary is built there, the game unpauses and pauses again to show that the site is built.
## Potential issues.
- The Pause Unpause feedback is great for Single Players but I assume a pain in the ass for Multiplaying. So I suggest you disable the function see [user_settings.md](user_settings.md) to learn about the user_settings.py or just read user_settings.py and set the pause feature to False.
