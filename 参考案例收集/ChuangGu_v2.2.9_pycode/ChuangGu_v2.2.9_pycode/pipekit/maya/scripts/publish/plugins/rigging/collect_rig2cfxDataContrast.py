# -*- coding: utf-8 -*-

from publish import plugin
from publish.gui import dialogWidget as Dialog
import maya.cmds as cmds
import os


class CollectRig2CfxDataContrast(plugin.MayaCollector):
    '''ntegrate the extracted '''
    order = plugin.MayaCollector.order + 2.0
    label = '收集：Rig与Cfx/SimNUL通过版本层级对比'
    actions = ['dialog']
    optional = True

    def process(self, **kwargs):
        self.instance = kwargs['instance']
        self.category = kwargs['category']
        self.taskDir = kwargs['taskDir']
        self.task = kwargs['task']
        self.abbr = kwargs['department']
        self.attr = None

        if self.category == 'chr' or self.category == 'prp':
            modjson = self.taskDir + '/mod/publish/' + self.task + '_mod.json'
            if not os.path.exists(modjson):
                self.optional = False
                raise RuntimeError('请完成 [收集：Rig与Mod历史版本层级对比] 的提示操作')
            else:
                self.optional = True

            # 获取*_mod.json文件内 'stage': [2]赋值,stage != None,强制下载 cfx.josn
            modStage = self.historyHierarchy(self.taskDir, 'mod', 'publish', 'stage')
            if modStage[2] in ['hair', 'cloth', 'cfx2']:
                cfxjson = self.taskDir + '/cfx/publish/' + self.task + '_cfx.json'
                if not os.path.exists(cfxjson):
                    self.optional = True
                    raise RuntimeError('缺少[*_cfx.json]文件,允许跳过但此任务不能输出动画缓存\n'
                                       '请到CGTW客户端rig任务下 -> [工作] -> [角色特效通过文件]框\n'
                                       '下载json文件后再次尝试文件验证')
                else:
                    self.optional = False

                self.attr = 'simNUL'
                self.ddict = self.contrast(self.taskDir, 'cfx', 'publish', self.attr, self.abbr, progressBar=self.instance)
                if self.ddict['submit'] == True:
                    cfxStage = self.historyHierarchy(self.taskDir, 'cfx', 'publish', 'stage')
                    cmds.setAttr('Group.stage', cfxStage[2], type='string')
                elif self.ddict['submit'] == None:
                    raise ValueError('整体个数不一样\n'
                                     '请参照cfx文件层级手动调整rig文件层级或替换cfx层级\n')
                elif self.ddict['submit'] == False:
                    raise ValueError('物体命名或UV不一样\n'
                                     '请参照cfx文件层级手动调整rig文件层级或替换cfx层级\n')
            else:
                cmds.setAttr('Group.stage', 'done', type='string')

    def dialog(self):
        if self.attr:
            ddict = self.contrast(self.taskDir, 'cfx', 'publish', self.attr, self.abbr, progressBar=self.instance)
            win = Dialog.Ui_Form(ddict['version'], ddict['outliner'])
            # Delete existing UI
            try:
                cmds.deleteUI('NoteDialog')
            except:
                pass
            win.setObjectName('NoteDialog')
            win.setWindowTitle('Rigging')
            win.show()