# -*- coding: utf-8 -*-

import maya.cmds as cmds
from publish import plugin


class ValidateNoOnModelChange3dc(plugin.Validator):
    ''' Checks that there are no unknown nodes. '''
    order = plugin.Validator.order + 4.0
    label = '验证：没有恶意控件'

    def process(self, **kwargs):
        self.error = {
            'fixing': False,
            'script': {}
        }

        script = cmds.ls(type='script')
        if script:
            for i in script:
                if 'uiConfigurationScriptNode' in i:
                    expression_str = cmds.getAttr(i + '.before')
                    expression_lines = []
                    for line in expression_str.split('\n'):
                        if '-editorChanged "onModelChange3dc"' in line:
                            self.error['fixing'] = True
                            continue
                        expression_lines.append(line)
                    fixed_expression = '\n'.join(expression_lines)
                    self.error['script'][i] = fixed_expression
            if self.error['fixing']:
                raise RuntimeError("找到恶意控件: {}".format(self.error))

    def repair(self, args):
        if self.error['script']:
            for k, v in self.error['script'].items():
                cmds.setAttr(k + '.before', v, type='string')