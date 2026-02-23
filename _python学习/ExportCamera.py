import maya.cmds as cmds
startFrame = cmds.playbackOptions(ast=True, q=True)
endFrame = cmds.playbackOptions(aet=True, q=True)
selected_cam = cmds.ls(sl=True)[0]

def  bakeCamera(cameraTrNode,sf, ef):
    if cmds.nodeType(cameraTrNode)=='camera':
        cameraTrNode=cmds.listRelatives(cameraTrNode,p=1,f=1)[0]
    
    NewCameraTr=cmds.duplicate(cameraTrNode,name=cameraTrNode+'_Ex',rc=1)[0]
    attrList = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz',
                'sx', 'sy', 'sz', 'translate', 'scale', 'rotate']
    for attr in attrList:
        cmds.setAttr(NewCameraTr+'.'+attr, lock=0)
    cmds.select(NewCameraTr)
    try:
        cmds.parent(w=1)
    except:
        pass
    cameraShNode = cmds.listRelatives(cameraTrNode, s=1,f=1)[0]
    focLen = cmds.getAttr(cameraShNode+'.fl')
    NewCameraShape = cmds.listRelatives(NewCameraTr, s=1,f=1)[0]
    NewCameraShape=cmds.rename(NewCameraShape, NewCameraTr+'shape')
    NewCameraTr = cmds.listRelatives(NewCameraShape, p=1,f=1)[0]
    NewCameraShape = cmds.listRelatives(NewCameraTr, s=1,f=1)[0]
    cmds.setAttr("{}.farClipPlane".format(NewCameraShape),10000000)
    for i in range(int(sf), int(ef+1)):
        cmds.currentTime(i)
        cameraRot = cmds.xform(cameraTrNode, q=1, ro=1, ws=1)
        cameraTr = cmds.xform(cameraTrNode, q=1, t=1, ws=1)
        cmds.xform(NewCameraTr, ro=cameraRot)
        cmds.xform(NewCameraTr, t=cameraTr)
        focLen = cmds.getAttr(cameraShNode+'.fl')
        cmds.select(NewCameraTr)
        cmds.setKeyframe(at='tx', v=cameraTr[0])
        cmds.setKeyframe(at='ty', v=cameraTr[1])
        cmds.setKeyframe(at='tz', v=cameraTr[2])
        cmds.setKeyframe(at='rx', v=cameraRot[0])
        cmds.setKeyframe(at='ry', v=cameraRot[1])
        cmds.setKeyframe(at='rz', v=cameraRot[2])
        cmds.setKeyframe(NewCameraShape, at='fl', v=focLen)
    return NewCameraTr
    
bakeCamera(selected_cam,startFrame,endFrame);