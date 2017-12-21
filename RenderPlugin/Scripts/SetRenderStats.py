from functools import partial
import maya.cmds as cmds
import sys

def SetRenderStat(mode, *args):
    LStats = ('castsShadows', 'receiveShadows', 'motionBlur', 'primaryVisibility', 'smoothShading', 'visibleInReflections', 'visibleInRefractions', 'doubleSided')
    RStats = ('miTransparencyCast', 'miTransparencyReceive', 'miReflectionReceive', 'miRefractionReceive', 'miFinalGatherCast', 'miFinalGatherReceive')
    items = cmds.ls(sl = 1, tr = 1)
    items = cmds.filterExpand(items, ex = 1, sm = 12) if items else None
    items = cmds.listRelatives(items, s = 1) if items else None
    items = list(set(items)) if items else None
    if not items:
        cmds.warning('// No Shapes Found.\n')
        return
    if mode == 'L':
        for item in items:
            for id in range(len(LStats)):
                cmds.setAttr('%s.%s' % (item, LStats[id]), cmds.checkBox('RenderStatsLCB0%s' % id, q = 1, v = 1))
    elif mode == 'R':
        for item in items:
            for id in range(len(RStats)):
                cmds.setAttr('%s.%s' % (item, RStats[id]), cmds.checkBox('RenderStatsRCB0%s' % id, q = 1, v = 1))

    sys.stdout.write('// Done.\n')

def SetRenderStatsUI():
    if cmds.window('SetRenderStatsWin', q = 1, ex = 1):
        cmds.deleteUI('SetRenderStatsWin')

    cmds.window('SetRenderStatsWin', s = 0, w = 480, t = 'Render Stats Tool')
    cmds.rowColumnLayout(nc = 2)

    cmds.frameLayout(l = 'Render Stats', w = 150, mh = 3, mw = 5)
    cmds.columnLayout(adj = 1)
    LLabels = ('Casts Shadows', 'Receive Shadows', 'Motion Blur', 'Primary Visibility', 'Smooth Shading', 'Visible In Reflections', 'Visible In Refractions', 'Double Sided')
    for id in range(len(LLabels)):
        cmds.checkBox('RenderStatsLCB0%s' % id, l = LLabels[id], v = 1)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(l = 'Mental Ray', w = 150, mh = 3, mw = 5)
    cmds.columnLayout(adj = 1)
    RLabels = ('Visible In Transparency', 'Transmit Transparency', 'Trace Reflection', 'Transmit Refraction', 'Final Gather Cast', 'Final Gather Receive')
    for id in range(len(RLabels)):
        cmds.checkBox('RenderStatsRCB0%s' % id, l = RLabels[id], v = 1)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.button(l = 'Set Selected', h = 35, c = partial(SetRenderStat, 'L'))
    cmds.button(l = 'Set Selected', h = 35, c = partial(SetRenderStat, 'R'))
    cmds.setParent(top = 1)
    cmds.setParent('..')

    cmds.showWindow('SetRenderStatsWin')

SetRenderStatsUI()
