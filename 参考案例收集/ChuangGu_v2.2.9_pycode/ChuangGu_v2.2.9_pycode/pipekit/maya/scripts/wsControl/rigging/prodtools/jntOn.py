# -*- coding: utf-8 -*-

RELATIVE = 2
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Show Joints'

from tools.rigDisplay import Rigging


def main():
    RIG = Rigging()
    RIG.joints(True)