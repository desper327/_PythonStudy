# Source Generated with Decompyle++
# File: ld_createSoftCluster.pyc (Python 2.6)

import maya.cmds as mc
import maya.mel as mm
import maya.OpenMaya as om

def softSelection():
    selection = om.MSelectionList()
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    softSelection.getSelection(selection)
    dagPath = om.MDagPath()
    component = om.MObject()
    iter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
    elements = []
    weights = []
    while not iter.isDone():
        iter.getDagPath(dagPath, component)
        dagPath.pop()
        node = dagPath.fullPathName()
        fnComp = om.MFnSingleIndexedComponent(component)
        
        getWeight = lambda i: if fnComp.hasWeights():fnComp.weight(i).influence() 1
        for i in range(fnComp.elementCount()):
            elements.append('%s.vtx[%i]' % (node, fnComp.element(i)))
            weights.append(getWeight(i))
        
        iter.next()
        continue
        (None,)
    return (elements, weights)


def ld_repositionCluster(clusterHandle, position):
    mc.xform(clusterHandle, a = True, ws = True, piv = (position[0], position[1], position[2]))
    clusterShape = mc.listRelatives(clusterHandle, c = True, s = True)
    mc.setAttr(clusterShape[0] + '.origin', position[0], position[1], position[2])


def ld_createSoftCluster():
    (elements, weights) = softSelection()
    mc.setToolTo('Move')
    currentMoveMode = mc.manipMoveContext('Move', q = True, m = True)
    mc.manipMoveContext('Move', e = True, m = 0)
    position = mc.manipMoveContext('Move', q = True, p = True)
    mc.manipMoveContext('Move', e = True, m = currentMoveMode)
    object = mc.listRelatives(mc.listRelatives(p = True), p = True)
    newClus = mc.cluster(elements, n = object[0] + '_softCluster')
    for i in range(len(elements)):
        mc.percent(newClus[0], elements[i], v = weights[i])
    
    ld_repositionCluster(newClus[1], position)

