# -*- coding: utf-8 -*-

RELATIVE = 2
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Blocking Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='blk', tooltip='Blocking Publish Tool')