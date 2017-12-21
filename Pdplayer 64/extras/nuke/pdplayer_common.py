import os.path
import nuke

if nuke.env['WIN32']:
  import _winreg

def get_pdplayer32_path():

  if nuke.env['WIN32']:

    path = 'C:\Program Files\Pdplayer\pdplayer.exe'

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

    return path

  elif nuke.env['MACOS']:

    return "/Applications/Pdplayer 32.app/Contents/MacOS/Pdplayer 32"

  else:

    return "/opt/pdplayer/pdplayer32"

def get_pdplayer64_path():

  if nuke.env['WIN32']:

    path = 'C:\Program Files\Pdplayer 64\pdplayer64.exe'

    try:
      k = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pdplayer64.exe' )
    except EnvironmentError:
      k = None

    if k:

      try:
        path = _winreg.QueryValue( k, None )
      except EnvironmentError:
        pass

      k.Close()
  
    return path

  elif nuke.env['MACOS']:
  
    return "/Applications/Pdplayer 64.app/Contents/MacOS/Pdplayer 64"
    
  else:
  
    return "/opt/pdplayer/pdplayer64"

def quote_fn( fn ):

  if nuke.env['WIN32']:

    return "\"" + fn + "\""

  else:

    return fn

def get_lut_path( path ):

  if nuke.env['MACOS']:

    return os.path.join( os.path.dirname( path ), "..", "Resources", "LUTs", "nfb" )

  else:

    return os.path.join( os.path.dirname( path ), "LUTs", "nfb" )
