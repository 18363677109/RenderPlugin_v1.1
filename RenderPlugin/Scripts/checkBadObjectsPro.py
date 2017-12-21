import maya.cmds as cmds

def checkBadObjects(strict = 0):
	def check(connections, *cases):
		result = False
		sources = connections[::2]
		destinations = connections[1::2]
		for case in cases:
			if [x for x in sources if case in x]:
				result = True
				break
			elif [x for x in destinations if case in x]:
				result = True
				break
		return result

	global BadObjects
	BadObjects = []
	objects = cmds.ls(s = 1)
	amount = 0
	count = 0
	num = len(objects)
	cmds.progressWindow(t = u'检测中...', pr = amount, ii = 1)
	cmds.scrollField('ScrollText', e = 1, cl = 1)
	mytext = u'检测结果'.center(57, '-') + '\n'
	cmds.scrollField('ScrollText', e = 1, it = mytext, ip = 0)
	cmds.editRenderLayerGlobals(crl = 'defaultRenderLayer')
	feedBackCaseA, feedBackCaseB = [], []
	for object in objects:
		if cmds.nodeType(object) in ('mesh', 'nurbsSurface'):
			connections = cmds.listConnections(object, c = 1, t = 'shadingEngine')
			if not connections:
				connections = cmds.listConnections(object, c = 1)
				if (connections and not check(connections, 'groupParts', 'outMesh', 'worldMesh', 'worldSpace')) or strict:
					if not cmds.ls(object, io = 1):
						BadObjects.append(object)
						addText = u'>>> %s 没有和SG节点连接\n' % object
						feedBackCaseA.append(addText)
			elif check(connections, 'compInstObjGroups'):
				BadObjects.append(object)
				addText = u'>>> %s 与SG节点之间可能存在异常连接\n' % object
				feedBackCaseB.append(addText)
		count += 1
		if count*50 % num == 0:
			amount += 2
			cmds.progressWindow(e = 1, pr = amount)
		elif count == num:
			amount = 100
			cmds.progressWindow(e = 1, pr = amount)
		if cmds.progressWindow(q = 1, ic = 1):
			break
		if cmds.progressWindow(q = 1, pr = 1) >= 100:
			break
	cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseA), ip = 0)
	cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseB), ip = 0)
	cmds.progressWindow(ep = 1)

def selectBadObjects():
	try:
		selectedText = cmds.scrollField('ScrollText', q = 1, sl = 1)
		if selectedText and '-' not in selectedText:
			splitedText = [x for x in selectedText.split() if '\\' not in repr(x) and '>' not in x]
			cmds.select(splitedText, r = 1)
		elif not selectedText:
			cmds.select(BadObjects, r = 1)
	except:
		pass

def fixBadObjects():
	cmds.editRenderLayerGlobals(crl = 'defaultRenderLayer')
	objects = cmds.ls(sl = 1)
	if objects:
		addText = u'修复结果'.center(57, '-') + '\n'
		cmds.scrollField('ScrollText', e = 1, it = addText, ip = 0)
		feedBackCaseA, feedBackCaseB = [], []
		for object in objects:
			connections = cmds.listConnections(object, c = 1,p = 1, t = 'shadingEngine')
			if not connections:
				cmds.sets(object, fe = 'initialShadingGroup', e = 1)
				addText = u'>>> %s 被赋予默认lamber1材质\n' % object
				feedBackCaseA.append(addText)
			else:
				check = [x for x in connections[::2] if 'compInstObjGroups' in x]
				if check:
					id = connections.index(check[0])
					cmds.disconnectAttr(connections[id], connections[id + 1])
					addText = u'>>> %s 断开可能引发错误的连接\n' % object
					feedBackCaseB.append(addText)
		cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseA), ip = 0)
		cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseB), ip = 0)

def checkBadObjectsUI():
	if cmds.window('checkBadObjectsWin', ex = 1):
		cmds.deleteUI('checkBadObjectsWin', wnd = 1)
		cmds.windowPref('checkBadObjectsWin', r = 1)

	mytext = u'说 明'.center(58, '-') + '\n' +\
			 u'用途：\n' +\
			 u'检测和修复未连接SG节点的物体以及与SG节点之间可能存在异常连接的物体。\n' +\
			 u'修复方案：\n' +\
			 u'1.对于未连接SG节点的物体，将赋予其默认lamber1材质。\n' +\
			 u'2.对于存在异常连接的物体，将尝试断开可能引发错误的连接。\n' +\
			 u'注意事项：\n' +\
			 u'1.请在使用修复功能前将文件备份，并且认真确认是否`必须`修复。\n' +\
			 u'2.对使用本插件造成的任何意外结果与损失，不承担任何责任与义务。\n\n' +\
			 u'2012年7月19日'.rjust(58, ' ') + '\n'

	cmds.window('checkBadObjectsWin', w = 460, h = 260, t = u"检测物体... v1.0")
	form = cmds.formLayout()
	textF = cmds.scrollField('ScrollText', w = 200, h = 200, ww = 1, ed = 0, tx = mytext)
	checkB = cmds.button(l = u'检测', h = 35, c = 'checkBadObjects()')
	cmds.popupMenu()
	cmds.menuItem(l = u'严格检测', c = 'checkBadObjects(strict = 1)')
	selectB = cmds.button(l = u'选择', w = 120, h = 35, c = 'selectBadObjects()')
	fixB = cmds.button(l = u'修复', w = 120, h = 35, c = 'fixBadObjects()')
	cmds.setParent('..')
	cmds.formLayout(form, e = 1, af =[(textF, 'top', 5), (textF, 'left', 5), (textF, 'right', 5),
									  (checkB, 'left', 5), (checkB, 'bottom', 5),
									  (fixB, 'right', 5), (fixB, 'bottom', 5),
									  (selectB, 'bottom', 5)],
								 ac =[(textF, 'bottom', 5, checkB), (textF, 'bottom', 5, selectB), (textF, 'bottom', 5, fixB),
									  (checkB, 'right', 5, selectB), (selectB, 'right', 5, fixB)])
	cmds.showWindow('checkBadObjectsWin')

checkBadObjectsUI()
