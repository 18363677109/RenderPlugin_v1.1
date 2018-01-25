 #******************************************aboutcg python教程*******************************************************
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

from pymel.core import *
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