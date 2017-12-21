import sys, os
import maya.cmds as cmds
import maya.mel as mel

class Progress:
    def __init__(self, number = 100, title = None, status = None):
        self.title = title or 'Progressing...'
        self.status = status or 'Please wait a moment.'
        self.number, self.delta = number, number/100 or 1
    def start(self):
        cmds.progressWindow(t = self.title, st = self.status, pr = 0, ii = 1, max = self.number)
    def get(self):
        return cmds.progressWindow(q = 1, pr = 1)
    def set(self, value):
        cmds.progressWindow(e = 1, pr = value)
    def step(self, value):
        cmds.progressWindow(e = 1, s = value * self.delta)
    def isCancelled(self):
        return cmds.progressWindow(q = 1, ic = 1)
    def stop(self):
        cmds.progressWindow(ep = 1)

def ConvertToDotMap(Path,Size):
    Path = Path.replace('\\','/')
    fileNodes = cmds.ls(typ = 'file')
    if not os.path.isdir(Path) or not fileNodes:return
    with open(os.path.join(Path,'log.txt'),'a+') as log:
        p = Progress(number = len(fileNodes), title = u'转换中...', status = '请稍等片刻...')
        num = 0
        for i in range(p.number):
            node = fileNodes[i]
            if p.isCancelled(): break
            if not i % p.delta: p.step(1)
            if not cmds.getAttr('%s.useFrameExtension' % node):
                if max(cmds.getAttr('%s.outSizeX' % node),cmds.getAttr('%s.outSizeY' % node)) > Size:
                    inputFile = cmds.getAttr('%s.fileTextureName' % node)
                    if os.path.splitext(inputFile)[1] != '.map':
                        outputFile = os.path.join(Path,os.path.split(inputFile)[1].split('.')[0] + '.map').replace('\\','/')
                        if not os.path.isfile(outputFile):
                            mel.eval('system("imf_copy -p -r \\"%s\\" \\"%s\\"");' %(inputFile, outputFile))
                        cmds.setAttr('%s.fileTextureName' % node,outputFile,type = 'string')
                        print >> log,('"%s":("%s","%s"),' %(node,inputFile,outputFile))
                        num += 1
        if num: sys.stdout.write(u'转换 %d 个贴图文件为 ".map" 格式，操作已完成。\n' % num)
        p.stop()

def ConvertDotMapBack(Path):
    if not os.path.isfile(os.path.join(Path,'log.txt')):return
    
    log = open(os.path.join(Path,'log.txt'),'r')
    try:
        content = 'ConvertToDotMapData = {%s}' % log.read()
        exec(content)
        data = ConvertToDotMapData
    except:
        raise UserWarning, u'读取日志文件错误。\n'
    else:
        count = 0
        for node in data.keys():
            curpath = cmds.getAttr('%s.fileTextureName' % node)
            if curpath != data[node][0]:
                cmds.setAttr('%s.fileTextureName' % node, data[node][0],type = 'string')
                count += 1
        if count: sys.stdout.write(u'还原 %d 个贴图文件，操作已完成。\n' % count)
    log.close()
    #os.remove(os.path.join(Path,'log.txt'))

def ConvertToDotMapUI():
    if cmds.window('ConvertToDotMapWin', ex = 1):
        cmds.deleteUI('ConvertToDotMapWin', wnd = 1)
        cmds.windowPref('ConvertToDotMapWin', r = 1)

    win = cmds.window('ConvertToDotMapWin', w = 400, h = 80, s = 1, t = u'转换贴图到".map"格式')
    form = cmds.formLayout(ann = u'图像的尺寸长度或宽度大于所设定像素，将进行转换。')
    pathFld = cmds.textField(w = 220, h = 30, ed = 1, tx = u'请输入".map"文件存放路径')
    sizeFld = cmds.textField(w = 60, h = 30, ed = 1, tx = u'1200 像素')
    setBtn = cmds.button(l = u'转换贴图', w = 100, h = 30, 
        c = lambda arg:ConvertToDotMap(cmds.textField(pathFld, q = 1, tx = 1), int(cmds.textField(sizeFld, q = 1, tx = 1).split()[0])))
    unsetBtn = cmds.button(l = u'还原贴图', w = 100, h = 30, c = lambda arg:ConvertDotMapBack(cmds.textField(pathFld, q = 1, tx = 1)))
    cmds.formLayout(form, e = 1, af = [(pathFld, 'top', 5), (pathFld, 'left', 5),
                                       (sizeFld, 'top', 5), (sizeFld, 'right', 5),
                                       (setBtn, 'left', 5), (setBtn, 'bottom', 5),
                                       (unsetBtn, 'right', 5), (unsetBtn, 'bottom', 5)],
                                 ac = [(pathFld, 'right', 5, sizeFld), 
                                       (setBtn, 'top', 5, pathFld), (setBtn, 'right', 5, unsetBtn), 
                                       (unsetBtn, 'top', 5, pathFld)])
    cmds.setParent('..')
    cmds.showWindow(win)

ConvertToDotMapUI()
