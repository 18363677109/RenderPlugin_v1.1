import nuke
import os.path
import _winreg

m = nuke.menu("Nuke")
r = m.findItem("&Render")

r.addSeparator()
r.addCommand("Review Selection in &Pdplayer", "nukescripts.flipbook(pdplayer_this, nuke.selectedNode())", "#P")

def pdplayer_this( node, start, end, incr, *args ):

  filename = nuke.filename( node )

  if filename is None or filename == "":
    raise RuntimeError( "Pdplayer cannot be executed on '%s', expected to find a filename and there was none." % (node.fullName(),) )

  os.path.normpath( filename )

  pa = nuke.value( node.name() + ".actual_format.pixel_aspect" )

  path = 'C:\Program Files\Pdplayer\pdplayer.exe'

  try:

    k = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pdplayer64.exe' )

  except EnvironmentError:

    try:

      k = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pdplayer.exe' )

    except EnvironmentError:

      k = None

  if k:

    try:

      path = _winreg.QueryValue( k, None )

    except EnvironmentError:

      pass

    k.Close()

  args = [ "\"" + path + "\"", "\"" + filename + "\"" ]

  args.append( "--range=" + str(start) + "-" + str(end) + "/" + str(incr) )
  args.append( "--pixel_aspect=" + pa )

  os.spawnv( os.P_NOWAITO, path, args )
