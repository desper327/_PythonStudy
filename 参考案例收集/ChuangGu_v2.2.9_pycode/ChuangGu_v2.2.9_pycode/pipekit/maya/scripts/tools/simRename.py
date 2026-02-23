# -*- coding: utf-8 -*-

from maya import cmds
from core import interface
import logging

LOG = logging.getLogger('Simulation')

def naming():
    # 服务日期
    if not interface.license():
        LOG.warning(u'到期不在提供服务.')
        return

    nulls = cmds.ls('*:srfNUL')
    if nulls:
        error = {}
        for null in nulls:
            meshes = cmds.filterExpand(null, ex=1, sm=12)
            if meshes:
                for mesh in meshes:
                    cshape = cmds.listRelatives(mesh, shapes=1, path=1, ni=1)[0]
                    nshape = mesh.split(':')[-1] + 'Shape'
                    if cshape.split(':')[-1] != nshape:
                        error[cshape] = nshape
        if error:
            repair = []
            for k, v in error.items():
                try:
                    cmds.rename(k, v)
                except:
                    repair.append(k)
            if repair:
                cmds.select(repair, r=1)
                LOG.warning(u'修复失败,未能修复的对象已被选择')
        else:
            LOG.info(u'验证通过,请通过[simabc]工具输出Alembic缓存')
    else:
        LOG.info(u'无效检查,场景内未找到检查对象')