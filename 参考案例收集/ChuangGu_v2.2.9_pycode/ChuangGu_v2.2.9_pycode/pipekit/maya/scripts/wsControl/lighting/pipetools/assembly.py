# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'import.png'
TOOLTIP = 'Lighting Merge Tool'

from merge.lgt import lgtMergeMain as LMM


def main():
    LMM.Merge(abbr='lgt', tooltip='Lighting Merge Tool')
