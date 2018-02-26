 #******************************************aboutcg python教程*******************************************************

aboutcg账号 changjiang171 bigbang

 场景过大 比如将球的xyz位移值为400万 会发现球已经不是球了  maya的容差值已经不能很好的控制模型了 所以软件里 模型不能过大或过小

#字符串 用 str   mel里是“”号表示 而py里可以用 'wwe' "abc"   '''qdisa'''  单引号 双引号 或三引号 来表示 是为了方便嵌套 单引号嵌套双引号
#双引号嵌套单引号等等  如果 有汉字的话 前头要加一个u   u'牛逼' 意思是utf-8编码
数与字符串
a = 1
b = 3.14
c = "changjiang"

变量与标识符
变量的交换
a = 10
b =22
a,b = b,a 

变量的赋值
a = 1  #将1这个常量 赋予a 这个变量

from pymel.core import *         #*是所有的意思 意思是导入所有 
ls(sl=1)           #或ls(sl=True)  这就是mel的列出所选择的在py中的写法   
# mel里 string $sel=`ls -sl`;
 selected = ls(sl=1) # python中就可以

#mel  string $sel[]=`listRelatives -q`;
selected[1].getShape()
#也可以下面这样
selected = ls(sl=1)[0].getShape()  #得到选择的物体的shape节点

# 行    ·断行和连行 ·缩进
a=1 b=2 c=3 d=4 这样会出错  
要么就下面这样每次赋值一行  
a=1
b=2 
c=3 
d=4
要么就分号隔开
a=1;b=2;c=3;d=4
#如果一行特别的长 就像下面这样 ·断行和连行  用\ 反斜线断开 方便书写
myNameIs = "my name is changjiang,and\
i am a good man"
#·缩进
for i in range(10):   #下一行会自动缩进4 space
    if(i>5):    #这一句和下面的平级，结果就会奇怪   缩进一个tab 表示 下面那行是下一级
        print(i+1)  #所以说 py对缩进较敏感

#表达式   ·运算符
1+1 #常量之间

a=1 
b=2
a+b #变量之间

2 in [1,3,5,7,9]  #测试2这个数在不在 13579这个列表里
# Result: False #    结果为假 并不在里面
2 not in  [1,3,5,7,9]
# Result: True # 

# 控制流 if用的概率极高  while循环常用  for循环很常用    break  continue
#mel版本写法
int $i = 55;
if($i>100)
{print "big";}
elif ($i>50)
{print "middle";}
else:
{print "small";}

#python版本写法  写起来很简单很舒服
i=55
if i >100:
    print 'big'
elif i>50:
    print 'middle'
else:
    print 'small'

#控制流 for 
#mel的写法
for($i=0;$i<100;$i++)

#python写法 
for i in range(100):  #加了冒号就自动带缩进   range()其实是占内存比较多的一种算法，意思是从1-100都干什么事  
    if i %2==0:      #如果只想得到偶数序列    如果想达到奇数的话  就写 if i %2!=0 或者 if i %2==1
        print i

for i in [1,5,0,48,115]：
    if i %1!=0:
        print i

from pymel.core import *  # *的意思是所有
for i in ((0,1,0),(1,0,0),(0,0,1)):
    circle(nr=i)
# 这就是pymel 语法是py 但是命令都是mel    
    

#元组 （） 内容写入后，不能被更改 信息很安全 

#控制流    while 
# 类似于for循环   for是一个有限的循环100次 1000次等等  while会不停的侦测一个东西是否达到条件，倾向于不可数的次数的循环 （while写的出无限循环）
n=0
while n <10:
    n=n+1
    print n
    if n>5:
        break  #如果大于5 就打断循环
    if n<5:
        continue #如果小于5就忽略以下脚本
    print ("hello world!")

# 实战案例猜数字脚本   
import random
number = int(random.uniform(1,100))
n=0
while True:
    n=n+1
    i = int (input('i guess the number is'))
    if i > number:
        print('a little bigger')
    if i < number:
        print('a little smaller')
    if i == number:
        print('congtatulations! \n','you have geuused',n,'times!')
        break

# ************************************函数
·什么是函数 ·定义函数 ·函数的参数 ·函数的注释 ·函数中的变量 ·return ·递归 

·什么是函数
#这里的函数意思是一种封包，类似于mel里的porc，global proc 
len 和 range 等就可以说是内置好的函数，除此之外当然可以自制函数  

