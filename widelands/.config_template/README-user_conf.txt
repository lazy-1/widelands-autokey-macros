user_conf.conf – Settings Documentation
────────────────────────────────────────

This file explains all the settings found in user_conf.conf
You only need to edit user_conf.conf — this file is for reading only.

Last meaningful update of this explanation: January 2026


Race & Basic Setup
────────────────────────────────────────
Which race you are currently playing
0 = Amazon
1 = Atlantean
2 = Barbarian
3 = Empire
4 = Frisian

    [main]
    race_number = 0          ; Change this number to match your in-game race


Work path & transient file
────────────────────────────────────────
Where debug logs, snapshots and the transient road-building file are saved.
Using /dev/shm (RAM disk) is strongly recommended because there are many
read/write operations — bad for SSD lifetime if stored on disk.

    [main]
    work_path = /dev/shm/Widelands/
    transient_path = %(work_path)sautokey_transient_store.json


Audio Feedback – General
────────────────────────────────────────
Where your sound files are stored (bell.oga, complete.oga, etc.)

Leave sound_dir empty to use the default location relative to the main script.
If you set it manually, make sure it ends with a slash /

    [main]
    sound_dir =                  ; empty = default, or: /home/user/Sounds/notifications/
    enable_sounds = true         ; true / false – turn all macro sounds on or off


Sound Files Dictionary
────────────────────────────────────────
Which sound is played for different events.
Leave value empty '' to disable that sound.

    [sound_files]
    red          = bell.oga                  ; Build site: large/red – Not Used
    orange       = complete.oga              ; Build site: medium/orange – Not Used
    green        = dialog-warning.oga        ; Build site: small/green – Not Used
    big_error    = phone-incoming-call.oga   ; Major error / alert
    meedmeep     = MeebMeeb.ogg              ; Module reload feedback
    down1        = KDE_Window_Close.ogg      ; Downward tone – Not Used
    up1          = KDE_Window_Open.ogg       ; Upward tone – Not Used
    down2        = Chatdown.ogg              ; Downward tone
    up2          = Chatup.ogg                ; Upward tone
    down3        = Musica Restore Down.ogg   ; Downward tone – Not Used
    up3          = Musica Restore Up.ogg     ; Upward tone – Not Used
    sharpstrum1  = sharp_organ.ogg           ; Sharp alert

    You can add your own entries here, example:
    custom_success = success.oga


Pause & Pause Delay
────────────────────────────────────────
Controls whether the game is paused during certain macro actions
and how long to wait after unpausing to let the game catch up.

    [main]
    enable_pause = true
    pause_delay  = 0.2         ; seconds – too short → pause may not register


Debug & Logging
────────────────────────────────────────
Full debug mode saves screenshots + verbose logs (makes macros noticeably slower)
Only enable when tuning or finding problems.

    [main]
    debug      = false         ; true = snapshots + heavy logging
    log_enabled = false        ; separate text log file


Click Stability Settings
────────────────────────────────────────
These control how reliably clicks are registered in Widelands/SDL2.

stable_click:
    delay after cursor warp (settle time)   → 0.03–0.08 s   (0.04 is safe)
    click hold duration                     → 0.01–0.05 s   (0.02 is reliable)

stable_click_relative:
    warp settle                             → usually 0.05
    click hold                              → usually 0.03

    [timings]
    delay_stable_settle = 0.04
    delay_click_hold    = 0.02
    warp_settle         = 0.05
    click_hold          = 0.03
    ctrl_press_delay    = 0.05


Waiting / Timing for Road Building & Dialogs
────────────────────────────────────────
Various short delays to make sure the game has registered clicks,
opened dialogs, or rendered content before the macro continues.

Typical safe values are already set. Only change if you see problems
(dialogs opening in wrong place, clicks ignored, etc.)

    [waits]
    wait_for_dialog1   = 0.05     ; Build_Zigzag_Road – wait for dialog
    wait1              = 0.1      ; Build_Connect_Road – after stable click
    wait_for_dialog2   = 0.1      ; Build_Connect_Road – dialog open
    wait_to_register1  = 0.1      ; Build_New_Road – mouse click register
    wait_for_dialog3   = 0.1      ; Build_New_Road – dialog render
    wait_to_register2  = 0.05     ; Build_New_Road – dialog click register
    wait_screenshot    = 0.05     ; screenshot race condition throttle
    wait_to_register3  = 0.05     ; common dialog click register


That's all the settings currently defined.
You can add your own keys in user_conf.conf if needed,
but the macro will only use the ones listed here.
