import maya.cmds as cmds
import pymel.core as pm


#屏幕中间显示信息
cmds.headsUpMessage( u'已删除vaccine_gene' )
#可以带有返回信息的对话框
result = cmds.confirmDialog(title='title',message='message',button=['Yes', 'No'],defaultButton='Yes',  cancelButton='No',  dismissString='No'  )  

#获取对象
sel=cmds.ls(type=('transform','nurbs'))
cmds.ls(exactType='tansform')#确切类型，不会包含joint等派生的节点
cmds.ls(excludetype='nurbs')#排除类型
#过滤名字
cmds.ls('*mod*')#*号代表任何数量的字符
cmds.ls('?mod')#?代表一个字符


sel=cmds.ls(selection=1)[0]




cmds.listRelatives(sel,parent=1)#获取父级的节点，allparent参数是获取所有父级
cmds.listRelatives(sel,ad=1,type='joint',long=1)#获取所有子的节点，类型为joint,长名能确保不重名


#设置父子集
cmds.parent(sel,'pCube1')#把sel作为子，放到pCube1的下面
cmds.parent(sel,world=1)#把sel放到世界层级下
#打组
cmds.group(sel,n='group1')#sel可以是数组
#移动旋转缩放
cmds.move(0,0,10,sel,r=1)#r是相对移动
cmds.move(0,0,10,sel,a=1)#a是绝对移动，会被放到世界空间的那个位置上
cmds.rotate(0,50,0,sel,r=1)
cmds.scale(1,3,1,sel,r=1)
t1=cmds.xform(sel,q=1,ws=1,t=1)#获取了sel的世界空间的位移旋转缩放
cmds.xform('pCube1',t=t1)#注意：xform命令不能处理缩放





type=cmds.nodeType(sel)
print (type)
print (sel)


#要拿到[u'fffffff']的内部的字符串，要加一个[0]即可
attrs=cmds.listAttr(sel,ud=1,k=1)#获取用户自定义属性,可以K帧的
print(attrs)
for i in attrs:
    at='{}.{}'.format(sel,i)
    print(at)
    print(i)
    cmds.setAttr(at,100)
    print(cmds.getAttr(at))
    cmds.addAttr(longName='mass', defaultValue=1.0, minValue=0.001, maxValue=10000)#添加属性
    
    


sel1=cmds.ls(selection=1)[0]
sel2=cmds.ls(selection=1)[1]
cmds.connectAttr('{}.tx'.format(sel),'{}.ty'.format(sel2),force=1)#连接2个属性，2个属性都是要以字符串传入
cmds.disconnectAttr('{}.tx'.format(sel),'{}.ty'.format(sel2),force=1)#断开连接


cameraTrNode=cmds.listRelatives(sel,p=1,f=1)[0]
print(cameraTrNode)

cons=cmds.listConnections('{}'.format(sel),source=1,destination=0,plugs=1)#获取上游的连接的接口
print(cons)
cons=cmds.listConnections('{}'.format(sel),source=1,destination=0,type='lambert')#获取兰伯特类型的上游节点

con1=cmds.connectionInfo('{}.tx'.format(sel),sourceFromDestination=1)#   获取某个接口的上游连接的接口
print(con1)
con2=cmds.connectionInfo('{}.tx'.format(sel),destinationFromSource=1)#   获取某个接口的下游连接的接口
print(con2)
con3=cmds.connectionInfo('{}.tx'.format(sel),isSource=1)#判断接口是不是输出的源，返回真假
con4=cmds.connectionInfo('{}.tx'.format(sel),isDestination=1)#判断接口是不是被输入的，返回真假

con5=cmds.pointConstraint(sel1,sel2,mo=1,name='hahaha_con')#添加点约束，只有位移被约束，mo是保留偏移
con6=cmds.pointConstraint(sel1,q=1,name=1)#返回这个对象的约束节点，只针对被约束对象
con7=cmds.pointConstraint(sel1,q=1,targetList=1)#返回这个对象的约束父级所有对象，只针对被约束对象
con8=cmds.orientConstraint(sel1,sel2,mo=1,name='hahaha_con')#添加旋转约束，类似点约束的参数


