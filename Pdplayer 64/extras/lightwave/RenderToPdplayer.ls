@name Render->Pdplayer
@asyncspawn

// LW 9.6:
get_render_suffix: fmt
{
    suffix = "";

    switch( fmt )
    {
    case 0:
    case 1:

		suffix = "001";
		break;

    case 2:
    case 3:

		suffix = "0001";
		break;

    case 4:
    case 5:

		suffix = "00001";
		break;

    case 6:
    case 7:

		suffix = "000001";
		break;

    case 8:
    case 9:

		suffix = "_001";
		break;

    case 10:
    case 11:

		suffix = "_0001";
		break;

    case 12:
    case 13:

		suffix = "_00001";
		break;

    case 14:
    case 15:

		suffix = "_000001";
		break;
    }

    return suffix;
}

/*

// LW 9.0:
get_render_suffix: fmt
{
    suffix = "";

    switch( fmt )
    {
    case 0:
    case 1:

		suffix = "001";
		break;

    case 2:
    case 3:

		suffix = "0001";
		break;

    case 4:
    case 5:

		suffix = "_001";
		break;

    case 6:
    case 7:

		suffix = "_0001";
		break;
    }

    return suffix;
}

*/

get_render_path
{
    SaveSceneCopy( "pdplayer.tmp.lws" );

    f = File( "pdplayer.tmp.lws", "r" );

    prefix = "";
    ext = "";
    fmt = 0;

    while( !f.eof() )
    {
        line = f.read();

        if( strleft( line, 20 ) == "SaveRGBImagesPrefix " )
        {
            prefix = strsub( line, 21, 65536 );
        }

        if( strleft( line, 14 ) == "RGBImageSaver " )
        {
            ext = strright( line, 5 );
            ext = strleft( ext, 4 );
        }

        if( strleft( line, 21 ) == "OutputFilenameFormat " )
        {
            fmt = integer( strsub( line, 22, 65536 ) );
        }
    }

    f.close();

    suffix = get_render_suffix( fmt );
    
    path = prefix + suffix + ext;

    return path;

}

generic
{
    pdppath = "C:\\Program Files\\pdplayer\\pdplayer.exe";
    rpath = get_render_path();

    command = "\"" + pdppath + "\" \"" + rpath + "\" --force_sequence --layer_watch_sequence";

    RenderScene();

    spawn( command );
}
