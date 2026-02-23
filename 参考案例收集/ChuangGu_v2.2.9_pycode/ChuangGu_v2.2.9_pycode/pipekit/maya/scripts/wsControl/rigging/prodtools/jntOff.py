# -*- coding: utf-8 -*-

RELATIVE = 3
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Hidden Joints'

from tools.rigDisplay import Rigging


def main():
    RIG = Rigging()
    RIG.joints(False)