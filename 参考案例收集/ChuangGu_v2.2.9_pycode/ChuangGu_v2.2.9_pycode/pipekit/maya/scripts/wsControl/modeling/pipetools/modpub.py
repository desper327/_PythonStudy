# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Model Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='mod', tooltip='Model Publish Tool')