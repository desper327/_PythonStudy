# -*- coding: utf-8 -*-

import os
import maya.cmds as cmds
import maya.mel as mel
from stat import S_IWUSR, S_IREAD
from publish import plugin


class ValidateNoMaliciousScripts(plugin.Validator):
    ''' Checks that there are no unknown nodes. '''
    order = plugin.Validator.order + 3.5
    label = '验证：没有恶意脚本'

    def process(self, **kwargs):
        self.forces = [
            'leukocyte.antivirus()',
            'autoUpdatoAttrEnd()',
            'look()',
            'sysytenasdasdfsadfsdaf_dsfsdfaasd'
        ]
        self.malicious = [
            'MayaMelUIConfigurationFile',
            'sysytenasdasdfsadfsdaf_dsfsdfaasd',
            'script',
            'breed_gene',
            'vaccine_gene'
        ]

        # 日期破解
        mel.eval('global proc autoUpdatoAttrEnd(){}')
        mel.eval('global proc look(){}')
        mel.eval('global int $autoUpdateAttrEd_aoto_int=1;')

        # 进程脚本
        scriptJobs = cmds.scriptJob(listJobs=1)
        for iscriptJob in scriptJobs:
            for iforce in self.forces:
                if iforce in iscriptJob:
                    # 终止脚本进程
                    index = int(iscriptJob.split(':')[0])
                    cmds.scriptJob(kill=index, force=1)

        # 感染的脚本
        self.error = {
            'scripts': {},
            'mel': {},
            'py': {},
            'vaccine': {}
        }
        scripts = cmds.ls(type='script')
        if scripts:
            for script in scripts:
                for maliciou in self.malicious:
                    lscript = script.split(':')[-1]
                    if maliciou in lscript:
                        before = cmds.getAttr(script + '.before')
                        # 镜头
                        if cmds.referenceQuery(script, isNodeReferenced=1) == 1:
                            if before != '':
                                self.error['scripts'][script] = 'empty'
                        # 资产
                        else:
                            if maliciou == 'script':
                                if '////****************************************////' in before or before == '':
                                    self.error['scripts'][script] = 'delete'
                            else:
                                self.error['scripts'][script] = 'delete'

        # 感染的userSetup.mel
        scriptsDir = cmds.internalVar(uad=True)+'scripts'
        userSetupMel = scriptsDir+'/userSetup.mel'
        if os.path.exists(userSetupMel):
            with open(userSetupMel, 'r') as fo:
                text = fo.read()

            if all([len(text) >= 4118,
                    '// Maya Mel UI Configuration File.Maya Mel UI Configuration File..\n// \n//\n//  This script is machine generated.  Edit at your own risk' in text,
                    'string $chengxu' in text]):
                self.error['mel'][userSetupMel] = 'delete'

        # 感染的userSetup.py
        userSetupPy = scriptsDir+'/userSetup.py'
        if os.path.exists(userSetupPy):
            with open(userSetupPy, 'r') as fo:
                text = fo.read()

            if 'leukocyte.occupation()' in text:
                self.error['py'][userSetupPy] = 'delete'

        # 删除vaccine文件
        files = ['vaccine.py', 'vaccine.pyc']
        for ifile in files:
            vaccine = scriptsDir + '/' + ifile
            if os.path.exists(vaccine):
                self.error['vaccine'][vaccine] = 'delete'

        if self.error['scripts']:
            raise ValueError('场景内工作脚本被感染,单击[repair]按钮完成自动修复.')
        elif self.error['mel']:
            raise ValueError('userSetup.mel 文件被感染,单击[repair]按钮完成自动修复.')
        elif self.error['py']:
            raise ValueError('userSetup.py 文件被感染,单击[repair]按钮完成自动修复.')
        elif self.error['vaccine']:
            raise ValueError("['vaccine.py', vaccine.pyc'] 为恶意脚本文件,单击[repair]按钮完成自动修复.")

    def repair(self, args):
        if self.error['scripts']:
            for k, v in self.error['scripts'].items():
                if v == 'empty':
                    cmds.scriptNode(k, e=1, beforeScript='')
                elif v == 'delete':
                    cmds.delete(k)

        if self.error['mel']:
            k, v = self.error['mel'].items()[0]
            if v == 'delete':
                os.chmod(k, S_IWUSR | S_IREAD)
                os.remove(k)

        if self.error['py']:
            k, v = self.error['py'].items()[0]
            if v == 'delete':
                os.chmod(k, S_IWUSR | S_IREAD)
                os.remove(k)

        if self.error['vaccine']:
            k, v = self.error['vaccine'].items()[0]
            if v == 'delete':
                os.chmod(k, S_IWUSR | S_IREAD)
                os.remove(k)