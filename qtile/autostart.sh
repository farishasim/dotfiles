#!/bin/bash

# start compositor
picom --experimental-backends --daemon

# start lock screen
xss-lock -- betterlockscreen -l dimblur -q &

# disable primary monitor
bash $HOME/.config/qtile/external_monitor_only.sh &
