# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'production.png'
TOOLTIP = 'Checking MeshShape Naming'

from tools import simRename


def main():
    simRename.naming()