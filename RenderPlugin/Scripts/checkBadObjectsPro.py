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
	cmds.progressWindow(t = u'�����...', pr = amount, ii = 1)
	cmds.scrollField('ScrollText', e = 1, cl = 1)
	mytext = u'�����'.center(57, '-') + '\n'
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
						addText = u'>>> %s û�к�SG�ڵ�����\n' % object
						feedBackCaseA.append(addText)
			elif check(connections, 'compInstObjGroups'):
				BadObjects.append(object)
				addText = u'>>> %s ��SG�ڵ�֮����ܴ����쳣����\n' % object
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
		addText = u'�޸����'.center(57, '-') + '\n'
		cmds.scrollField('ScrollText', e = 1, it = addText, ip = 0)
		feedBackCaseA, feedBackCaseB = [], []
		for object in objects:
			connections = cmds.listConnections(object, c = 1,p = 1, t = 'shadingEngine')
			if not connections:
				cmds.sets(object, fe = 'initialShadingGroup', e = 1)
				addText = u'>>> %s ������Ĭ��lamber1����\n' % object
				feedBackCaseA.append(addText)
			else:
				check = [x for x in connections[::2] if 'compInstObjGroups' in x]
				if check:
					id = connections.index(check[0])
					cmds.disconnectAttr(connections[id], connections[id + 1])
					addText = u'>>> %s �Ͽ������������������\n' % object
					feedBackCaseB.append(addText)
		cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseA), ip = 0)
		cmds.scrollField('ScrollText', e = 1, it = ''.join(feedBackCaseB), ip = 0)

def checkBadObjectsUI():
	if cmds.window('checkBadObjectsWin', ex = 1):
		cmds.deleteUI('checkBadObjectsWin', wnd = 1)
		cmds.windowPref('checkBadObjectsWin', r = 1)

	mytext = u'˵ ��'.center(58, '-') + '\n' +\
			 u'��;��\n' +\
			 u'�����޸�δ����SG�ڵ�������Լ���SG�ڵ�֮����ܴ����쳣���ӵ����塣\n' +\
			 u'�޸�������\n' +\
			 u'1.����δ����SG�ڵ�����壬��������Ĭ��lamber1���ʡ�\n' +\
			 u'2.���ڴ����쳣���ӵ����壬�����ԶϿ�����������������ӡ�\n' +\
			 u'ע�����\n' +\
			 u'1.����ʹ���޸�����ǰ���ļ����ݣ���������ȷ���Ƿ�`����`�޸���\n' +\
			 u'2.��ʹ�ñ������ɵ��κ�����������ʧ�����е��κ�����������\n\n' +\
			 u'2012��7��19��'.rjust(58, ' ') + '\n'

	cmds.window('checkBadObjectsWin', w = 460, h = 260, t = u"�������... v1.0")
	form = cmds.formLayout()
	textF = cmds.scrollField('ScrollText', w = 200, h = 200, ww = 1, ed = 0, tx = mytext)
	checkB = cmds.button(l = u'���', h = 35, c = 'checkBadObjects()')
	cmds.popupMenu()
	cmds.menuItem(l = u'�ϸ���', c = 'checkBadObjects(strict = 1)')
	selectB = cmds.button(l = u'ѡ��', w = 120, h = 35, c = 'selectBadObjects()')
	fixB = cmds.button(l = u'�޸�', w = 120, h = 35, c = 'fixBadObjects()')
	cmds.setParent('..')
	cmds.formLayout(form, e = 1, af =[(textF, 'top', 5), (textF, 'left', 5), (textF, 'right', 5),
									  (checkB, 'left', 5), (checkB, 'bottom', 5),
									  (fixB, 'right', 5), (fixB, 'bottom', 5),
									  (selectB, 'bottom', 5)],
								 ac =[(textF, 'bottom', 5, checkB), (textF, 'bottom', 5, selectB), (textF, 'bottom', 5, fixB),
									  (checkB, 'right', 5, selectB), (selectB, 'right', 5, fixB)])
	cmds.showWindow('checkBadObjectsWin')

checkBadObjectsUI()
