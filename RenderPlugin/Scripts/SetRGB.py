# -*- coding: utf-8 -*-
import maya.cmds as cmds

def RGBUI():
    if cmds.window('RGB_UI', ex = 1):
        cmds.deleteUI('RGB_UI')
    cmds.window('RGB_UI', t = "QDISA-RGB_Tool_v1.1", s = 0,widthHeight=(300,120))
    cmds.rowColumnLayout(numberOfRows=1)
    cmds.button('ºì', h = 50, w = 50, bgc = (1,0,0), c = 'SetMatte("R")')
    cmds.button('»Æ', h = 50, w = 50, bgc = (1,1,0), c = 'SetMatte("Y")')
    cmds.button('ÂÌ', h = 50, w = 50, bgc = (0,1,0), c = 'SetMatte("G")')
    cmds.button('Çå', h = 50, w = 50, bgc = (0,1,1), c = 'SetMatte("C")')
    cmds.button('À¶', h = 50, w = 50, bgc = (0,0,1), c = 'SetMatte("B")')
    cmds.button('×Ï', h = 50, w = 50, bgc = (1,0,1), c = 'SetMatte("M")')
    cmds.button('ºÚ', h = 50, w = 80, bgc = (0,0,0), c = 'SetMatte("BK")')
    cmds.button('°×', h = 50, w = 80, bgc = (1,1,1), c = 'SetMatte("W")')
    cmds.setParent(top = 1)
    cmds.setParent('..')

    cmds.showWindow('RGB_UI')

def SetMatte(mode):
    data = {'R':(1,0,0,1),'Y':(1,1,0,1),'G':(0,1,0,1),'C':(0,1,1,1),'B':(0,0,1,1),'M':(1,0,1,1),'BK':(0,0,0,0),'W':(1,1,1,1)}

    Item = cmds.ls(sl = 1)
    if mode in data.keys():
        if not cmds.objExists('Matte_%s' % mode):
            Mat = cmds.shadingNode('surfaceShader',asShader = 1, n = 'Matte_%s' % mode)
            SG = cmds.sets(r = 1, nss = 1, em = 1, n = Mat + 'SG')
            cmds.connectAttr('%s.outColor' % Mat, '%s.surfaceShader' % SG, f = 1)
        else:
            Mat = 'Matte_%s' % mode
            SG = (cmds.listConnections('%s.outColor' % Mat))[0]
        cmds.setAttr('%s.outColor' % Mat, data[mode][0], data[mode][1], data[mode][2], typ = 'double3')
        cmds.setAttr('%s.outMatteOpacity' % Mat, data[mode][3], data[mode][3], data[mode][3], typ = 'double3')
        cmds.select(Item, r = 1)
        cmds.sets(e = 1, forceElement = SG)
