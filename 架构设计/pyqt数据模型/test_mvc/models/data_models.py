"""
业务数据模型 - 使用Pydantic进行数据验证
这些模型独立于UI框架，可以在任何地方使用
"""
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

#{'project.entity': 'SJLXS', 'project.full_name': '三界旅行社', 'project.id': 'E9C54612-4E32-41EE-A7C6-7F1318DF13B7', 'project.status': 'Active', 
# 'project.database': 'proj_sjlxs', 'project.color': '', 'project.start_date': '', 'project.end_date': '', 
# 'project.image': '[{"max": "/upload/public/00000000/57a6f79c5791af45fcf8b975c7f4a7bb.png", 
# "min": "/upload/public/00000000/57a6f79c5791af45fcf8b975c7f4a7bb_min.png", "type": "image", 
# "att_id": "71C237DC-BC00-BD50-397B-3AFE9A8CC3ED"}]', 'project.description': '', 'project.frame_rate': '', 
# 'project.resolution': '', 'project.create_time': '2025-10-28 09:43:36', 'project.create_by': '黄斌凯', 
# 'project.last_update_time': '2025-10-28 09:47:09', 'project.last_update_by': '黄斌凯', 'project.template': 
# commonTemplate', 'project.tag': '', 'project.is_etask': '', 'project.project_group': '', 
# 'project.template_id': '38A86ED1-64FB-4988-BC3C-FFCDE433AFC8', 'project.maya_version': '', 'project.ue_version': '', 
# 'project.arnold_version': '', 'project.ae_version': '', 'project.pr_version': '', 'project.nuke_version': '', 
# 'project.zb_version': '', 'project.cfx_houdini_version': '', 'project.vfx_houdini_version': '', 'project.task_jc': '', 
# 'id': 'E9C54612-4E32-41EE-A7C6-7F1318DF13B7'}
class Project(BaseModel):
    """项目数据模型"""
    project_entity: str = Field(..., alias='project.entity', min_length=1, max_length=100, description="项目实体")
    project_full_name: str = Field(..., alias='project.full_name', min_length=1, max_length=100, description="项目全名")
    project_id: str = Field(..., alias='project.id', min_length=1, max_length=100, description="项目ID")
    project_status: str = Field(..., alias='project.status', min_length=1, max_length=100, description="项目状态")
    project_database: str = Field(..., alias='project.database', min_length=1, max_length=100, description="项目数据库")
    #project_color: str = Field(..., alias='project.color', description="项目颜色")
    #project_start_date: str = Field(..., alias='project.start_date', description="项目开始日期")
    #project_end_date: str = Field(..., alias='project.end_date', description="项目结束日期")
    #project_image: str = Field(..., alias='project.image', description="项目图片")
    #project_description: Optional[str] = Field(None, alias='project.description', max_length=500, description="项目描述")
    project_frame_rate: Optional[str] = Field(None, alias='project.frame_rate', description="帧率")
    project_resolution: Optional[str] = Field(None, alias='project.resolution', description="分辨率")
    #project_create_time: str = Field(..., alias='project.create_time', description="创建时间")
    #project_create_by: str = Field(..., alias='project.create_by', description="创建者")
    #project_last_update_time: str = Field(..., alias='project.last_update_time', description="最后更新时间")
    #project_last_update_by: str = Field(..., alias='project.last_update_by', description="最后更新者")
    project_template: str = Field(..., alias='project.template', description="项目模板")
    #project_tag: str = Field(..., alias='project.tag', description="项目标签")
    #project_is_etask: str = Field(..., alias='project.is_etask', description="是否为Etask项目")
    #project_project_group: str = Field(..., alias='project.project_group', description="项目组")
    #project_template_id: str = Field(..., alias='project.template_id', description="模板ID")
    project_maya_version: str = Field(..., alias='project.maya_version', description="Maya版本")
    project_ue_version: str = Field(..., alias='project.ue_version', description="UE版本")
    project_arnold_version: str = Field(..., alias='project.arnold_version', description="Arnold版本")
    #project_ae_version: str = Field(..., alias='project.ae_version', description="AE版本")
    #project_pr_version: str = Field(..., alias='project.pr_version', description="PR版本")
    project_nuke_version: str = Field(..., alias='project.nuke_version', description="Nuke版本")
    #project_zb_version: str = Field(..., alias='project.zb_version', description="ZB版本")
    project_cfx_houdini_version: str = Field(..., alias='project.cfx_houdini_version', description="CFX Houdini版本")
    project_vfx_houdini_version: str = Field(..., alias='project.vfx_houdini_version', description="VFX Houdini版本")
    project_task_jc: str = Field(..., alias='project.task_jc', description="任务简称")
    
    
    @field_validator('project_entity')
    def project_entity_must_not_be_empty(cls, v):
        """验证项目名称不能为空或只包含空格"""
        if not v or not v.strip():
            raise ValueError('项目名称不能为空')
        return v.strip()
    
    


