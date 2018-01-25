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
for i in range(100):  #加了冒号就自动带缩进 
    if i %2==0:      #如果只想得到偶数序列    如果想达到奇数的话  就写 if i %2!=0 或者 if i %2==1
        print i

#元组 （） 内容写入后，不能被更改 信息很安全 
