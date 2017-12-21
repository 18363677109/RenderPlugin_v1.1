import os.path
import re
import nuke
import nukescripts
from pdplayer_common import *

class PdplayerFlipbook( nukescripts.FlipbookApplication ):

  def _add_lut( self, lut, is_dpx, fnargs ):

    la = lut.split( "-" )

    lf = None
    cs = "sRGB"

    if len( la ) < 2 or la[0] == la[1]:

      if is_dpx:
        lf = "linear"

    elif la[1] == "linear":

      lf = la[0]

    elif la[1] == "sRGB":

      if la[0] != "linear" or is_dpx:
        lf = la[0]

      cs = "linear"

    else:

      lf = lut

    if lf != None:

      fnargs.append( '--lookup_table=' + quote_fn( os.path.join( get_lut_path( self.path() ), lf + ".cms" ) ) )

    fnargs.append( "--color_space=" + cs )


  def __init__( self, path, name, mov ):
    self.path_ = path
    self.name_ = name
    self.mov_ = mov

  def name( self ):
    return self.name_

  def path( self ):
    return self.path_

  def run( self, filename, frameRange, views, options ):

    fnargs = []
    fnargs.append( "--range=" + str( frameRange ).replace( 'x', '/' ) )

    fnargs.append( "--pixel_aspect=" + str( options.get( "pixelAspect", 1 ) ) )

    if nuke.env['NukeVersionString'] >= '6.2v2':

      lut = options.get( "lut", "linear" )
      (root, ext) = os.path.splitext( filename )
      self._add_lut( lut, ext == ".cin" or ext == ".dpx", fnargs )

    roi = options.get( "roi", None )
    dimensions = options.get( "dimensions", None )

    if roi != None and dimensions != None:


      roi_x = int( roi["x"] )
      roi_y = int( roi["y"] )
      roi_w = int( roi["w"] )
      roi_h = int( roi["h"] )

      dim_w = dimensions[ "width" ]
      dim_h = dimensions[ "height" ]

      if roi_x != 0 or roi_y != 0 or roi_w != 0 or roi_h != 0:

        roi_x = roi_x + roi_w / 2 - dim_w / 2
        roi_y = roi_y + roi_h / 2 - dim_h / 2

        fnargs.append( "--crop=%d,%d,%d,%d" % (roi_x, roi_y, roi_w, roi_h) )

    os.path.normpath( filename )

    args = []
    args.append( quote_fn( self.path() ) )

    if len( views ) > 1:

      (lfn, subs) = re.subn( "%V", views[0], filename );
      (lfn, subs) = re.subn( "%v", views[0][0], lfn );
      args.append( quote_fn( lfn ) );
      args.append( "--target_view=left" );
      args.extend( fnargs );

      (rfn, subs) = re.subn( "%V", views[1], filename );
      (rfn, subs) = re.subn( "%v", views[1][0], rfn );
      args.append( quote_fn( rfn ) );
      args.append( "--target_view=right" );
      args.extend( fnargs );

      args.append( "--stereo_view=both" );

    elif len( views ) == 1:

      (lfn, subs) = re.subn( "%V", views[0], filename );
      (lfn, subs) = re.subn( "%v", views[0][0], lfn );
      args.append( quote_fn( lfn ) );
      args.extend( fnargs );

    else:

      args.append( quote_fn( filename ) );
      args.extend( fnargs );

    args.append( "--nuke_lut=" + options.get( "lut", "" ) )
    args.append( "--nuke_fr=" + str( frameRange ) )
    args.append( "--nuke_audio=" + options.get( "audio", "" ) )

    os.spawnv( os.P_NOWAITO, self.path(), args )

  def capabilities( self ):

    ft = [ "bmp", "cin", "dpx", "dds", "exr", "sxr", "hdr", "iff", "jpg", "jpeg", "pic", "png", "psd", "r3d", "rla", "rpf", "sgi", "sgi16", "rgb", "rgb16", "tga", "tif", "tiff", "ftif", "vrimg", "yuv" ]

    if self.mov_:
      ft.append( "avi" )
      ft.append( "mov" )

    return { 
      'proxyScale': False,
      'crop': True,
      'canPreLaunch': True,
      'supportsArbitraryChannels': False,
      'maximumViews' : 2,
      'fileTypes' : ft
    }

def init_py():
  nukescripts.register( PdplayerFlipbook( get_pdplayer32_path(), "Pdplayer 32", True ) )
  nukescripts.register( PdplayerFlipbook( get_pdplayer64_path(), "Pdplayer 64", False ) )

def menu_py():
  pass
