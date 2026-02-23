# -*- coding: utf-8 -*-

RELATIVE = 3
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Animation Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='ani', tooltip='Animation Publish Tool')