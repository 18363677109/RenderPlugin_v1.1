#pragma warning( disable: 4996 )

#include <lwserver.h>
#include <lwhandler.h>
#include <lwhost.h>
#include <lwframbuf.h>
#include <lwio.h>

#include <string>
#include <vector>

#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <windows.h>
#include <shellapi.h>
#include <shlobj.h>

enum color_space_type
{
	cs_linear = 0,
	cs_srgb = 1
};

static std::string s_cfg_dir;

class framebuffer
{
private:

	GlobalFunc * global_;

	int color_space_;

	int width_;
	int height_;

	std::string name_;

	HANDLE hfm_;
	void * pv_;

	DWORD start_time_;

	int y_;

	framebuffer( framebuffer const & );
	framebuffer & operator=( framebuffer const & rhs );

private:

	void load( std::string const & fn );
	void save( std::string const & fn );

public:

	explicit framebuffer( GlobalFunc * global );
	~framebuffer();

	void reset();

	LWError assign( framebuffer const & rhs );

	LWError open( int width, int height );
	void close();

	void begin();
	LWError write( void const * r, void const * g, void const * b, void const * a );
	void pause();

	static void * ui_get( void * this_, unsigned long vid );
	static LWXPRefreshCode ui_set( void * this_, unsigned long vid, void * value );
};

framebuffer::framebuffer( GlobalFunc * global ): global_( global ), color_space_( cs_linear ), width_( 0 ), height_( 0 ), hfm_( 0 ), pv_( 0 ), start_time_( 0 ), y_( 0 )
{
	load( s_cfg_dir + "pdplayfb.cfg" );
}

framebuffer::~framebuffer()
{
	reset();
	save( s_cfg_dir + "pdplayfb.cfg" );
}

void framebuffer::reset()
{
	if( pv_ )
	{
		UnmapViewOfFile( pv_ );
	}

	if( hfm_ )
	{
		CloseHandle( hfm_ );
	}

	width_ = 0;
	height_ = 0;

	hfm_ = 0;
	pv_ = 0;

	y_ = 0;
}

static std::string get_buffer_name()
{
	char name[ 256 ];

	time_t tt = time( 0 );
	strftime( name, sizeof( name ), "pdplayfb_%H%M%S", localtime( &tt ) );

	char suffix[ 2 ] = { static_cast< char >( GetTickCount() % 26 + 'a' ) };
	strcat( name, suffix );

	return name;
}

LWError framebuffer::assign( framebuffer const & rhs )
{
	reset();

	color_space_ = rhs.color_space_;

	return 0;
}

LWError framebuffer::open( int width, int height )
{
	reset();

	unsigned const shm_magic = 0xFC7D001A;
	unsigned const shm_version = 0;
	unsigned const shm_header_size = 40+64+4;

	DWORD n = width * height;
	DWORD m = shm_header_size + n * 5;

	name_ = get_buffer_name();

	HANDLE hfm = CreateFileMapping( INVALID_HANDLE_VALUE, 0, PAGE_READWRITE, 0, m, name_.c_str() );

	if( hfm == 0 )
	{
		return "Could not allocate shared memory";
	}

	void * pv = MapViewOfFile( hfm, FILE_MAP_WRITE, 0, 0, 0 );

	if( pv == 0 )
	{
		CloseHandle( hfm );
		return "Could not map shared memory";
	}

	width_ = width;
	height_ = height;
	hfm_ = hfm;
	pv_ = pv;
	start_time_ = GetTickCount();

	unsigned * pw = static_cast< unsigned * >( pv );
	char * pc = static_cast< char *>( pv );

	pw[ 0 ] = shm_magic;						// magic
	pw[ 1 ] = shm_version;						// version
	pw[ 2 ] = shm_header_size;					// header size

	pw[ 3 ] = width;							// width
	pw[ 4 ] = height;							// height

	pw[ 5 ] = shm_header_size;					// color offset
	pw[ 6 ] = shm_header_size + n * 4;			// alpha offset
	pw[ 7 ] = 0;								// depth offset

	pw[ 8 ] = -1;								// frame
	pw[ 9 ] = 0;								// render time, in ms

	memset( pc + 40, 0, 64 );					// project name (ASCIIZ, 64 chars)

	pw[ 26 ] = color_space_ == cs_srgb? 2: 1;	// color space, 0: unspecified, 1: linear, 2: sRGB

	// clear color and alpha data

	memset( pc + shm_header_size, 0, n * 5 );

	// get current frame

	LWTimeInfo * pti = static_cast< LWTimeInfo * >( global_( LWTIMEINFO_GLOBAL, GFUSE_TRANSIENT ) );

	if( pti != 0 )
	{
		pw[ 8 ] = pti->frame;
	}

	// get scene name

	LWSceneInfo * psi = static_cast< LWSceneInfo * >( global_( LWSCENEINFO_GLOBAL, GFUSE_TRANSIENT ) );

	if( psi != 0 )
	{
		strncpy( pc + 40, psi->name, 63 );
		pc[ 103 ] = 0;
	}

	return 0;
}

