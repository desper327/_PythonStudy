# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoHistory(plugin.Validator):
    """Validate transforms have no history
    """
    label = '验证：没有构造历史或禁止的节点'
    actions = ['select']

    def getInvalid(self):
        ignoreTypes = ['shadingEngine', 'objectSet']
        dag = cmds.ls(dag=True)
        xform = cmds.ls(type='transform')
        history = cmds.listHistory(dag)
        history = list(set(history))
        shapes = cmds.ls(history, shapes=True)
        shapes.extend(xform)
        history = [x for x in history if x not in shapes]
        history = [x for x in history if cmds.nodeType(x) not in ignoreTypes]
        
        # Ensure only valid node types
        allowed = ['mesh', 'transform', 'nurbsCurve', 'camera', 'shadingEngine']
        disallowed = ['objectSet']
        
        nodes = cmds.ls(long=True, dagObjects=True)
        for each in disallowed:
            for x in cmds.ls(type=each):
                if x[:7] in ['default', 'initial']:
                    continue
                nodes.append(x)
                
        valid = cmds.ls(long=True, type=allowed)
        invalid = set(nodes) - set(valid)

        if invalid:
            # This is used to make the list of invalid objects more readable in the UI for artists.
            transformList = []
            for inval in invalid:
                inval = cmds.ls(inval)[0]
                if 'nurbsSurface' == cmds.objectType(inval):
                    inval = cmds.listRelatives(inval, parent=True)
                transformList.append(inval)
            invalid = transformList        
            
        history.extend(invalid)
        history = list(set(history))
        return history

    def process(self, **kwargs):
        invalid = self.getInvalid()
        if invalid:
            raise TypeError('历史记录和禁止节点: ' + str('\n'.join(invalid)))

    def repair(self, args):
        cmds.delete(all=True, constructionHistory=True)
        additionalHistory = self.getInvalid()
        if additionalHistory:
            cmds.lockNode(additionalHistory, lock=0)
            cmds.delete(additionalHistory)

    def select(self):
        cmds.select(self.getInvalid(), r=1)