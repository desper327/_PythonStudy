# -*- coding: utf-8 -*-

from publish import plugin
from publish.gui import dialogWidget as Dialog
import maya.cmds as cmds


class CollectModSelfDataContrast(plugin.MayaCollector):
    '''ntegrate the extracted '''
    order = plugin.MayaCollector.order + 1.5
    label = '收集：Mod/SrfNUL提交版本层级对比'
    optional = True
    actions = ['dialog']

    def process(self, **kwargs):
        self.instance = kwargs['instance']
        self.category = kwargs['category']
        self.taskDir = kwargs['taskDir']
        self.attr = None
        # srfNUL
        if not cmds.objExists('srfNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')

        self.attr = 'srfNUL'
        self.ddict = self.contrast(self.taskDir, 'mod', 'submit', 'srfNUL', progressBar=self.instance)
        if self.ddict['submit'] == None:
            raise ValueError('整体个数不一样\n'
                             '如果必须新增物体或改动UV请跳过,没有请好好检查三思而后行\n'
                             '跳过以后就意味着 [rig, srf] 需要被动更新文件了 \n')
        elif self.ddict['submit'] == False:
            raise ValueError('物体命名或个数或UV不一样\n'
                             '如果必须新增物体或改动UV请跳过,没有请好好检查三思而后行\n'
                             '跳过以后就意味着 [rig, srf] 需要被动更新文件了 \n')

        # simNUL
        self.attr = 'simNUL'
        self.ddict = self.contrast(self.taskDir, 'mod', 'submit', 'simNUL', progressBar=self.instance)
        if self.ddict['submit'] == None:
            raise ValueError('整体个数不一样\n'
                             '如果必须新增物体或改动UV请跳过,没有请好好检查三思而后行\n'
                             '跳过以后就意味着 [rig, cfx] 需要被动更新文件了 \n')
        elif self.ddict['submit'] == False:
            raise ValueError('物体命名或UV不一样\n'
                             '如果必须新增物体或改动UV请跳过,没有请好好检查三思而后行\n'
                             '跳过以后就意味着 [rig, cfx] 需要被动更新文件了 \n')

    def dialog(self):
        if self.attr:
            ddict = self.contrast(self.taskDir, 'mod', 'submit', self.attr, progressBar=self.instance)
            win = Dialog.Ui_Form(ddict['version'], ddict['outliner'])
            # Delete existing UI
            try:
                cmds.deleteUI('NoteDialog')
            except:
                pass
            win.setObjectName('NoteDialog')
            win.setWindowTitle('Modeling')
            win.show()