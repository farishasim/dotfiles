#!/bin/bash

# start compositor
picom --experimental-backends --daemon

# start lock screen
xss-lock -- betterlockscreen -l dimblur -q &
