import os.path
import re
import nuke
from pdplayer_common import *

def pdplayer_this( path, node, start, end, incr, view ):

  filename = nuke.filename( node )

  if filename is None or filename == "":
    raise RuntimeError( "Pdplayer cannot be executed on '%s', expected to find a filename and there was none." % (node.fullName(),) )

  os.path.normpath( filename )

  pa = nuke.value( node.name() + ".actual_format.pixel_aspect" )

  args = []
  args.append( quote_fn( path ) )

  if len( view ) > 1:

    (lfn, subs) = re.subn( "%V", view[0], filename );
    (lfn, subs) = re.subn( "%v", view[0][0], lfn );
    args.append( quote_fn( lfn ) );
    args.append( "--range=" + str(start) + "-" + str(end) + "/" + str(incr) )
    args.append( "--pixel_aspect=" + pa )
    args.append( "--target_view=left" );

    (rfn, subs) = re.subn( "%V", view[1], filename );
    (rfn, subs) = re.subn( "%v", view[1][0], rfn );
    args.append( quote_fn( rfn ) );
    args.append( "--range=" + str(start) + "-" + str(end) + "/" + str(incr) )
    args.append( "--pixel_aspect=" + pa )
    args.append( "--target_view=right" );

    args.append( "--stereo_view=both" )

  elif len( view ) == 1:

    (lfn, subs) = re.subn( "%V", view[0], filename );
    (lfn, subs) = re.subn( "%v", view[0][0], lfn );
    args.append( quote_fn( lfn ) );
    args.append( "--range=" + str(start) + "-" + str(end) + "/" + str(incr) )
    args.append( "--pixel_aspect=" + pa )

  else:

    args.append( quote_fn( filename ) );
    args.append( "--range=" + str(start) + "-" + str(end) + "/" + str(incr) )
    args.append( "--pixel_aspect=" + pa )

  os.spawnv( os.P_NOWAITO, path, args )

def pdplayer32_this( node, start, end, incr, view ):
  pdplayer_this( get_pdplayer32_path(), node, start, end, incr, view )

def pdplayer64_this( node, start, end, incr, view ):
  pdplayer_this( get_pdplayer64_path(), node, start, end, incr, view )

def init_py():
  pass

def menu_py():

  m = nuke.menu( "Nuke" )
  r = m.findItem( "&Render" )

  r.addSeparator()
  r.addCommand( "Review Selection in Pdplayer &32", "nukescripts.flipbook(pdplayer.pdplayer32_this, nuke.selectedNode())", "#3" )
  r.addCommand( "Review Selection in Pdplayer &62", "nukescripts.flipbook(pdplayer.pdplayer64_this, nuke.selectedNode())", "#6" )