·定义函数的参数 
def helloWorld():
    print('hello world ! ')

helloWorld ## Result: <function helloWorld at 0x000000003D0AD978> #   直接helloWorld 它会告诉说你在内存中占用的位置】
helloWorld()   #加上小括号，这才是正确的写法  这就是一个没有参数也没有变量的函数 

def bijioadaxiao(a,b):
    if a > b:
        print (a,"is bigger than",b)
    if a == b:
        print (a,"is same as",b)

bijioadaxiao (3.48594*7.8,2.66*4.524+8)       

#注释 
中文注释写  # coding = utf-8
内容里这么些    print (u'中文')

#实战阶乘
#fn(n) = n!    fn(4) = 4*3*2*1       fn(1) = 1

def fn(n):
    result = 1
    for i in range(n):
        result *= (i+1) 
    return result 
fn(3)
# Result: 6 # 

#递归  逻辑更清晰化，是逻辑的循环而不是语法的循环 
#fn(n) = n*fn(n-1)
def fn(n):
    if n > 1:
        return (n*fn(n-1))
    in n == 1:
        return 1
    else:
        print 'error!'
fn(10)


# 数据结构 
·list  ·tuple  ·dict  ·str  ·set

list1 = [1,3,4,2.55,'black',[12,6,8,822],(1.5,6,80)]  #列表可以有整数，浮点，字符串，列表，元组
list1[-1]  #就是列表里最后一个
#切片
·t[0]       #第一个
·t[-1]      #最后一个
·t[1:3]     #第一个到第三个之间
·t[1:-1]    #第二个开始至倒数第二个结束
·t[:]       #全部
list1[0:5:2]  #从头开始到第五个 每2个取一次  在类似maya建模 等需要隔物取值的场合用处较多      list[：：2]从头到尾每隔2取值 


frpm pymel.core import *
select(ls(sl=1) [::2])   #建了很多盒子 这样可以隔着选    #这就是切片对数据的操作


·tuple 和list的区别
list1 = [1,2,3]
tuple1 = (4,5,6)

lsit1[0] = 10  #这是给数组里的第一个从新赋值  可以赋值
tuple1[0] = 10   #会发现报错，元组不可以被改变

#dict 就是字典 
dict = {'a':'this','b':'that' }          #一个关键字对应一个结果
dict[0]   #这样访问时不对的
dict['a']  #像这样直接访问关键字 
len(dict)  #测量字典长度

# 实战案例 翻译机 
#在做一些数据库时 dict时非常有用的 

__author__ = 'NeroBlack'
DICT = {
    'i':u'我',
    'my':u'我的',
    'is':u'是',
    'name':u'名字',
    'that':u'那',
    'like':u'喜欢',
    'computergraphic':u'计算机艺术',
    'especially':u'尤其是',
    'learning':u'学习',
    'english':u'英语',
    'life':u'生活',
   }
TEXT = '''My name is NeroBlack
I like computergraphic especially vfx
I like learning English
That is my life'''
def translateWord(word):
    conv = word.lower() # 全变成小写
    if conv not in DICT:     #这是py接近自然语言的地方  not in 表示 word 不在dict里
        return word
    return DICT[conv]
def translateSentence(sentence):
    words = sentence.split(' ')
    chineseSentence = ''
    for w in words:
        chineseSentence += translateWord(w)
    return chineseSentence
def translateText(text):
    sentences = text.split('\n')
    translateTexts = ''
    for s in sentences:
        translateTexts += translateSentence(s)
        translateTexts += '\n'
    return translateTexts
print(translateText(TEXT))


#数据结构   string
print(help(str))   #会的到很长的帮助文档 常用的有 

s = 'changjiang'
print(len(s))   #测量长度
print(s.split('j'))    #用j来分割
print(s[1:-1])         #切片
print(s.lower())        #小写 
print(s.upper())        #大写
print(s.find('j'))      #查找字符所在的位置


·str测试     
获取此路径中的版本号
d:\proj\cj\shot\bl\scene\v001.mb

path = r'd:\proj\cj\shot\bl\scene\v001.mb'   # r前缀取消转义符产生的误解 让转义符失去作用
number = int(path.split('\\')[-1][1;-3])
print(str(number).zfill(3))
#此案例几乎包含了 string 最常用的一些玩法  

