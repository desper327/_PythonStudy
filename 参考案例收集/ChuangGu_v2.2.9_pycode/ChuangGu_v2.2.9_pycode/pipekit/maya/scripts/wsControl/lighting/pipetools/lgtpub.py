# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Lighting Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='lgt', tooltip='Lighting Publish Tool')