# -*- coding: utf-8 -*-

import re
import os
import time
import maya.cmds as cmds
from publish import plugin
from publish.gui import editorWidget as Editor


class ValidateFileTextureFormat(plugin.Validator):
    ''' Checks that the turtle plug-in is disabled. '''
    order = plugin.Validator.order + 0.5
    label = '验证：贴图文件规则'
    actions = ['editor']
    ignoreType = ['shots', 'asm', 'mod', 'rig']

    def process(self, **kwargs):
        render = kwargs['render']
        abbr = kwargs['department']
        if abbr == 'cfx':
            self.imagesDir = kwargs['taskDir'] + '/' + abbr + '/publish/xgen/images'
        else:
            self.imagesDir = kwargs['taskDir'] + '/' + abbr + '/images'
        self.instance = kwargs['instance']
        lgtExts = ['rstexbin', 'tx']
        subExts = ['jpg', 'png', 'tif']
        if abbr == 'cfx':
            subExts.append('iff')

        self.uidirct = {
            'mis': {
                'title': None,
                'files': []
            },
            'ext': {
                'title': None,
                'files': []
            },
            'sub': {
                'title': None,
                'files': []
            },
            'str': {
                'title': None,
                'files': []
            },
            'img': {
                'title': None,
                'files': []
            },
            'dir': {
                'title': None,
                'files': []
            },
            'error': None
        }

        # redshift.map
        if render[0] == 'Redshift':
            files = cmds.ls(type=['file', 'RedshiftCameraMap', 'RedshiftNormalMap'])
        else:
            files = cmds.ls(type=['file'])
        if files:
            files.sort(reverse=False)
            for f in files:
                if cmds.nodeType(f) == 'file':
                    attr = 'fileTextureName'
                    # 象限
                    utm = cmds.getAttr(f + '.uvTilingMode')
                    # 序列
                    ufe = cmds.getAttr(f + '.useFrameExtension')
                else:
                    attr = 'tex0'
                    utm = 0
                    ufe = False
                path = cmds.getAttr(f + '.' + attr)
                if not path:
                    self.uidirct['mis']['files'].append({f: path})
                else:
                    '''
                    {
                        dirs[0]: '文件完整路径', 
                        dirs[1]: '文件扩展格式'
                    }
                    '''
                    dirs = path.rsplit('.', 1)
                    if len(dirs) == 1:
                        self.uidirct['mis']['files'].append({f: path})
                    elif dirs[1].lower() in lgtExts:
                        subFile = []
                        for e in subExts:
                            efile = dirs[0] + '.' + e
                            if os.path.exists(efile):
                                subFile.append(efile)
                                cmds.setAttr(f + '.' + attr, efile, type='string')
                                break
                        if not subFile:
                            self.uidirct['ext']['files'].append({f: path})
                    else:
                        if dirs[1].lower() not in subExts:
                            self.uidirct['sub']['files'].append({f: path})
                        else:
                            '''
                            {
                                name[0]: '文件根路径', 
                                name[1]: '文件名称'
                            }
                            '''
                            name = dirs[0].rsplit('/', 1)
                            if re.findall(u'[\u4e00-\u9fff]+', name[0]):
                                self.uidirct['str']['files'].append({f: path})
                            else:
                                # 图片象限或序列,使用象限或序列进行数字判断
                                if utm == 3 or ufe == True:
                                    if bool(re.search(r'\d', name[1])) == True:
                                        template = re.sub(r'\d', '*', name[1]) + '.' + dirs[1]
                                        udims = cmds.getFileList(fld=name[0], fs=template)
                                        if not udims:
                                            self.uidirct['img']['files'].append({f: path})
                                        else:
                                            for udim in udims:
                                                if self.imagesDir != name[0]:
                                                    self.uidirct['dir']['files'].append({f: name[0] + '/' + udim})
                                # 常规图片
                                else:
                                    if not os.path.exists(path):
                                        self.uidirct['img']['files'].append({f: path})
                                    else:
                                        sfile = self.imagesDir + '/' + name[1] + '.' + dirs[1]
                                        if sfile != path:
                                            self.uidirct['dir']['files'].append({f: path})
        if self.uidirct['mis']['files']:
            self.uidirct['error'] = 'mis'
            self.uidirct['mis']['title'] = '贴图路径禁止为空.'
            raise ValueError("贴图路径禁止为空.\n"
                             "单击['editor']在子集界面单击按钮选择错误对象.\n"
                             "如果不需要file节点请手动删除.")
        elif self.uidirct['ext']['files']:
            self.uidirct['error'] = 'ext'
            self.uidirct['ext']['title'] = '贴图文件格式错误.'
            raise ValueError("贴图文件格式错误.\n"
                             "单击['editor']在子集界面单击按钮选择错误对象.\n"
                             "提交文件时禁止贴图读取格式为{}.".format(lgtExts))
        elif self.uidirct['sub']['files']:
            self.uidirct['error'] = 'sub'
            self.uidirct['sub']['title'] = '贴图文件格式错误.'
            raise ValueError("贴图文件格式错误.\n"
                             "单击['editor']在子集界面单击按钮选择错误对象.\n"
                             "提交文件时贴图读取格式必须为{}.".format(subExts))
        elif self.uidirct['str']['files']:
            self.uidirct['error'] = 'str'
            self.uidirct['str']['title'] = '贴图文件包含中文.'
            raise ValueError("贴图文件包含中文.\n"
                             "单击['editor']在子集界面单击按钮选择错误对象.\n"
                             "请手动完成文件命名修改.")
        elif self.uidirct['img']['files']:
            self.uidirct['error'] = 'img'
            self.uidirct['img']['title'] = '贴图读取文件丢失.'
            raise ValueError("贴图读取文件丢失.\n"
                             "单击['editor']在子集界面单击按钮选择错误对象.\n"
                             "请将丢失的贴图文件手动拷贝到读取路径下.")
        elif self.uidirct['dir']['files']:
            self.uidirct['error'] = 'dir'
            self.uidirct['dir']['title'] = '贴图文件目录错误.'
            raise ValueError("贴图文件目录错误.\n"
                             "单击['repair']自动完成文件拷贝及路径设置.")

    def editor(self):
        win = Editor.Ui_Form(**self.uidirct)
        # Delete existing UI
        try:
            cmds.deleteUI('FileEditor')
        except:
            pass
        win.setObjectName('FileEditor')
        win.show()

    def repair(self, args):
        if self.uidirct['error'] == 'dir':
            cmds.sysFile(self.imagesDir, makeDir=True)
            self.instance.label.setVisible(False)
            self.instance.version.setVisible(False)
            self.instance.progressBar.setVisible(True)
            self.instance.progressBar.setStyleSheet('''
                QProgressBar::chunk { 
                    background-color: rgb(150,75,150); 
                }
            ''')
            error = self.uidirct['dir']['files']
            m = 100.0/len(error)
            n = 0
            repeat = []
            for i in error:
                cmds.refresh()
                filename = i.keys()[0]
                oldfile = i.values()[0]
                n += 1
                p = n * m
                if cmds.nodeType(filename) == 'file':
                    attr = 'fileTextureName'
                else:
                    attr = 'tex0'
                newfile = self.imagesDir + '/' + oldfile.split('/')[-1]
                if not os.path.exists(newfile):
                    cmds.sysFile(oldfile, copy=newfile)
                if filename not in repeat:
                    repeat.append(filename)
                    getfile = cmds.getAttr(filename + '.' + attr)
                    setfile = self.imagesDir + '/' + getfile.split('/')[-1]
                    cmds.setAttr(filename + '.' + attr, setfile, type='string')
                self.instance.progressBar.setValue(p)
            time.sleep(0.5)
            self.instance.label.setVisible(True)
            self.instance.version.setVisible(True)
            self.instance.progressBar.setVisible(False)
        else:
            raise ValueError("单击['editor']打开子集界面.\n"
                             "左侧file节点名称的按钮都可以单击."
                             "单击按钮选择对象手动完成对问题的修复.")