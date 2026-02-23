# -*- coding: utf-8 -*-

RELATIVE = 2
SUFFIX = None
ICON = 'export.png'
TOOLTIP = 'Simulation Export Tool'

from export.sim import simExportMain as SEM


def main():
    SEM.main()