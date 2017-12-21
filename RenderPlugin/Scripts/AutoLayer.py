# -*- coding: utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel
import os

def AL_CheckFileMtime(destPath, srcPath):
    '''检测文件修改时间是否相同'''
    
    if os.path.getmtime(destPath) == os.path.getmtime(srcPath):
        return False
    else:
        return True

def FixZD():
    '''调节Z通道'''

    CAM = cmds.ls(sl = 1)
    CAMSP = cmds.ls(cmds.listRelatives(CAM), ca = 1) if CAM else None
    CRL = cmds.editRenderLayerGlobals(q = 1, crl = 1)
    SG  = cmds.listConnections('%s.shadingGroupOverride' % CRL, d = 0, s = 1)
    SG  = SG[0] if SG else None
    History = cmds.listHistory(SG) if SG else None
    SI = cmds.ls(History, typ = 'samplerInfo')
    SI  = SI[0] if SI else None
    MD = cmds.ls(History, typ = 'multiplyDivide')
    MD  = MD[0] if MD else None
    SR = cmds.ls(History, typ = 'setRange')
    SR  = SR[0] if SR else None

    if all([CAM, CAMSP, CRL, SG, SI, MD, SR]):
        Action = True
    elif globals().has_key('ZDEPTH_LAYER_NODES') and all([CAM, CAMSP]):
        SI, MD, SR, Mat, SG = ZDEPTH_LAYER_NODES
        Action = True
    else:
        Action = False
    
    if Action:
        if not cmds.isConnected('%s.pointCameraZ' % SI, '%s.input1X' % MD):
            cmds.error('//请选择Z通道层和渲染用摄像机\n')
        if not cmds.isConnected('%s.outputX' % MD, '%s.valueX' % SR):
            cmds.error('//请选择Z通道层和渲染用摄像机\n')
        CAM = cmds.listRelatives(CAMSP, p = 1)

        N = (cmds.spaceLocator(n = 'CAM_NP'))[0]
        cmds.transformLimits(N, tx = (0,0), etx = (1,1),
                                       ty = (0,0), ety = (1,1),
                                       rx = (0,0), erx = (1,1),
                                       ry = (0,0), ery = (1,1),
                                       rz = (0,0), erz = (1,1))
        cmds.setAttr('%s.overrideEnabled' % N, 1)
        cmds.setAttr('%s.overrideColor' % N, 16)
        cmds.setAttr('%s.tz' % N, -1)
        cmds.parent(N, CAM[0], r = 1)

        F = (cmds.spaceLocator(n = 'CAM_FP'))[0]
        cmds.transformLimits(F, tx = (0,0), etx = (1,1),
                                       ty = (0,0), ety = (1,1),
                                       rx = (0,0), erx = (1,1),
                                       ry = (0,0), ery = (1,1),
                                       rz = (0,0), erz = (1,1))
        cmds.setAttr('%s.overrideEnabled' % F, 1)
        cmds.setAttr('%s.overrideColor' % F, 1)
        cmds.setAttr('%s.tz' % F, -20)
        cmds.parent(F, CAM[0], r = 1)

        cmds.setAttr('%s.input2Y' % MD, -1)
        cmds.setAttr('%s.input2Z' % MD, -1)
        cmds.connectAttr('%s.tz' % N, '%s.input1Y' % MD, f = 1)
        cmds.connectAttr('%s.tz' % F, '%s.input1Z' % MD, f = 1)

        if not cmds.isConnected('%s.outputY' % MD, '%s.oldMinX' % SR):
            cmds.connectAttr('%s.outputY' % MD, '%s.oldMinX' % SR, f = 1)
        if not cmds.isConnected('%s.outputZ' % MD, '%s.oldMaxX' % SR):
            cmds.connectAttr('%s.outputZ' % MD, '%s.oldMaxX' % SR, f = 1)

    else:
        cmds.error('//请选择Z通道层和渲染用摄像机\n')

def FixPhysSS():
    '''修复物理灯光'''

    CamList = cmds.ls(ca = 1)
    for cam in CamList:
        try:
            cmds.editRenderLayerAdjustment(cam + '.miEnvironmentShader')
            cmds.editRenderLayerAdjustment(cam + '.miLensShader')
        except RuntimeError:
            cmds.error('//请选择非默认渲染层')
            break
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

def AL_GetList():
    '''得到场景中分层所需的列表'''

    global AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List
    AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List = [],[],[],[],[]
    Set_List = cmds.ls(typ = 'objectSet')
    for x in Set_List:
        if 'CH_' in x:
            AL_CH_List.append(x)
        elif 'BG_' in x:
            AL_BG_List.append(x)
        elif 'PROP' in x:
            AL_PROP_List.append(x)
        elif 'LT_' in x:
            AL_LT_List.append(x)
    AL_LT_List = [cmds.listRelatives(x, p = 1)[0] for x in cmds.ls(lt = 1) if not cmds.referenceQuery(x, inr = 1)]
    AL_CAM_List = mel.eval('listTransforms -ca')

