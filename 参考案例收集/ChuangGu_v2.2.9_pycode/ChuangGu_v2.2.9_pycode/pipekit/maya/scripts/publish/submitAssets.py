# -*- coding: utf-8 -*-

from PySide2 import QtCore
import re
import os
import json
import maya.cmds as cmds
import maya.mel as mel
import envpath


class SubmitAssets(QtCore.QObject):
    SigScriptEditor = QtCore.Signal(str, str)

    def __init__(self, **kwargs):
        super(SubmitAssets, self).__init__()

        # 传参
        self.category = kwargs['category']
        self.abbr = kwargs['abbr']
        self.format = kwargs['format']
        self.dirpath = kwargs['dirpath'] + '/submit'
        self.task = kwargs['task']
        self.comment = kwargs['comment']
        self.render = kwargs['render']

        # 导出文件所选物体
        self.object = []
        if self.abbr == 'asm':
            self.object = cmds.ls(['*_set_AR', '*_env_DS'])
        elif self.abbr == 'mod':
            self.object = ['Geometry']
        elif self.abbr == 'rig':
            self.object = ['Group']
        elif self.abbr == 'cfx':
            self.object = ['cfxNUL']
        elif self.abbr == 'srf':
            if self.category in ['set']:
                self.object = ['Group']
            else:
                self.object = ['Geometry']

        # 获取版本号及版本路径
        dirs = cmds.getFileList(folder=self.dirpath, filespec='v*.')
        if not dirs:
            self.ver = 'v001'
            self.verDir = self.dirpath + '/' + self.ver
            self.oldVerDir = None
        else:
            dirs.sort(reverse=False)
            count = int(re.sub('\D', '', dirs[-1])) + 1
            self.ver = 'v' + str(count).zfill(3)
            self.verDir = self.dirpath + '/' + self.ver
            self.oldVerDir = self.dirpath + '/' + dirs[-1]

    def versionData(self):
        '''
        jfile: */v001/task_mod.json
        {
            "v001": {
                "stage": ["done", "face", "cfx2", "tangchun", "2020/04/04 10:00:00"],
                "hierarchy": "default",
                "comment": "",
                "application": "Maya 2020"
            }
        }
        '''
        vdict = {}
        stage = []
        if self.category in ['env', 'set']:
            stage.append('done')
            stage.append(None)
            stage.append(None)
        else:
            '''
            stage: 0
            '''
            if self.abbr == 'rig':
                # 阶段判断
                staged = cmds.getAttr('Group.stage')
                if staged in ['done', 'hair', 'cloth', 'cfx2']:
                    stage.append('done')
                else:
                    stage.append(staged)
                # 表情判断
                if cmds.objExists('FaceGroup'):
                    if cmds.listRelatives('FaceGroup', children=1):
                        stage.append('face')
                    else:
                        stage.append(None)
                else:
                    stage.append(None)
            else:
                stage.append('done')
                stage.append(None)
            # 毛发,布料判断
            fx2 = []
            if cmds.objExists('hairGrmNUL') and cmds.filterExpand('hairGrmNUL', ex=1, sm=12):
                fx2.append('hair')
            if cmds.objExists('clothWpNUL') and cmds.filterExpand('clothWpNUL', ex=1, sm=12):
                fx2.append('cloth')
            if fx2:
                if len(fx2) == 2:
                    stage.append('cfx2')
                else:
                    stage.append(fx2[0])
            else:
                stage.append(None)

        stage.append(os.environ['USERNAME'].lower())
        stage.append(cmds.date())

        vdict[self.ver] = {
            'stage': stage,
            'comment': self.comment,
            'application': 'Maya ' + str(cmds.about(api=1))[:4] + '.' + str(cmds.about(api=1))[5:6],
            'ctoolkit': envpath.CTOOLKIT
        }
        return vdict

    def hierarchyData(self):
        '''
        {
            "simNUL": [
                "|simNUL|hairGrmNUL",
                "|simNUL|clothWpNUL|CH_QYZR_RC_cloth_01_SDM_solver",
                "|simNUL|clothWpNUL",
                "CH_QYZR_RC_cloth_01_SDM_solverShape['count':(4783,9372,4589,9178)] ['uvp':(5423,0.167916,0.483337)]",
            ],
            "srfNUL": [
                "|srfNUL|defaultNUL|CH_QYZR_RC_head_grp|QingYangZhenRen_eye_grp|QingYangZhenRen_eye_R_SDM",
                "|srfNUL|defaultNUL",
                "|srfNUL|clothNUL|CH_QYZR_RC_cloth_01_SDM",
                "|srfNUL|clothNUL",
                "|srfNUL|noRenderNUL|CH_QYZR_RC_jiemao_PLY",
                "|srfNUL|noRenderNUL",
                "QingYangZhenRen_eye_R_SDMShape['count':(541,1080,540,1060)] ['uvp':(561,0.5,0.483146)]",
            ]
        }
        '''
        nulls = []
        # if self.category == 'chr' or self.category == 'prp':
        if self.abbr == 'srf':
            nulls.append('srfNUL')
        elif self.abbr == 'cfx':
            nulls.append('srfNUL')
            nulls.append('simNUL')
        else:
            nulls.append('srfNUL')
            nulls.append('simNUL')

        hdict = {}
        for null in nulls:
            if cmds.objExists(null):
                cmds.displaySmoothness(null, divisionsU=0, divisionsV=0, pointsWire=4, pointsShaded=1, polygonObject=1)
                text = []

                objs = cmds.listRelatives(null, ad=1, f=1, type=['transform'])
                if objs:
                    for iobj in objs:
                        text.append(iobj.replace('|Group', '').replace('|Geometry', '').replace('|cfxNUL', ''))
                meshes = cmds.filterExpand(null, ex=1, sm=12)
                if meshes:
                    if self.abbr == 'cfx' and null == 'simNUL':
                        cmds.select('simNUL')
                        mel.eval('displayNClothMesh "input"')
                    cmds.MoveTool()
                    for mesh in meshes:
                        shape = cmds.listRelatives(mesh, shapes=1, path=1, ni=1)
                        count = cmds.polyEvaluate(shape[0], uv=1, e=1, v=1, f=1, t=1)
                        cmds.select(shape[0]+'.f[0:' + str(count['face']) + ']', r=1)
                        uvPivot = cmds.getAttr(shape[0] + '.uvPivot')
                        uPivot = round(uvPivot[0][0], 6)
                        vPivot = round(uvPivot[0][1], 6)
                        text.append(shape[0].split('|')[-1] + "{'count':(" +
                                    str(count['vertex']) + ',' +
                                    str(count['edge']) + ',' +
                                    str(count['face']) + ',' +
                                    str(count['triangle']) + '),' +
                                    "'uvp':(" + str(count['uvcoord']) + ',' + str(uPivot) + ',' + str(vPivot) + ')}')
                    if self.abbr == 'cfx' and null == 'simNUL':
                        cmds.select('simNUL')
                        mel.eval('displayNClothMesh "current"')
                hdict[null] = text
        cmds.select(clear=1)
        return hdict

    def materials(self, mfile):
        '''
        {
            "lookdev":{
                "render": ["Arnold", "6.2.0.1"],
                "materials":{
                    "ar": [],
                    "rs": []
                }
            }
        }
        '''
        mdict = {
            "render": self.render,
            "materials": {}
        }
        materials = cmds.ls(materials=1)
        if materials:
            for material in materials:
                cmds.hyperShade(objects=material)
                objs = cmds.ls(sl=1)
                if objs:
                    mdict['materials'][material] = objs
                    cmds.select(clear=1)
            # export materials file
            cmds.select(materials, r=1)
            cmds.file(mfile, f=1, typ=self.format[1], es=1, ch=1, con=1, chn=1, eas=0, sh=1)
        return mdict

    def writeData(self, jsonname):
        fdict = {}
        # 截取历史最新版本
        if self.oldVerDir:
            oldfile = self.oldVerDir + '/' + jsonname
            if os.path.exists(oldfile):
                with open(oldfile, 'r') as fo:
                    text = fo.read()
                    tdict = json.loads(text)
                ver = tdict.keys()
                ver.sort(reverse=True)
                fdict[ver[0]] = tdict[ver[0]]
        # 添加当前最新版本
        vdict = self.versionData()
        hdict = self.hierarchyData()
        for k, v in hdict.items():
            vdict.values()[0][k] = v
        # srf部门: 导出shd文件同时增加['lookdev']字段
        if self.abbr == 'srf':
            mfile = self.verDir + '/' + self.task + '_srf_shd.mb'
            mdict = self.materials(mfile)
            vdict.values()[0]['lookdev'] = mdict
        fdict[vdict.keys()[0]] = vdict.values()[0]
        # 写入新本json文件
        newfile = self.verDir + '/' + jsonname
        with open(newfile, 'w') as fo:
            fo.write(json.dumps(fdict, indent=4))

    def writeAsmData(self, jsonname):
        fdict = {}
        # 截取历史最新版本
        jfile =self.verDir.rsplit('/', 3)[0] + '/asm/publish/' + jsonname
        if os.path.exists(jfile):
            with open(jfile, 'r') as fo:
                text = fo.read()
                tdict = json.loads(text)
            vers = tdict.keys()
            vers.sort(reverse=True)
            fdict[vers[0]] = tdict[vers[0]]
            ver = 'v' + str(int(re.sub('\D', '', vers[0]))+1).zfill(3)
        else:
            ver = 'v001'

        # 添加最新版本
        fdict[ver] = {
            'stage': 'done',
            'comment': self.comment,
            'application': 'Maya ' + str(cmds.about(api=1))[:4] + '.' + str(cmds.about(api=1))[5:6],
            'ctoolkit': envpath.CTOOLKIT
        }

        # 添加assembly字段
        tdict = {
            'assembly': {
                'chr': {},
                'prp': {},
                'env': {},
                'set': {}
            }
        }
        # ar
        ars = cmds.ls(type=['assemblyReference'])
        for i in ars:
            filename = cmds.getAttr(i + '.definition')
            array = filename.split('/')
            category = array[3]
            task = array[4]
            if task not in tdict['assembly'][category]:
                tdict['assembly'][category][task] = {
                    "nsid": [],
                    "file": filename
                }

            nsid = re.sub('\D', '', str(i.split('_')[-1]))
            if not nsid:
                nsid = 0
            else:
                nsid = int(nsid)
            tdict['assembly'][category][task]['nsid'].append(nsid)
        # ds
        dss = cmds.ls('*_env_DS')
        for i in dss:
            child = cmds.listRelatives(i, children=1)
            if child:
                array = i.split('_')
                category = array[1]
                task = array[0]
                nodes = cmds.listHistory(child[0])
                if self.render[0] == 'Redshift':
                    filename = cmds.getAttr(nodes[-1] + '.fileName')
                elif self.render[0] == 'Arnold':
                    filename = cmds.getAttr(nodes[-1] + '.dso')
                tdict['assembly'][category][task] = {
                    "nsid": [len(child)],
                    "file": filename
                }

        fdict[ver]['assembly'] = tdict.values()[0]
        # 写入新本json文件
        with open(jfile, 'w') as fo:
            fo.write(json.dumps(fdict, indent=4))

    def definition(self):
        # 文件路径
        cmds.sysFile(self.verDir, makeDir=1)
        modPubDir = self.verDir.rsplit('/', 3)[0] + '/mod/publish'
        rigPubDir = self.verDir.rsplit('/', 3)[0] + '/rig/publish'
        srfPubDir = self.verDir.rsplit('/', 3)[0] + '/srf/publish'
        asmPubDir = self.verDir.rsplit('/', 3)[0] + '/asm/publish'
        adFile = asmPubDir + '/' + self.task + '.mb'
        asmFile = asmPubDir + '/' + self.task + '_asm.mb'
        setFile = asmPubDir + '/' + self.task + '_set.mb'

        if self.abbr == 'mod':
            # 加载插件及预设
            plugins = ['sceneAssembly.mll', 'gpuCache.mll']
            for plugin in plugins:
                if not cmds.pluginInfo(plugin, q=1, loaded=1):
                    cmds.loadPlugin(plugin)

            # 删除所有AD节点，在创建一个AD节点
            adsNodes=cmds.ls(type=['assemblyDefinition'])
            if adsNodes:
                cmds.delete(adsNodes)
            adNode = cmds.assembly(type='assemblyDefinition')

            # mod->[0-2]
            active0 = ['Locator', 'ModBbox', 'ModCache']
            for i in range(len(active0)):
                if i == 0:
                    cmds.assembly(adNode, e=1, createRepresentation="Locator")
                else:
                    if i == 1:
                        gpuFile = modPubDir + '/' + self.task + '_mod_box.abc'
                    elif i == 2:
                        gpuFile = modPubDir + '/' + self.task + '_mod_gpu.abc'
                    cmds.assembly(adNode, e=1, createRepresentation="Cache", input=gpuFile)
                    cmds.setAttr(adNode + '.representations[' + str(i) + '].repLabel', active0[i], type='string')

            # export box abc
            bbox = cmds.geomToBBox('srfNUL',
                                   nameSuffix='_BBox',
                                   single=1,
                                   shaderColor=[0.75, 0.65, 0.65],
                                   keepOriginal=1)
            cmds.gpuCache(bbox[0],
                          startTime=1,
                          endTime=1,
                          optimize=1,
                          optimizationThreshold=40000,
                          writeMaterials=1,
                          dataFormat='ogawa',
                          directory=self.verDir,
                          fileName=self.task + '_mod_box')
            cmds.delete(bbox)
            mel.eval('catchQuiet(`delete "BBoxLambert*" "BBoxSG*"`)')
            # export gpu
            cmds.gpuCache('srfNUL',
                          startTime=1,
                          endTime=1,
                          optimize=1,
                          optimizationThreshold=40000,
                          writeMaterials=1,
                          dataFormat='ogawa',
                          directory=self.verDir,
                          fileName=self.task + '_mod_gpu')

            # srf->[3-5]
            active1 = ['RigFiles', 'SrfProxy', 'SrfFiles']
            refFile = []
            for i in range(len(active1)):
                if i == 0:
                    refFile.append(rigPubDir + '/' + self.task + '_rig.mb')
                elif i == 1:
                    refFile.append(srfPubDir + '/' + self.task + '_srf_pxy.mb')
                elif i == 2:
                    refFile.append(srfPubDir + '/' + self.task + '_srf.mb')
                cmds.assembly(adNode, e=1, createRepresentation="Scene", input=refFile[i])
                cmds.setAttr(adNode + '.representations[' + str(3 + i) + '].repLabel', active1[i], type='string')

            # 导出definition节点
            cmds.sysFile(asmPubDir, makeDir=1)
            cmds.select(adNode, r=1)
            cmds.file(adFile, force=1, channels=0, constructionHistory=0, constraints=0, shader=0, typ="mayaBinary", es=1)
            cmds.delete(adNode)

            # set-> assembly reference
            if self.category == 'set':
                # 不存mod输出,如果onset二次编辑过则不输出
                if not os.path.exists(asmFile):
                    # ar合集
                    arNodes = cmds.ls(type=['assemblyReference'])
                    if arNodes:
                        cmds.delete(arNodes)
                    arNode = cmds.assembly(type='assemblyReference', name=self.task+'_set_AR')
                    cmds.setAttr(arNode + '.repNamespace', self.task+'_set_NS', type='string')
                    cmds.setAttr(arNode + '.definition', adFile, type='string')
                    arNodes = cmds.ls('*_*_AR*')
                    if arNodes:
                        cmds.select(arNodes, r=1)
                        cmds.file(asmFile, force=1, channels=0, constructionHistory=0, constraints=0, shader=0, typ="mayaBinary", es=1)
                        cmds.delete(arNode)
                    # set的ad节点
                    adNodes = cmds.ls(type=['assemblyDefinition'])
                    if adNodes:
                        cmds.delete(adNodes)
                    adNode = cmds.assembly(type='assemblyDefinition')
                    # cmds.assembly(adNode, e=1, createRepresentation="Locator")
                    cmds.assembly(adNode, e=1, createRepresentation="Scene", input=asmFile)
                    cmds.setAttr(adNode + '.representations[0].repLabel', 'AsmScene', type='string')
                    cmds.select(adNode, r=1)
                    cmds.file(setFile, force=1, channels=0, constructionHistory=0, constraints=0, shader=0, typ="mayaBinary", es=1)
                    cmds.delete(adNode)
        elif self.abbr == 'srf':
            if self.render[0] == 'Redshift':
                if not cmds.pluginInfo('redshift4maya.mll', q=1, loaded=1):
                    try:
                        cmds.loadPlugin('redshift4maya.mll')
                    except:
                        self.SigScriptEditor.emit('exoprt', '未找到Redshift 2.5.48渲染器')
                        raise RuntimeError('未找到Redshift 2.5.48渲染器')
                # export
                exRsFile = self.verDir + '/' + self.task + '_srf_pxy.rs'
                ppRsFile = srfPubDir + '/' + self.task + '_srf_pxy.rs'
                cmds.select('srfNUL', r=1)
                cmds.rsProxy(filePath=exRsFile, sl=1)
                cmds.select(clear=1)
                rsNodes = mel.eval('redshiftCreateProxy')
                cmds.setAttr(rsNodes[0] + '.fileName', ppRsFile, type='string')
                proxy = cmds.rename(rsNodes[2], self.task + '_proxy')
                rsNode = cmds.rename(rsNodes[0], self.task + '_redshiftProxy')
                cmds.setAttr(rsNode + '.objectIdMode', 1)
                cmds.setAttr(rsNode + '.visibilityMode', 1)
                cmds.setAttr(rsNode + '.displayMode', 1)
                if self.abbr == 'env':
                    cmds.setAttr(rsNode + '.displayPercent', 50)
                else:
                    cmds.setAttr(rsNode + '.displayPercent', 75)
            elif self.render[0] == 'Arnold':
                if not cmds.pluginInfo('mtoa.mll', q=1, loaded=1):
                    try:
                        cmds.loadPlugin('mtoa.mll')
                    except:
                        self.SigScriptEditor.emit('exoprt', '未找到Arnold 6.1.0.0渲染器')
                        raise RuntimeError('未找到Arnold 6.1.0.0渲染器')
                # export
                exAssFile = self.verDir + '/' + self.task + '_srf_pxy.ass'
                ppAssFile = srfPubDir + '/' + self.task + '_srf_pxy.ass'
                cmds.select('srfNUL', r=1)
                cmds.arnoldExportAss(f=exAssFile, s=1, shadowLinks=0, lightLinks=0, boundingBox=1)
                cmds.select(clear=1)
                aiShape = cmds.createNode('aiStandIn', n=self.task + '_aiStandIn')
                cmds.setAttr(aiShape + '.dso', ppAssFile, type='string')
                temp = cmds.listRelatives(aiShape, p=1)
                proxy = cmds.rename(temp[0], self.task + '_proxy')
                if self.category == 'env':
                    cmds.setAttr(aiShape + '.mode', 2)
                else:
                    cmds.setAttr(aiShape + '.mode', 6)
            pxyfile = self.verDir + '/' + self.task + '_srf_pxy.mb'
            cmds.select(proxy, r=1)
            cmds.file(pxyfile, force=1, channels=0, constructionHistory=1, constraints=0, shader=1, typ="mayaBinary", es=1)
            cmds.delete(proxy)

    def exportFile(self, esfile):
        if self.abbr == 'cfx':
            # 加载插件
            if not cmds.pluginInfo('AbcExport.mll', q=1, loaded=1):
                cmds.loadPlugin('AbcExport.mll')

            # 保存cfx文件
            meshes = cmds.filterExpand('simNUL', ex=1, sm=12)
            if meshes:
                cmds.select('clothWpNUL')
                mel.eval('displayNClothMesh "current"')
            cmds.file(rename=esfile)
            cmds.file(f=1, save=1, type=self.format[1])

            # 导出abc文件
            if meshes:
                simfile = esfile.replace('_cfx.mb', '_sim.mb')
                abcfile = simfile.replace('.mb', '.abc')
                cmds.select('simNUL')
                mel.eval('displayNClothMesh "input"')
                cmds.AbcExport(j="-frameRange 1 1 "
                                 "-stripNamespaces "
                                 "-uvWrite "
                                 "-worldSpace "
                                 "-writeVisibility "
                                 "-dataFormat ogawa "
                                 "-root simNUL "
                                 "-file " + abcfile)

            # 保存sim文件,删除毛发及布料系统
            nodes = cmds.ls(type=['xgmPalette'], l=1)
            if nodes:
                cmds.parent(nodes[0], 'cfxNUL')
                nulls = ['srfNUL', 'fx2NUL']
                for null in nulls:
                    if cmds.objExists(null):
                        cmds.delete(null)
                nulls = ['simNUL', 'hairGrmNUL', 'clothWpNUL']
                for null in nulls:
                    if cmds.objExists(null):
                        cmds.setAttr(null + '.v', 0)
                cmds.delete('simNUL', ch=1)
                cmds.file(rename=simfile)
                cmds.file(f=1, save=1, type=self.format[1])
        else:
            # 选择物体
            cmds.select(self.object, r=1)
            # 加选物体
            if self.abbr in ['rig', 'srf']:
                if cmds.objExists('Sets'):
                    cmds.select("Sets", add=1, ne=1)
            # 导出文件
            if self.abbr == 'asm':
                cmds.file(esfile, f=1, typ=self.format[1], es=1, ch=1, con=1, chn=1, eas=0, sh=1)
            elif self.abbr == 'mod':
                cmds.file(esfile, f=1, typ=self.format[1], es=1, ch=0, con=0, chn=0, eas=0, sh=0)
            elif self.abbr == 'srf':
                if self.category in ['set']:
                    cmds.file(esfile, f=1, typ=self.format[1], es=1, ch=1, con=1, chn=1, eas=0, sh=1)
                else:
                    cmds.file(esfile, f=1, typ=self.format[1], es=1, ch=0, con=0, chn=0, eas=0, sh=1)
            elif self.abbr == 'rig':
                cmds.file(esfile, f=1, typ=self.format[1], es=1, ch=1, con=1, chn=1, eas=0, sh=1)

    def exportMaterialX(self, mfile):
        if cmds.objExists('srfNUL'):
            # 导出mtlx文件
            cmds.select('srfNUL', r=1)
            cmds.arnoldExportToMaterialX(filename=mfile, look="LookA", relative=1, fullPath=0)
            cmds.select(clear=1)

            # 添加mtlx文件内部空间字符
            with open(mfile, 'r') as fo:
                lines = fo.readlines()
            namespace = 'geom="*{}*:'.format(self.task)
            for i in range(len(lines)):
                if 'geom=' in lines[i]:
                    lines[i] = lines[i].replace('geom="', namespace).replace('\n', '')
                else:
                    lines[i] = lines[i].replace('\n', '')
            xmltext = '\n'.join(lines)

            # 覆盖mtlx文件
            with open(mfile, 'w') as fo:
                fo.write(xmltext)

    def publish(self):
        # 保存工程文件
        cmds.file(f=1, save=1)

        # 判断所选物体是否存在
        error = []
        for obj in self.object:
            if not cmds.objExists(obj):
                error.append(obj)
        if error:
            self.SigScriptEditor.emit('error', '所选物体 {} 丢失'.format(self.object))
            return

        # 部门提交规则
        if self.abbr == 'asm':
            # 发布Maya文件
            asmfile = self.verDir.rsplit('/', 3)[0] + '/asm/publish/' + self.task + '_' + self.abbr + self.format[0]
            self.exportFile(asmfile)
            # 创建Json文件
            jsonfile = self.task + '_' + self.abbr + '.json'
            self.writeAsmData(jsonfile)
            # asm/publish文件夹
            os.startfile(self.verDir.rsplit('/', 3)[0] + '/asm/publish')
            self.SigScriptEditor.emit('submit', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                '将asm/publish文件夹下所有文件拖拽到工作/场景引用框')
        else:
            # 创建*/submit/v###文件夹
            cmds.sysFile(self.verDir, makeDir=True)

            # 发布Maya文件
            verfile = self.verDir + '/' + self.task + '_' + self.abbr + self.format[0]
            self.exportFile(verfile)

            # 创建Json文件
            jsonfile = self.task + '_' + self.abbr + '.json'
            self.writeData(jsonfile)

            # 创建definition数据
            self.definition()

            # 打开submit/v###文件夹
            os.startfile(self.verDir)
            if self.abbr == 'mod':
                os.startfile(self.verDir.rsplit('/', 3)[0] + '/asm/publish')
                self.SigScriptEditor.emit('submit', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                    '将submit/v###文件夹下所有文件拖拽到工作/工程审核框\n'
                                                    '将asm/publish文件夹下所有文件拖拽到工作/场景引用框')
            elif self.abbr == 'srf':
                # 发布mtlx文件
                if self.render[0] == 'Arnold' and self.category in ['chr', 'prp', 'veh']:
                    mfile = self.verDir + '/' + self.task + '_srf.mtlx'
                    self.exportMaterialX(mfile)
                self.SigScriptEditor.emit('submit', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                    '将submit/v###文件夹下所有文件拖拽到工作/工程审核框\n'
                                                    '到工作/贴图文件框右上角[...]单击批量上传网盘文件|所有文件')
            elif self.abbr == 'cfx':
                self.SigScriptEditor.emit('submit', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                    '将submit/v###文件夹下所有文件拖拽到工作/工程审核框\n'
                                                    '到工作/描述文件框右上角[...]单击批量上传网盘文件|所有文件')
            else:
                self.SigScriptEditor.emit('submit', '任务数据输出完成,请在CGTW客户端下完成文件提交的工作\n'
                                                    '将submit/v###文件夹下所有文件拖拽到工作/工程审核框')