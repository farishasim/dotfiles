# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# ----------------------------
#          Variable
# ----------------------------

mod = "mod4"
terminal = guess_terminal("alacritty")
browser = "firefox"

# ----------------------------
#           Colors
# ----------------------------

colors = dict(
    background= "0e0f0f",
    foreground= "bbd0d3",
    primary=    "dfb064",
    secondary=  "71abb7",
    info=       "498693",
    warning=    "ffe2a9",
    positive=   "5e9577",
    negative=   "d75f5f",
)

# ----------------------------
#         Util function
# ----------------------------

@lazy.function
def window_to_prev_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 0:
        qtile.current_window.togroup(qtile.groups[i - 1].name)
        qtile.groups[i-1].toscreen()

@lazy.function
def window_to_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 6:
        qtile.current_window.togroup(qtile.groups[i + 1].name)
        # qtile.current_screen.toggle_group(qtile.groups[i + 1])
        qtile.groups[i+1].toscreen()

# ----------------------------
#          Key Binding
# ----------------------------

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Workspace Navigation
    Key([mod, "mod1"], "Left", lazy.screen.prev_group(), desc="Move to left group"),
    Key([mod, "mod1"], "Right", lazy.screen.next_group(), desc="Move to right group"),
    # Move window to another group
    Key([mod, "mod1", "shift"], "Left", window_to_prev_group(), desc="Move window to previous group"),
    Key([mod, "mod1", "shift"], "Right", window_to_next_group(), desc="Move window to next group"),

    # Apps
    Key([mod], "m", lazy.spawn("/home/hasim/.config/qtile/external_monitor_only.sh")),
    Key([mod], "c", lazy.spawn("code")),
    Key([mod], "b", lazy.spawn(browser)),
]

# ----------------------------
#          Group
# ----------------------------

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# ----------------------------
#          Layout
# ----------------------------

layout_border = dict(
    border_normal=colors["background"], 
    border_focus=colors["primary"],
    border_width=1, 
    margin=6
)

layouts = [
    # layout.Columns(border_normal="#4a7074", border_focus=colors["primary"], border_width=3, margin=10),
    layout.Columns(**layout_border),
    # layout.Floating(**layout_border)
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# ----------------------------
#          Widget
# ----------------------------

widget_defaults = dict(
    font="UbuntuMono Nerd Font Bold",
    fontsize=14,
    padding=0,
    # foreground=colors["foreground"],
)

extension_defaults = widget_defaults.copy()

separator = widget.Sep(
    linewidth=2,
    foreground=colors["primary"],
    size_percent=65,
    padding=20,
)

widgets = [
    # LEFT SIDE
    # Rofi app launcher
    widget.LaunchBar(
        test_only=True,
        foreground=colors["primary"], fontsize=18, padding=8,
        progs=[
            (" ", "rofi -show drun", "launch applications")
        ]
    ),
    # Activities
    widget.GroupBox(
        # highlight_color=["000000", colors["primary"]],
        # highlight_color=colors["primary"],
        highlight_method="text",
        this_current_screen_border=colors["secondary"],
        # this_screen_border=colors["primary"],
        padding=1,
    ),
    widget.Prompt(),
    widget.Spacer(),
    
    # RIGHT SIDE
    # Network
    # widget.TextBox("NET ", foreground=colors["secondary"]),
    # widget.Net(
    #     format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}'
    # ),
    # separator,
    # Memory
    widget.TextBox("DISK ", foreground=colors["secondary"]),
    widget.DF(
        visible_on_warn=False,
    ),
    separator,
    # Memory
    widget.TextBox("MEM ", foreground=colors["secondary"]),
    widget.Memory(
        format='{MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}',
        measure_mem='G'
    ),
    separator,
    # Volume
    widget.TextBox("  ", foreground=colors["secondary"]),
    widget.PulseVolume(
        volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -10%",
        volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +10%",
        # emoji=True,
        fmt="{}",
    ),
    separator,
    widget.Clock(
        format="%Y-%m-%d %a %I:%M",
    ),
    widget.QuickExit(
        default_text="    ",
        countdown_format=" [{}s]",
        foreground=colors["negative"],
    ),
] 

# ----------------------------
#          Screen
# ----------------------------

screens = [
    Screen(
        wallpaper="/home/hasim/.wallpaper/desert.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            widgets=widgets,
            size=24,
            border_width=[1, 1, 1, 1],  # Draw top and bottom borders
            border_color=[colors["primary"] for i in range(4)],  # Borders are magenta
            background=colors["background"],
            opacity=0.75,
            margin=[layout_border['margin']*i for i in [1,1,1,1]]
        ),
        bottom=bar.Gap(layout_border['margin']),
        left=bar.Gap(layout_border['margin']),
        right=bar.Gap(layout_border['margin']),
        # Set static wallpaper
    ),
]

# ----------------------------
#           Mouse
# ----------------------------

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag(["control"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# ----------------------------
#          Others
# ----------------------------

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **layout_border
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# ----------------------------
#          Hook
# ----------------------------

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
