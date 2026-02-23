# -*- coding: utf-8 -*-

from publish import plugin


class ValidateSaveWorked(plugin.MayaCollector):
    ''' Check whether the currently opened file is a project work file. '''

    label = '验证：场景工程文件'
    order = plugin.Validator.order + 4.5

    def process(self, **kwargs):
        self.work = self.workFilePath()
        if self.work == False:
            raise RuntimeError('请切换至存档菜单完成工程新版发布.')