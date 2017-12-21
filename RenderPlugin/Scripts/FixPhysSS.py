# -*- coding: utf-8 -*-

import maya.cmds as cmds

def FixPhysSS():
    curPanel = cmds.getPanel(wf = 1)
    try:
        cam = cmds.modelEditor(curPanel, q = 1, camera = 1)
    except RuntimeError:
        cmds.error('//«Î—°‘Ò»˝Œ¨ ”¥∞') 
    else:
        try:
            cmds.editRenderLayerAdjustment(cam + '.miEnvironmentShader')
            cmds.editRenderLayerAdjustment(cam + '.miLensShader')
        except RuntimeError:
            cmds.error('//«Î—°‘Ò∑«ƒ¨»œ‰÷»æ≤„')
        else:
            PSK_List = cmds.ls(typ = 'mia_physicalsky')
            if len(PSK_List) != 0:
                for x in PSK_List:
                    if cmds.isConnected(x + '.message', cam + '.miEnvironmentShader'):
                        cmds.disconnectAttr(x + '.message', cam + '.miEnvironmentShader')
                        break
            MES_List = cmds.ls(typ = 'mia_exposure_simple')
            if len(MES_List) != 0:
                for y in MES_List:
                    if cmds.isConnected(y + '.message', cam + '.miLensShader'):
                        cmds.disconnectAttr(y + '.message', cam + '.miLensShader')
                        break

FixPhysSS()