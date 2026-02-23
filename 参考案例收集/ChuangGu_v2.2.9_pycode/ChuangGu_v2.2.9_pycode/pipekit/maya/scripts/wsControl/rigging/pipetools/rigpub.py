# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Rigging Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='rig', tooltip='Rigging Publish Tool')