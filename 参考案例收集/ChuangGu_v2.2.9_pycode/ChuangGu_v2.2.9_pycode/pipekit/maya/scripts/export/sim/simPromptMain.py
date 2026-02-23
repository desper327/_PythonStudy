# -*- coding: utf-8 -*-

'''
import os
import sys
SCRIPTPATH = os.path.dirname(__file__)
if SCRIPTPATH not in sys.path:
    sys.path.append(SCRIPTPATH)
'''
try:
    import maya.standalone
    maya.standalone.initialize('mayapy')
    from export.sim import simPromptCmds
    MX = simPromptCmds.Export()
    MX.apply()
except:
    pass