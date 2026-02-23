# -*- coding: utf-8 -*-

RELATIVE = 1
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Export Materials'

from tools.comTransferMat import materialsJson


def main():
    materialsJson('export')