#数据结构   set 
·交集 ·并集 ·差集 
A = {1,3,4,6,8,9,11}
B = {2,3,4,7,11,9}
print(A & B)  # 求交集 &
print(A | B)  # 并集，全集  |  回车上头的竖线
print(A - B)  #差集（先后有影响）
print(B - A)  #差集（先后有影响）
print(B ^ A)  # 求出 只属于a 或 b的

a = [1,2,3,4,5,6]
b = [2,4,6,8,10]

print(list(set(a) - set(b)))   #a和b都是数组 set(a)将a集化 转换成一个集 

list1 = [1,2,3,5,6,8,0,3,7,8]   #有重复元素
print(list(set(list1)))   #这样就集化 再list化过滤掉重复的 


# 文件的读写 
·open  ·write ·close

TEXT = '''My name is changjiang
I like computergraphic especially vfx
I like learning English
That is my life'''

f = open('Introduction.txt'.'w')
f.write(TEXT)
f.close()   #这样会打开一个txt 然后写入TEXT的内容 并保存关闭

f=open('Introduction.txt')
while True:
    r=f.readline()
    if len(r)=0:
        break
    print (r)    #len那行意思是如果新的行 that is my life 之后没了内容，就break 结束

##  异常处理 
·try  ·except（as） ·finally

# try案例
def tryThis():
    return(1/0)
try:
    print(tryThis())
except:
    print('your number is not for the function!')
print('ok,your calculation is done ! ')
print('the result is ...')


# except as案例
def tryThis():
    return(1/0)
l = [0,1,2,3]
try:
    print(tryThis())
    pass
except ZeroDivisionError as e:
    print('ERROR:',str(e))
except Exception as e:
    print('OTHER ERROR:',str(e))
finally:                                    # finally   不管之前结果 总会执行一件事
    print('you have do a number')   

print('ok,your calculation is done ! ')
print('the result is ...')

# raise exception 限制非法操作 抛出异常，给用户一定警告性
def compare(num):
    a = 50
    if num < 0:
        raise Exception('ERROR: your number is not suit ,it is smaller than zero ! ')
    if num > a:
        print(str(num),'is bigger than 50')
    if num < a:
        print(str(num),'is smaller than 50')
    if num == a:
        print(str(num),'is same as 50')
for i in [15,33,55,-65,77,98]:                #很多时候的错误可能是由于没注意逗号和冒号 
    try:
        print(compare(i))                   #抛出错误 告诉了-65不对，其他的还能正确的运行 
    except Exception as e:
        print(str(i),str(e))

# Python 标准库   
导入模块有这么几种形式  ·import m       ·from m import f        ·from m import *
# · import    以前经常会有这么一句话 from pymel.core import *       每个模块就像一个个打包好的库

import pymel.core as pm   #这样就用pm这个简写，指代了 pymel.core这句话 
上面是第一种写法，也可以像下面这么写
import pymel.core
pm = pymel.core

pm.ls(sl=1)
pm.parent

# from m import f
import random
random.randint(1,5)  #这样的写法还是有点麻烦 想用下面这种简单的写法 
randint(1,5)    #直接这么写会出错，那么就要下面这么引入

from random import randint
randint(1, 5)  #开始就明确表示了要引入的具体内容，randint已经是一个global的namespace


from random import *   #这个通配符表示引入了random函数下的所有
uniform(1, 8)
那么 from pymel.core import *  就好理解了 意思是导入所有的 pymel.core的模块 执行之后发现可以直接调用很多命令
ls() addAttr等等 

##关于path 
import pymel.core
pm.__file__
# Result: 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\lib\\site-packages\\pymel\\core\\__init__.pyc' # 
返回了模块的路径   
·PYTHONPATH   
·sys.path 

