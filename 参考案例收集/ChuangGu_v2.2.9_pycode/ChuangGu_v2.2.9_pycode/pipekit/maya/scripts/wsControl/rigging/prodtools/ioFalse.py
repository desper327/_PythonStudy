# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Hidden Intermediate Objects'

from tools.rigDisplay import Rigging


def main():
    RIG = Rigging()
    RIG.intermediateObjects(False)