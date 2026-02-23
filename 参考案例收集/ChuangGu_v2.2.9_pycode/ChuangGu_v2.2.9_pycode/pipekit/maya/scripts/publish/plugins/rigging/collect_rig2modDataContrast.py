# -*- coding: utf-8 -*-

from publish import plugin
from publish.gui import dialogWidget as Dialog
import maya.cmds as cmds
import os


class CollectRig2ModDataContrast(plugin.MayaCollector):
    '''ntegrate the extracted '''
    order = plugin.MayaCollector.order + 1.5
    label = '收集：Rig与Mod/SrfNUL通过版本层级对比'
    actions = ['dialog']

    def process(self, **kwargs):
        self.instance = kwargs['instance']
        self.category = kwargs['category']
        self.taskDir = kwargs['taskDir']
        self.task = kwargs['task']
        self.attr = None
        modjson = self.taskDir + '/mod/publish/' + self.task + '_mod.json'
        if not os.path.exists(modjson):
            raise RuntimeError('缺少[*_mod.json]文件\n'
                               '请到CGTW客户端rig任务下 -> [工作] -> [模型通过文件]框\n'
                               '下载json文件后再次尝试文件验证')

        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        if self.category in ['chr', 'prp', 'veh', 'set']:
            if not cmds.objExists('Group.stage'):
                cmds.addAttr('Group', ln='stage', dt='string')
            cmds.setAttr('Group.stage', 'done', type='string')

        self.attr = 'srfNUL'
        self.ddict = self.contrast(self.taskDir, 'mod', 'publish', self.attr, progressBar=self.instance)
        if self.ddict['submit'] == None:
            raise ValueError('整体个数不一样\n'
                             '请参照mod文件层级手动调整rig文件层级或替换mod层级\n')
        elif self.ddict['submit'] == False:
            raise ValueError('物体命名或UV不一样\n'
                             '请参照mod文件层级手动调整rig文件层级或替换mod层级\n')

    def dialog(self):
        if self.attr:
            ddict = self.contrast(self.taskDir, 'mod', 'publish', self.attr, progressBar=self.instance)
            win = Dialog.Ui_Form(ddict['version'], ddict['outliner'])
            # Delete existing UI
            try:
                cmds.deleteUI('NoteDialog')
            except:
                pass
            win.setObjectName('NoteDialog')
            win.setWindowTitle('Rigging')
            win.show()