# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Surfacing Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='srf', tooltip='Surfacing Publish Tool')