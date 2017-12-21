import nuke

if nuke.env['NukeVersionString'] >= '6.2':

  from pdplayer_62 import *

else:

  from pdplayer_52 import *
