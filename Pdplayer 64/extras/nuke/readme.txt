Pdplayer Nuke Integration
-------------------------

This directory contains Python scripts that allow Pdplayer to be used as a
Nuke flipbook. To enable this integration, copy the contents of this directory
(without this readme.txt file) into your .nuke directory (the .nuke directory
is a subdirectory of your home directory and is described in "Loading Gizmos,
NDK Plug-ins, and TCL scripts" in the Nuke user guide).

If you already have an init.py or menu.py file in .nuke, you can append the
contents of init.py or menu.py in this directory to your existing file instead
or overwriting it (Python scripts are ordinary text files).

If your version of Nuke is 6.2 or later, you will get two additional options
in the "Flipbook Selected" dialog in addition to the default "Framecycler" -
"Pdplayer 32" and "Pdplayer 64".

If you're using Nuke 6.1 or earlier (5.2 is the earliest version supported by
these scripts), you will get two additional menu items in the Render menu -
"Review Selection in Pdplayer 32" and "Review Selection in Pdplayer 64".

Under Mac OS X, these scripts assume that Pdplayer 32 and Pdplayer 64 are
located in /Applications. Under Linux, they look for pdplayer32 and pdplayer64
in /opt/pdplayer.
