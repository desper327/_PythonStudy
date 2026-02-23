# -*- coding: utf-8 -*-

import os
import json
import time
import logging
import maya.cmds as cmds
import maya.mel as mel


class Plugin(object):
    '''
    属性:
        name: 对象名称
        label: gui上使用的'Nice-name'
        order: 处理该插件的顺序
        optional: 用户是否可以跳过插件
        default: 插件默认运行
        ignoreType: 可以选择限制“输出”插件类型(组件、资产或发布)
        actions: 与此插件相关联的操作
    '''
    name = None
    label = None
    order = -1
    optional = False
    default = True
    ignoreType = []
    actions = []

    def __init__(self):
        self.log = logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))
        self.name = type(self).__name__


class Collector(Plugin):
    ''' Parse a given working scene for available Instances '''
    order = 0

    def createInstance(self, **kwargs):
        return kwargs


class Checklist(Plugin):
    ''' Checklist plugin to run before validators '''
    order = 1


class Validator(Plugin):
    ''' Validate/check/test individual instance for correctness '''
    order = 2


class Extractor(Plugin):
    ''' Physically separate Instance from Application into corresponding resources '''
    order = 3


class Integrator(Plugin):
    ''' Integrates publishes into a publish pipeline '''
    order = 4


class MayaCollector(Collector):
    ''' Maya specific collection base class '''
    def historyHierarchy(self, taskDir, abbr, stage, key):
        '''
        :param taskDir:
        :param abbr: ['mod', 'rig', 'srf', 'cfx']
        :param stage: ['submit', 'publish']
        :param key: ['srfNUL', 'simNUL', 'stage']
        :return:
        '''
        task = taskDir.split('/')[-1]
        hierarchy = []
        if stage == 'submit':
            submitDir = taskDir + '/' + abbr + '/submit'
            dirs = cmds.getFileList(folder=submitDir, filespec='v*.')
            if dirs:
                dirs.sort(reverse=False)
                verDir = submitDir + '/' + dirs[-1]
                jsonfile = verDir + '/' + task + '_' + abbr + '.json'
            else:
                jsonfile = submitDir + '/v001/' + task + '_' + abbr + '.json'
        elif stage == 'publish':
            publishDir = taskDir + '/' + abbr + '/publish'
            jsonfile = publishDir + '/' + task + '_' + abbr + '.json'
        # 获取上版本层级数据
        if os.path.exists(jsonfile):
            with open(jsonfile, 'r') as fo:
                text = fo.read()
                fdict = json.loads(text)
            ver = fdict.keys()
            ver.sort(reverse=True)
            if key in fdict[ver[0]]:
                hierarchy = fdict[ver[0]][key]
        return hierarchy

    def outlinerHierarchy(self, abbr, null):
        hierarchy = []
        if cmds.objExists(null):
            cmds.displaySmoothness(null, divisionsU=0, divisionsV=0, pointsWire=4, pointsShaded=1, polygonObject=1)

            objs = cmds.listRelatives(null, ad=1, f=1, type=['transform'])
            if objs:
                for iobj in objs:
                    hierarchy.append(iobj.replace('|Group', '').replace('|Geometry', '').replace('|cfxNUL', ''))

            meshes = cmds.filterExpand(null, ex=1, sm=12)
            if meshes:
                if abbr == 'cfx' and null == 'simNUL':
                    cmds.select('simNUL')
                    mel.eval('displayNClothMesh "input"')
                cmds.MoveTool()
                for mesh in meshes:
                    if cmds.nodeType(mesh) == 'mesh':
                        shape = mesh
                    else:
                        shape = cmds.listRelatives(mesh, shapes=1, path=1, ni=1)[0]
                    count = cmds.polyEvaluate(shape, uv=1, e=1, v=1, f=1, t=1)
                    cmds.select(shape + '.f[0:' + str(count['face']) + ']', r=1)
                    uvPivot = cmds.getAttr(shape + '.uvPivot')
                    uPivot = round(uvPivot[0][0], 6)
                    vPivot = round(uvPivot[0][1], 6)
                    hierarchy.append(shape.split('|')[-1] + "{'count':(" +
                                     str(count['vertex']) + ',' +
                                     str(count['edge']) + ',' +
                                     str(count['face']) + ',' +
                                     str(count['triangle']) + '),' +
                                     "'uvp':(" + str(count['uvcoord']) + ',' + str(uPivot) + ',' + str(vPivot) + ')}')
                if abbr == 'cfx' and null == 'simNUL':
                    cmds.select('simNUL')
                    mel.eval('displayNClothMesh "current"')
        cmds.select(clear=1)
        return hierarchy

    def contrast(self, taskDir, module, stage, key, abbr=None, progressBar=None):
        ndict = {
            'version': [],
            'outliner': [],
            'submit': True
        }
        if progressBar:
            progressBar.label.setVisible(True)
            progressBar.label.setText('[收集：历史版本/层级对比]')
            progressBar.version.setVisible(False)
            progressBar.progressBar.setVisible(True)
            progressBar.progressBar.setStyleSheet('''
                QProgressBar::chunk { 
                    background-color: rgb(100,100,100); 
                }
            ''')
            progressBar.progressBar.setValue(1)
            old = self.historyHierarchy(taskDir, module, stage, key)
            progressBar.progressBar.setValue(10)
            new = self.outlinerHierarchy(abbr, key)
            progressBar.progressBar.setValue(25)

            ndict['version'] = old
            ndict['outliner'] = new
            if old:
                if len(new) == len(old):
                    n = 0
                    m = 75.0 / len(new)
                    for i in range(len(new)):
                        time.sleep(0.001)
                        n += 1
                        v = 75.0 + (n * m)
                        progressBar.progressBar.setValue(v)
                        if new[i] != old[i]:
                            ndict['submit'] = False
                            break
                else:
                    ndict['submit'] = None
            time.sleep(0.5)
            progressBar.label.setVisible(True)
            progressBar.version.setVisible(True)
            progressBar.progressBar.setVisible(False)
        else:
            old = self.historyHierarchy(taskDir, module, stage, key)
            new = self.outlinerHierarchy(abbr, key)

            ndict['version'] = old
            ndict['outliner'] = new
            if old:
                if len(new) == len(old):
                    for i in range(len(new)):
                        if new[i] != old[i]:
                            ndict['submit'] = False
                            break
                else:
                    ndict['submit'] = None
        return ndict

    def workFilePath(self):
        exn = cmds.file(q=1, exn=1)
        if '/work/' in exn:
            return True
        else:
            return False


class MayaExtractor(Extractor):
    ''' Maya specific extraction base class '''
    pass