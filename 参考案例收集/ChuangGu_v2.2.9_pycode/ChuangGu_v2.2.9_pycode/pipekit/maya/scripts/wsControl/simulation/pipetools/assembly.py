# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'import.png'
TOOLTIP = 'Simulation Merge Tool'

from merge.sim import simMergeMain as SMM


def main():
    SMM.Merge(abbr='sim', tooltip='Simulation Merge Tool')