# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class CollectOutlinerRules(plugin.MayaCollector):
    ''' Checks that there are no display layers in the current scene. '''
    order = plugin.MayaCollector.order + 0.5
    label = '收集：引用节点规则'

    def process(self, **kwargs):
        task = kwargs['task']
        exist = []
        error = []
        setAR = task + '_set_AR'
        setARs = cmds.ls(task + '_set_AR*')
        for i in setARs:
            if i == setAR:
                exist.append(i)
            else:
                error.append(i)

        if not exist:
            raise RuntimeError('请切回存档菜单选择存档文件后单击[打开]按钮\n'
                               '已经创建的env_AR会丢失,请先另存为临时文件.')
        elif error:
            raise RuntimeError("场景内只能存在一个['{}_set_AR']文件,请手动删除多余的[*_set_AR*]文件".format(task))
        else:
            ds = cmds.ls('*_env_DS')
            if not ds:
                raise RuntimeError("场景内至少存在一个['*_env_DS']关联复制组,反之没有二次提交的意义.")
            else:
                empty = []
                for i in ds:
                    child = cmds.listRelatives(i, children=1)
                    if not child:
                        empty.append(i)
                if empty:
                    raise RuntimeError("关联复制组 {} 下缺少代理文件,双击图标完成修复或删除关联复制空组".format(empty))