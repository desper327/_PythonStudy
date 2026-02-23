# -*- coding: utf-8 -*-

RELATIVE = 2
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Import Materials'

from tools.comTransferMat import materialsJson


def main():
    materialsJson('import')