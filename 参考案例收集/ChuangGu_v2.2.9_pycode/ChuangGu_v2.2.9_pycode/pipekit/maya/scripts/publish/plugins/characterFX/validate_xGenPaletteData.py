# -*- coding: utf-8 -*-

import xgenm as xg
import xgenm.xgGlobal as xgg
import os
import maya.cmds as cmds
from publish import plugin


class ValidateXGenPaletteData(plugin.Validator):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.Validator.order - 1.0
    label = '验证：xGen描述文件'

    def process(self, **kwargs):
        self.error = {}
        task = kwargs['task']
        taskDir = kwargs['taskDir']
        self.xgenDir = taskDir + '/cfx/publish/xgen'
        self.palette = task + '_COL'
        # xGen
        if not cmds.objExists('hairRiggingNUL'):
            raise RuntimeError('缺少层级框架,请单击[验证：大纲层级框架]完成修复')
        else:
            xgmPalette = cmds.ls(type=['xgmPalette'])
            if xgmPalette:
                meshs = cmds.filterExpand('hairGrmNUL', ex=1, sm=12)
                if not meshs:
                    raise ValueError("['hairGrmNUL']总组下必须存在毛发生长体.")
                if not xgmPalette or len(xgmPalette) > 1:
                    raise ValueError("场景内只能存在一个['xgmPalette']类型节点.")
                else:
                    de = xgg.DescriptionEditor
                    oldPalette = de.currentPalette()
                    if oldPalette == '':
                        raise ValueError("未发现可以使用的['xgmPalette']节点,请手动恢复")
                    else:
                        # path
                        oldDataDir = xg.getAttr("xgDataPath", oldPalette).replace('\\', '/')
                        workspace = cmds.workspace(q=1, dir=1, rd=1)
                        oldDataDir = oldDataDir.replace('${PROJECT}', workspace)
                        oldXgenDir =oldDataDir.rsplit('/', 1)[0]
                        if not os.path.exists(oldXgenDir):
                            raise ValueError("请通过['File/Set Project...']菜单功能设置项目工程.\n"
                                             "将工程路径设置到['xgen']上层级文件夹即可.")
                        elif not os.path.exists(oldDataDir):
                            self.error['open'] = oldXgenDir
                            raise ValueError("xgen描述文件数据失效.\n"
                                             "xgmPalette物体命名与['*/xgen/collections']文件夹下的文件夹命名不一致.\n"
                                             "将备份文件夹描述数据拷贝到['*/xgen/collections']文件夹下.")
                        else:
                            size = 0
                            for root, dirs, files in os.walk(oldDataDir):
                                size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
                            if size == 0:
                                self.error['open'] = oldDataDir
                                raise ValueError("xgen描述文件数据丢失.\n"
                                                 "到['*/xgen/collections']文件夹下手动排查或修复错误.\n"
                                                 "描述文件夹 {} 数据为0kb,请从备份文件夹恢复数据.".format([oldPalette]))
                            else:
                                newDataDir = self.xgenDir + '/collections/' + self.palette
                                if oldDataDir != newDataDir:
                                    self.error['path'] = [oldDataDir, newDataDir]

                if self.error:
                    raise RuntimeError("xgmPalette描述数据路径错误.\n"
                                       "单击['repair']按钮前请确保<*/xgen/collections>数据正确加载.\n"
                                       "单击['repair']按钮自动完成修复工作.")

    def repair(self, args):
        # 拷贝xgen文件夹到服务器
        if 'path' in self.error or 'name' in self.error:
            xgmPalette = cmds.ls(type='xgmPalette')
            if 'path' in self.error:
                cmds.sysFile(self.error['path'][1], makeDir=True)
                os.system('xcopy "' + self.error['path'][0] + '" "' + self.error['path'][1] + '" /e/y')
                xg.setAttr('xgDataPath', str(self.error['path'][1]), str(xgmPalette[0]))
        else:
            if 'open' in self.error:
                os.startfile(self.error['open'])
            raise ValueError("请手动解决存在的错误.")