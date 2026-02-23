# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'Simulation Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='sim', tooltip='Simulation Publish Tool')