def AL_CrtLayer(mode,auto = 0):
    '''创建分层'''

    if mode == 'CH':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_LT_List != []:
                cmds.editRenderLayerMembers(name, AL_LT_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'CH_AO':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'CH_NM':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'CH_FN':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'BG':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_BG_List != []:
                cmds.editRenderLayerMembers(name, AL_BG_List, nr = 1)
            if AL_LT_List != []:
                cmds.editRenderLayerMembers(name, AL_LT_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'BG_AO':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_BG_List != []:
                cmds.editRenderLayerMembers(name, AL_BG_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'ZD':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_BG_List != []:
                cmds.editRenderLayerMembers(name, AL_BG_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'SD':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_BG_List != []:
                cmds.editRenderLayerMembers(name, AL_BG_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_LT_List != []:
                cmds.editRenderLayerMembers(name, AL_LT_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'SSS':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

    elif mode == 'RGB':
        name = cmds.createRenderLayer(n = mode, e = 1, mc = 1)
        if auto:
            if AL_CH_List != []:
                cmds.editRenderLayerMembers(name, AL_CH_List, nr = 1)
            if AL_PROP_List != []:
                cmds.editRenderLayerMembers(name, AL_PROP_List, nr = 1)
            if AL_CAM_List != []:
                cmds.editRenderLayerMembers(name, AL_CAM_List, nr = 1)
        AL_AdjLayer(mode,name)

def AL_AdjLayer(mode,name):
    '''调整分层'''

    if mode == 'CH':
        try:
            cmds.ls(typ = 'mia_physicalsky')
        except:
            pass
        else:
            if cmds.ls(typ = 'mia_physicalsky') != []:
                cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather')
                cmds.setAttr('miDefaultOptions.finalGather', 1)
    
    elif mode == 'CH_AO':
        mel.eval('renderLayerBuiltinPreset occlusion %s;' % name)
        SG = (cmds.listConnections('%s.shadingGroupOverride' % name, d = 0, s = 1))[0]
        Mat = (cmds.listConnections('%s.surfaceShader' % SG, d = 0, s = 1))[0]
        Occ = (cmds.listConnections('%s.outColor' % Mat, d = 0, s = 1))[0]
        cmds.setAttr('%s.samples' % Occ, 64)
        cmds.setAttr('%s.max_distance' % Occ, 10)
        FixPhysSS()

    elif mode == 'CH_NM':
        mel.eval('renderLayerBuiltinPreset normal %s;' % name)
        FixPhysSS()

    elif mode == 'CH_FN':
        SI = cmds.shadingNode('samplerInfo',au = 1)
        Ramp = cmds.shadingNode('ramp',at = 1)
        Mat = cmds.shadingNode('surfaceShader',asShader = 1)
        SG = cmds.sets(r = 1, nss = 1, em = 1, n = Mat + 'SG')
        cmds.connectAttr('%s.facingRatio' % SI, '%s.uvCoord.vCoord' % Ramp, f = 1)
        cmds.connectAttr('%s.outColor' % Ramp, '%s.outColor' % Mat, f = 1)
        cmds.connectAttr('%s.outColor' % Mat, '%s.surfaceShader' % SG, f = 1)

        cmds.setAttr('%s.interpolation' % Ramp, 3)
        cmds.removeMultiInstance('%s.colorEntryList[2]' % Ramp, b = 1)
        cmds.setAttr('%s.colorEntryList[1].position' % Ramp, 0.6)
        cmds.setAttr('%s.colorEntryList[1].color' % Ramp, 0, 0, 0,typ = 'double3')
        cmds.setAttr('%s.colorEntryList[0].position' % Ramp, 0)
        cmds.setAttr('%s.colorEntryList[0].color' % Ramp, 1, 1, 1,typ = 'double3')

        mel.eval('hookShaderOverride("%s", "", "%s")' % (name,Mat))
        FixPhysSS()

    elif mode == 'BG':
        try:
            cmds.ls(typ = 'mia_physicalsky')
        except:
            pass
        else:
            if cmds.ls(typ = 'mia_physicalsky') != []:
                cmds.editRenderLayerAdjustment('miDefaultOptions.finalGather')
                cmds.setAttr('miDefaultOptions.finalGather', 1)

    elif mode == 'BG_AO':
        mel.eval('renderLayerBuiltinPreset occlusion %s;' % name)
        SG = (cmds.listConnections('%s.shadingGroupOverride' % name, d = 0, s = 1))[0]
        Mat = (cmds.listConnections('%s.surfaceShader' % SG, d = 0, s = 1))[0]
        Occ = (cmds.listConnections('%s.outColor' % Mat, d = 0, s = 1))[0]
        cmds.setAttr('%s.samples' % Occ, 64)
        cmds.setAttr('%s.max_distance' % Occ, 10)
        FixPhysSS()

    elif mode == 'ZD':
        mel.eval('renderLayerBuiltinPreset linearDepth %s;' % name)
        FixPhysSS()

    elif mode == 'SSS':
        FixPhysSS()

    elif mode == 'SD':
        FixPhysSS()

    elif mode == 'RGB':
        mel.eval('renderLayerEditorSelectObjects RenderLayerTab %s;' % name)
        SetMatte('BK')
        cmds.select(cl = 1)
        FixPhysSS()

def AL_CheckList():
    '''检查列表变量'''

    try:
        AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List
    except:
        AL_GetList()

def AL_ClearList():
    '''清理列表变量'''

    global AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List
    del AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List

def AutoLayer():
    '''自动分层 V0.4'''

    global AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List

    AL_CheckList()

    Layers = ('CH','CH_AO','CH_NM','CH_FN','BG','BG_AO','ZD','SD','SSS','RGB')

    for x in Layers:
        AL_CrtLayer(x, auto = 1)

    del AL_CH_List, AL_BG_List, AL_PROP_List, AL_LT_List, AL_CAM_List
