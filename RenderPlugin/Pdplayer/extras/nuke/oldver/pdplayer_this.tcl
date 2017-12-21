proc pdplayer_this {node first last incr} {
    set filename [filename $node]
    if {$filename==""} {error "Can't flipbook this node"}

    # fix filenames for local system (ie add drive letter on windows):
    set filename [file normalize [filename_fix $filename]]

    set pa [value $node.actual_format.pixel_aspect]

    exec "C:/Program Files/pdplayer/pdplayer.exe" $filename "--range=$first-$last/$incr" "--pixel_aspect=$pa" &
}