import sys   
sys.path      #会发现下面返回了超级多的东西      一个名字叫 Result[] 的列表 
# Result: ['C:\\Program Files\\Autodesk\\Maya2016\\bin',
 'C:\\ProgramData\\Redshift\\Plugins\\Maya\\Common\\scripts',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\bifrost\\scripts\\presets',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\bifrost\\scripts',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\fbx\\scripts',
 'C:\\Program Files\\Autodesk\\mentalrayForMaya2016\\scripts\\AETemplates',
 'C:\\Program Files\\Autodesk\\mentalrayForMaya2016\\scripts\\mentalray',
 'C:\\Program Files\\Autodesk\\mentalrayForMaya2016\\scripts\\NETemplates',
 'C:\\Program Files\\Autodesk\\mentalrayForMaya2016\\scripts\\unsupported',
 'C:\\Program Files\\Autodesk\\mentalrayForMaya2016\\scripts',
 'C:\\solidangle\\mtoadeploy\\2016\\scripts',
 'C:\\Yeti-v2.0.8_Maya2016-windows64\\scripts',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\substance\\scripts',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\cafm',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\xmaya',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\brushes',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\dialogs',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\fxmodules',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\tabs',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\util',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts\\xgenm\\ui\\widgets',
 'C:\\Program Files\\Autodesk\\Maya2016\\plug-ins\\xgen\\scripts',
 'C:\\Program Files\\Autodesk\\Maya2016\\bin\\python27.zip',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\DLLs',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\lib',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\lib\\plat-win',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\lib\\lib-tk',
 'C:\\Program Files\\Autodesk\\Maya2016\\bin',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python',
 'C:\\Program Files\\Autodesk\\Maya2016\\Python\\lib\\site-packages',
 'C:\\Program Files\\Autodesk\\Maya2016\\bin\\python27.zip\\lib-tk',
 u'D:/Documents/maya/2016/prefs/scripts',
 u'D:/Documents/maya/2016/scripts',
 u'D:/Documents/maya/scripts',
 'C:\\solidangle\\mtoadeploy\\2016\\extensions'] # 
 
import maya.OpenMaya
dir(maya.OpenMaya)
#找到了一个函数想具体的看看内容 可以像下面这样写
help(maya.OpenMaya.setRefValue)

getenv PYTHONPATH;     ## getenv PYTHONPATH;这个mel会得到所有的环境变量改动值 
// Result: C:/ProgramData/Redshift/Plugins/Maya/Common/scripts;C:/Program Files/Autodesk/Maya2016/plug-ins/bifrost/scripts/presets;C:/Program Files/Autodesk/Maya2016/plug-ins/bifrost/scripts;C:/Program Files/Autodesk/Maya2016/plug-ins/fbx/scripts;C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/AETemplates;C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/mentalray;C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/NETemplates;C:/Program Files/Autodesk/mentalrayForMaya2016/scripts/unsupported;C:/Program Files/Autodesk/mentalrayForMaya2016/scripts;C:/solidangle/mtoadeploy/2016/scripts;C:/Yeti-v2.0.8_Maya2016-windows64/scripts;C:/Program Files/Autodesk/Maya2016/plug-ins/substance/scripts;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/cafm;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/xmaya;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/brushes;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/dialogs;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/fxmodules;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/tabs;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/util;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts/xgenm/ui/widgets;C:/Program Files/Autodesk/Maya2016/plug-ins/xgen/scripts // 



# 编写模块    1.  __init__.py    2.   __all__=[sub1,sub2]      让模块在import时候做点事情 
    之前都是导入一些模块，引入别人写好的，但是一旦有了自己特定的需求，就需要编写模块。模块必须有__init__.py这个文件
一个路径下有__init__.py 把自己写的模块写进去
import sys 
sys.path.appened(r'C:User\changjiang\xxx\107')
import m.func
m.func.fn()   #fn这个函数里的内容就会被调用 

sys.path.extend(r'C:User\\changjiang\\xxx\\107')
from m import *    #直接*无法导入所有 必须在init文件里写一个东西  __all__ = ['func','func2']
func
func2  #这样在调用 1和2 这2函数时候就可以直接调用了  


 ## ------------------------------------------------------标准库  ---------------------------------------------------
 ## Python standard library 所有的python都有标准库 用了标准库里的东西 不用愁别人没有 

import this   #this 就是一个pyhton之禅    实现的方法就和自制的库一样   
this.__file__   #  'C:\\ProgramData\\Anaconda3\\lib\\this.py'   加上 .__file__后缀 就会得到文件所在的路径 

#  · os 模块包含普遍的操作系统功能      · sys 和Python interpreter相关功能    这两是用的最多最频繁的标准库 
os  
os.name    
os.getcwd()   
os.chdir()      
os.remove()     
os.system()     
os.sep      
os.listdir()

os.path.isfile()
os.path.isdir()
os.path.normpath()
os.paht.getsize()
os.path.join()
os.path.basename()
os.path.dirname()