class Stage(BaseModel):
    """阶段数据模型"""
    entity: str = Field(..., alias='entity', min_length=1, max_length=100, description="阶段实体")
    module: str = Field(..., alias='module', min_length=1, max_length=100, description="模块")
    module_type: str = Field(..., alias='module_type', min_length=0, max_length=100, description="模块类型")
    description: str = Field(..., alias='description', min_length=0, max_length=500, description="描述")


class Episode(BaseModel):
    eps_entity: str = Field(..., alias='eps.entity', min_length=0, max_length=100)
    eps_id: str = Field(..., alias='eps.id', min_length=0, max_length=100)
    eps_url: str = Field(..., alias='eps.url', min_length=0, max_length=100)
    eps_project_code: str = Field(..., alias='eps.project_code', min_length=0, max_length=100)
    eps_status: str = Field(..., alias='eps.status', min_length=0, max_length=100)
    eps_link_asset: str = Field(..., alias='eps.link_asset', min_length=0, max_length=100)


class Scene(BaseModel):
    eps_entity: str = Field(..., alias='eps.entity', min_length=0, max_length=100)
    eps_id: str = Field(..., alias='eps.id', min_length=0, max_length=100)
    eps_url: str = Field(..., alias='eps.url', min_length=0, max_length=100)
    eps_status: str = Field(..., alias='eps.status', min_length=0, max_length=100)
    sc_entity:str = Field(..., alias='seq.entity', min_length=0, max_length=100)
    sc_id:str = Field(..., alias='seq.id', min_length=0, max_length=100)
    sc_url:str = Field(..., alias='seq.url', min_length=0, max_length=100)
    sc_status:str = Field(..., alias='seq.status', min_length=0, max_length=100)
    sc_link_asset:str = Field(..., alias='seq.link_asset', min_length=0, max_length=100)
    seq_link_eps:str = Field(..., alias='seq.link_eps', min_length=0, max_length=100)


class Shot(BaseModel):
    eps_entity: str = Field(..., alias='eps.entity', min_length=0, max_length=100)
    eps_id: str = Field(..., alias='eps.id', min_length=0, max_length=100)
    eps_url: str = Field(..., alias='eps.url', min_length=0, max_length=100)
    sc_entity:str = Field(..., alias='seq.entity', min_length=0, max_length=100)
    sc_id:str = Field(..., alias='seq.id', min_length=0, max_length=100)
    sc_url:str = Field(..., alias='seq.url', min_length=0, max_length=100)
    sc_status:str = Field(..., alias='seq.status', min_length=0, max_length=100)
    shot_entity:str = Field(..., alias='shot.entity', min_length=0, max_length=100)
    shot_id:str = Field(..., alias='shot.id', min_length=0, max_length=100)
    shot_url:str = Field(..., alias='shot.url', min_length=0, max_length=100)
    shot_status:str = Field(..., alias='shot.status', min_length=0, max_length=100)
    shot_vfx_note:str = Field(..., alias='shot.vfx_note', min_length=0, max_length=500)
