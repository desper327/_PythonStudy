# -*- coding: utf-8 -*-

RELATIVE = 4
SUFFIX = None
ICON = 'export.png'
TOOLTIP = 'Animation Export Tool'

from export.ani import aniExportMain as ABC


def main():
    ABC.main()