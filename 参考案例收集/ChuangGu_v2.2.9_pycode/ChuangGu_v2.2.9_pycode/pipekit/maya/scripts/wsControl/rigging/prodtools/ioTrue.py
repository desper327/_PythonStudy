# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Show Intermediate Objects'

from tools.rigDisplay import Rigging


def main():
    RIG = Rigging()
    RIG.intermediateObjects(True)