void framebuffer::close()
{
	reset();
}

void framebuffer::begin()
{
	y_ = 0;
}

#undef min

static inline int to_cineon( double x )
{
	//double k = 0.002 / 0.600;

	//if( x <= 0.0 )
	//{
	//	return 95;
	//}

	// comparison reversed to handle NaNs better

	if( x > 0.0 )
	{
		double b = 0.0107977516232771; // pow( 10.0, (95-685)*k )

		double x2 = b + x * ( 1.0 - b );

		return std::min( 685 + static_cast< int >( log10( x2 ) * 300.0 ), 1023 );
	}
	else
	{
		return 95;
	}
}

static inline unsigned char float_to_byte( double x )
{
	if( x <= 0.0 )
	{
		return 0;
	}

	if( x >= 1.0 )
	{
		return 255;
	}

	return static_cast< unsigned char >( x * 255.9 );
}

LWError framebuffer::write( void const * r, void const * g, void const * b, void const * a )
{
	float const * bf = static_cast< float const * >( b );
	float const * gf = static_cast< float const * >( g );
	float const * rf = static_cast< float const * >( r );
	float const * af = static_cast< float const * >( a );

	unsigned * pw = static_cast< unsigned * >( pv_ );
	unsigned char * pc = static_cast< unsigned char * >( pv_ );

	unsigned mc = pw[ 5 ] / 4 + width_ * y_;
	unsigned ma = pw[ 6 ] + width_ * y_;

	for( int i = 0; i < width_; ++i )
	{
		int b2 = to_cineon( bf[ i ] );
		int g2 = to_cineon( gf[ i ] );
		int r2 = to_cineon( rf[ i ] );

		pw[ mc + i ] = ( r2 << 22 ) | ( g2 << 12 ) | ( b2 << 2 );
		pc[ ma + i ] = float_to_byte( af[ i ] );
	}

	pw[ 9 ] = GetTickCount() - start_time_; // update render time

	++y_;

	return NULL;
}

void framebuffer::pause()
{
	std::string cmdline = "--attach shm:/" + name_;

	// ShellExecute( 0, "open", "pdplayer.exe", cmdline.c_str(), 0, SW_SHOWNORMAL );

	SHELLEXECUTEINFOA sei = { sizeof( sei ) };

	sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_FLAG_NO_UI;

	sei.hwnd = 0;
	sei.lpVerb = "open";
	sei.lpFile = "pdplayer.exe";
	sei.lpParameters = cmdline.c_str();
	sei.nShow = SW_SHOWNORMAL;

	ShellExecuteExA( &sei );

	WaitForSingleObject( sei.hProcess, 1200 );
	CloseHandle( sei.hProcess );
}

enum
{
	ID_COLOR_SPACE = 0x8001
};

void * framebuffer::ui_get( void * this_, unsigned long vid )
{
	framebuffer * pfb = static_cast< framebuffer * >( this_ );

	switch ( vid )
	{
	case ID_COLOR_SPACE:
			
		return &pfb->color_space_;

	default:
			
		return 0;
	}
}

LWXPRefreshCode framebuffer::ui_set( void * this_, unsigned long vid, void * value )
{
	framebuffer * pfb = static_cast< framebuffer * >( this_ );

	switch( vid )
	{
	case ID_COLOR_SPACE:

		pfb->color_space_ = *(int*)value;
		return LWXPRC_DFLT;

    default:

		return LWXPRC_NONE;
	}
}

LWID const LWID_CSPC = LWID_( 'C', 'S', 'P', 'C' );

static LWBlockIdent s_config_id[] =
{
	{ LWID_CSPC, "ColorSpace" },
	{ 0, 0 }
};

void framebuffer::load( std::string const & fn )
{
	if ( LWFileIOFuncs * pfio = static_cast< LWFileIOFuncs * >( global_( LWFILEIOFUNCS_GLOBAL, GFUSE_TRANSIENT ) ) )
	{
		if( LWLoadState * pl = pfio->openLoad( fn.c_str(), LWIO_ASCII ) )
		{
			while( LWID lwid = LWLOAD_FIND( pl, s_config_id ) )
			{
				switch( lwid )
				{
				case LWID_CSPC:

					{
						long csp = 0;

						if( LWLOAD_I4( pl, &csp, 1 ) == 1 && ( csp == cs_linear || csp == cs_srgb ) )
						{
							color_space_ = csp;
						}
					}

					break;
				}

				LWLOAD_END( pl );
			}

			pfio->closeLoad( pl );
		}
	}
}

void framebuffer::save( std::string const & fn )
{
	if ( LWFileIOFuncs * pfio = static_cast< LWFileIOFuncs * >( global_( LWFILEIOFUNCS_GLOBAL, GFUSE_TRANSIENT ) ) )
	{
		if( LWSaveState * ps = pfio->openSave( fn.c_str(), LWIO_ASCII ) )
		{
			long csp = color_space_;

			LWSAVE_BEGIN( ps, &s_config_id[ 0 ], 1 );
				LWSAVE_I4( ps, &csp, 1 );
			LWSAVE_END( ps );

			pfio->closeSave( ps );
		}
	}
}

