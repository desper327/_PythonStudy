# -*- coding: utf-8 -*-

import os
import json


def project(jsonfile):
    if not os.path.exists(jsonfile):
        return {}
    else:
        with open(jsonfile, 'r') as fo:
            return json.load(fo)


def stage(jsonfile):
    if not os.path.exists(jsonfile):
        return ['none']
    else:
        with open(jsonfile, 'r') as fo:
            text = fo.read()
            fdict = json.loads(text)
        ver = fdict.keys()
        ver.sort(reverse=True)
        if 'stage' in fdict[ver[0]]:
            return fdict[ver[0]]['stage']
        else:
            return ['null']