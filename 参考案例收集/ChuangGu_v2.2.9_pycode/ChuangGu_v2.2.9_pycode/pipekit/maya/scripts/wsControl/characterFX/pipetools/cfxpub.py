# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'publish.png'
TOOLTIP = 'CharacterFX Publish Tool'

from publish import publishMain as PM


def main():
    PM.Publish(abbr='cfx', tooltip='CharacterFX Publish Tool')