# -*- coding: utf-8 -*-

def department(abbr=None):
    ddict = {
        "mod": ("assets", "modeling"),
        "rig": ("assets", "rigging"),
        "srf": ("assets", "surfacing"),
        "ldv": ("assets", "lookdev"),
        "cfx": ("assets", "characterFX"),
        "asm": ("assets", "assembly"),
        "lay": ("shots", "layout"),
        "blk": ("shots", "blocking"),
        "ani": ("shots", "animation"),
        "sim": ("shots", "simulation"),
        "efx": ("shots", "effects"),
        "lgt": ("shots", "lighting"),
        "rdr": ("shots", "render"),
        "cmp": ("shots", "compositing")
    }
    if abbr == None:
        return None
    else:
        if len(abbr) == 3:
            # 根据部门简写返回部门全称
            if abbr in ddict:
                return ddict[abbr]
            else:
                return False
        else:
            # 根据部门全称返回部门简写
            ndict = {}
            for k, v in ddict.items():
                ndict[k] = v[1]
            if abbr in ndict.values():
                return list(ndict.keys())[list(ndict.values()).index(abbr)]
            else:
                return False


def fileFormat(abbr=None):
    mfdict = {
        'mod': ['.mb', 'mayaBinary'],
        'rig': ['.mb', 'mayaBinary'],
        'srf': ['.mb', 'mayaBinary'],
        'ldv': ['.mb', 'mayaBinary'],
        'cfx': ['.mb', 'mayaBinary'],
        "asm": (".mb", "mayaBinary"),
        'lay': ['.ma', 'mayaAscii'],
        'blk': ['.ma', 'mayaAscii'],
        'ani': ['.ma', 'mayaAscii'],
        'sim': ['.ma', 'mayaAscii'],
        'efx': ['.hip', ''],
        'lgt': ['.ma', 'mayaAscii'],
        'rdr': ['.ma', 'mayaAscii'],
        'cmp': ['.nuk', '']
    }
    if abbr == None:
        return []
    else:
        return mfdict[abbr]


def packageFormat(abbr=None):
    pfdict = {
        'mod': ['mb', 'abc', 'fbx', 'ass', 'usd', 'json'],
        'rig': ['mb', 'fbx', 'json'],
        'srf': ['mb', 'abc', 'fbx', 'ass', 'usd', 'json'],
        'ldv': ['mb', 'abc', 'fbx', 'ass', 'usd', 'json'],
        'cfx': ['mb', 'json'],
        'asm': ['mb', 'json'],
        'lay': ['ma', 'abc', 'fbx', 'json'],
        'blk': ['ma', 'abc', 'fbx', 'json'],
        'ani': ['ma', 'abc', 'fbx', 'json'],
        'sim': ['ma', 'abc', 'fbx', 'json'],
        'efx': ['ma', 'hip', 'fbx', 'json'],
        'lgt': ['ma', 'json'],
        'rdr': ['ma', 'json'],
        'cmp': ['nuk', 'json']
    }
    if abbr == None:
        return []
    else:
        return pfdict[abbr]