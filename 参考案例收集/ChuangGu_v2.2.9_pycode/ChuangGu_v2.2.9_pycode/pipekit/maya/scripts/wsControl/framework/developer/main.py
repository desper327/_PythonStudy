# -*- coding: utf-8 -*-

RELATIVE = 0
SUFFIX = None
ICON = 'developer.png'
TOOLTIP = u'开发人员白皮书'

import os
import webbrowser


def main():
    pdffile = os.path.dirname(__file__) + '/whitepaper.pdf'
    try:
        webbrowser.open(pdffile)
    except:
        pass