cmds.setKeyframe('pCylinder1',at='ty',time=10,v=10)#参数分别是对象、属性名、时间、值，如果没有time就在当前帧设置关键帧

tc=cmds.keyframe('pCylinder1',at='ry',q=1,timeChange=1)# 查询关键帧所有时间，返回列表
cmds.keyframe('pCylinder1',q=1,valueChange=1)#查询关键帧所有值，返回列表
cmds.keyframe(sel1,e=1,at='tx',timeChange=8,time=(min(tc),max(tc)),relative=1)#移动一定范围内的关键帧,相对的


cmds.file(new=1,force=1)#强制新建一个场景，不会保存当前的场景

#保存文件需要2步
cmds.file(rename='D:/ball.ma')
cmds.file(save=1,type='mayaAscii')
#打开文件
cmds.file('D:/ball.ma',open=1,force=1)
#查询文件名字
cmds.file(q=1,sceneName=1,shortName=1)#shortName是短名，就是只是文件的名，不含路径
#导出选择为ma文件
cmds.file('D:/ball2.ma',exportSelected=1,type='mayaAscii')
#导入ma文件
cmds.file('D:/ball2.ma',i=1,type='mayaAscii',namespace='ns1')
#引用进来一个文件
cmds.file('D:/ball2.ma',r=1,namespace='ns1')
#查询引用文件
cmds.file(q=1,reference=1)
#查询已选物体的引用文件名
cmds.referenceQuery(sel1,file=1)
#查询是否是引用的，返回真假
cmds.referenceQuery(sel1, isNodeReferenced=True)



#窗口
w1_name='window1'
if cmds.window(w1_name,exists=True):#如果存在就删除
    cmds.deleteUI(w1_name)
if cmds.windowPref(w1_name,exists=True):#删除窗口的用户偏好设置
    cmds.windowPref(w1_name,remove=True)
w1=cmds.window(w1_name,title='my window',widthHeight=(300,300))
#添加按钮和layout
cmds.columnLayout(adjustableColumn=True)
cmds.button(label='click me',command="print('clicked')")#注意这里的命令是要加’‘并且区分内部的“”
cmds.button(label='close',command='cmds.deleteUI(w1_name)')

cmds.showWindow(w1)



#视图操作

#执行mel文件  maya.mel 和 pymel有，cmds没有这个函数
import maya.mel as mm
path="C:/Users/89468/Desktop/barnev_Shift_animation_code_CN.mel"
pm.mel.eval('source "{}";'.format(path))
mm.eval('source "{}";'.format(path))
#执行mel语句
mm.eval("polySphere -r 10 -sx 32 -sy 32 -sz 32 -n 'pSphere1';")
pm.mel.eval("polySphere -r 10 -sx 32 -sy 32 -sz 32 -n 'pSphere1';")

#pymel
a=pm.ls(selection=1,type='transform')[0]
print(a)

#获取和设置属性，属性.get
z=a.getTranslation().z
print(z)
x=a.translateX.get()
a.translateX.set(10)
a.translatey.isKeyable()

#获取连接
a.connections()
a.inputs()
a.outputs()
a.inputs(plugs=1)#获取的是输入接口信息

#通过名字获取一个对象


#coding:utf-8
import maya.cmds as cmds
sel=cmds.ls(sl=1)
vtx=cmds.polyEvaluate(sel,vertex=True)
a=cmds.listHistory(sel)
sel=a[0]
#cmds.skinCluster('joint1', sel)
b=cmds.pointPosition('{0}.vtx[0]'.format(sel))
pos=[]
for i in range(vtx):
    pos.append(cmds.pointPosition('{0}.vtx[{1}]'.format(sel,i)))
print(pos)
