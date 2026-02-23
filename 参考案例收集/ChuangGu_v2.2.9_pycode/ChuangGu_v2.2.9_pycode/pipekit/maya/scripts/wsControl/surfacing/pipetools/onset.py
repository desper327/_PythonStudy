# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Model Scene Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='asm', tooltip='Model Scene Publish Tool')