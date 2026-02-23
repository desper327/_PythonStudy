# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'import.png'
TOOLTIP = 'Build Reference Assets Tool'

from build import buildMain


def main():
    buildMain.main()