// Handler

XCALL_( static LWInstance )
Create( void * priv, void * /*context*/, LWError * err )
{
	framebuffer * fb = new( std::nothrow ) framebuffer( (GlobalFunc*)priv );

	if( fb == 0 )
	{
		*err = "Couldn't allocate instance data.";
	}

	return fb;
}

XCALL_( static void )
Destroy( LWInstance pv )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	delete pfb;
}

XCALL_( static LWError )
Copy( LWInstance to, LWInstance from )
{
	framebuffer * pfb = static_cast< framebuffer * >( to );
	framebuffer * pfb2 = static_cast< framebuffer * >( from );

	return pfb->assign( *pfb2 );
}

// FrameBuffer

XCALL_( static void )
Close( LWInstance pv )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	pfb->close();
}

XCALL_( static LWError )
Open( LWInstance pv, int width, int height )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	return pfb->open( width, height );
}


XCALL_( static LWError )
Begin( LWInstance pv )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	pfb->begin();
	return 0;
}

XCALL_( static LWError )
Write( LWInstance pv, void const * r, void const * g, void const * b, void const * a )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	return pfb->write( r, g, b, a );
}

XCALL_( static void )
Pause( LWInstance pv )
{
	framebuffer * pfb = static_cast< framebuffer * >( pv );
	pfb->pause();
}

// Handler activation function

XCALL_( int )
Handler( long version, GlobalFunc * global, void * local, void * /*serverData*/ )
{
	if( version != LWFRAMEBUFFER_VERSION )
	{
		return AFUNC_BADVERSION;
	}

	if( global == 0 )
	{
		return AFUNC_BADGLOBAL;
	}

	// get settings dir

	if( LWDirInfoFunc * pdi = (LWDirInfoFunc *) global( LWDIRINFOFUNC_GLOBAL, GFUSE_TRANSIENT ) )
	{
		if( char const * cfg = pdi( LWFTYPE_SETTING ) )
		{
			s_cfg_dir = std::string( cfg ) + '\\';
		}
	}

	LWFrameBufferHandler * pfbh = static_cast< LWFrameBufferHandler * >( local );

	pfbh->inst->priv = (void*)global;

	pfbh->inst->create = Create;
	pfbh->inst->destroy = Destroy;
	pfbh->inst->copy = Copy;

	pfbh->type = LWFBT_FLOAT;

	pfbh->open  = Open;
	pfbh->close = Close;
	pfbh->begin = Begin;
	pfbh->write = Write;
	pfbh->pause = Pause;

	return AFUNC_OK;
}

// Interface

static LWXPanelControl s_xctl[] =
{
	{ ID_COLOR_SPACE, "Color Space", "iPopChoice", },
	{ 0 }
};

static LWXPanelDataDesc s_xdata[] =
{
	{ ID_COLOR_SPACE, "Color Space", "integer", },
	{ 0 }
};

static char * s_color_space[] = { "Linear", "sRGB", 0 };

static LWXPanelHint s_xhint[] =
{
	XpSTRLIST( ID_COLOR_SPACE, s_color_space ),
	XpEND
};

XCALL_( int )
Interface( long version, GlobalFunc * global, void * local2, void * /*serverData*/ )
{
	if( version != LWINTERFACE_VERSION )
	{
		return AFUNC_BADVERSION;
	}

	LWInterface * local = static_cast< LWInterface * >( local2 );

	LWXPanelFuncs * xpanf = static_cast< LWXPanelFuncs * >( global( LWXPANELFUNCS_GLOBAL, GFUSE_TRANSIENT ) );

	if( xpanf == 0 )
	{
		return AFUNC_BADGLOBAL;
	}

	local->options = 0;
	local->command = 0;

	if( LWXPanelID panel = xpanf->create( LWXP_VIEW, s_xctl ) )
	{
		xpanf->hint( panel, 0, s_xhint );

		xpanf->describe( panel, s_xdata, framebuffer::ui_get, framebuffer::ui_set );

		xpanf->viewInst( panel, local->inst );

		local->panel = panel;

		return AFUNC_OK;
	}
	else
	{
		return AFUNC_BADGLOBAL;
	}
}

ServerTagInfo ServerTags[] = {

	{ "Pdplayer", SRVTAG_USERNAME | LANGID_USENGLISH },
	{ "Pdplayer", SRVTAG_USERNAME },

	{ NULL }
};

char const * pn = "PdplayerFb";

extern "C" ServerRecord ServerDesc[] =
{
   { LWFRAMEBUFFER_HCLASS, pn, Handler, ServerTags },
   { LWFRAMEBUFFER_ICLASS, pn, Interface, ServerTags },
   { NULL }
};
