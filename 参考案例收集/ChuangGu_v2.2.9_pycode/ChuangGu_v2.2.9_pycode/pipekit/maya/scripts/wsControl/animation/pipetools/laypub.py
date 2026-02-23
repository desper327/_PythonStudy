# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Layout Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='lay', tooltip='Layout Publish Tool')