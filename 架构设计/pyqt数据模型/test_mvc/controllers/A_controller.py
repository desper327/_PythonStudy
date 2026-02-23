import sys
import os
import traceback
import tomllib

from PySide6.QtWidgets import QApplication
from views.A_view import A_view
from models.A_model import A_model
from models.data_models import Project,Stage,Episode,Scene,Shot

from config import cgt,Yprint



class A_controller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.A_view = A_view()
        self.login()

        self.A_model = A_model()
        self.connect_view_signals()
        self.connect_model_signals()
        
        self.init_model()
    
    def run(self):
        self.A_view.show()
        sys.exit(self.app.exec())

    def login(self):
        cgt.login()
    
    def init_model(self):
        # 从cgt获取原始项目数据（字典列表）
        raw_projects_data = cgt.get_project_data()
        
        # 将字典列表转换为Project模型实例列表
        # Pydantic会根据我们设置的别名（alias）自动匹配字段
        self.A_model.projects = [Project.model_validate(data) for data in raw_projects_data]
        

    def connect_view_signals(self):
        # ==连接view的信号和槽==
        self.A_view.comboBox_proj.currentIndexChanged.connect(self.comboBox_proj_selected_changed)
        self.A_view.comboBox_stage.currentIndexChanged.connect(self.comboBox_stage_selected_changed)
        self.A_view.comboBox_eps.currentIndexChanged.connect(self.comboBox_eps_selected_changed)
        self.A_view.comboBox_sc.currentIndexChanged.connect(self.comboBox_sc_selected_changed)
        self.A_view.comboBox_shot.currentIndexChanged.connect(self.comboBox_shot_selected_changed)
        self.A_view.checkBox_mytask.stateChanged.connect(self.checkBox_mytask_stateChanged)
    
    def connect_model_signals(self):
        # ==连接model的信号和槽==
        self.A_model.projects_changed.connect(self.handle_projects_changed)
        self.A_model.current_project_changed.connect(self.handle_current_project_change)
        self.A_model.stages_changed.connect(self.handle_stages_changed)
        self.A_model.current_stage_changed.connect(self.handle_current_stage_changed)
        self.A_model.episodes_changed.connect(self.handle_episodes_changed)
        self.A_model.current_eps_changed.connect(self.handle_current_eps_changed)
        self.A_model.scenes_changed.connect(self.handle_scenes_changed)
        self.A_model.current_sc_changed.connect(self.handle_current_sc_changed)
        self.A_model.shots_changed.connect(self.handle_shots_changed)
        self.A_model.current_shot_changed.connect(self.handle_current_shot_changed)
        self.A_model.mytask_changed.connect(self.handle_mytask_changed)


    # ==处理view的信号==
    def comboBox_proj_selected_changed(self, index):
        Yprint(self.A_model.projects[index])
        self.A_model.current_project = self.A_model.projects[index]

    def comboBox_stage_selected_changed(self, index):
        Yprint(self.A_model.stages[index])
        self.A_model.current_stage = self.A_model.stages[index]

    def comboBox_eps_selected_changed(self):
        self.A_model.current_eps = self.A_model.episodes[self.A_view.comboBox_eps.currentIndex()]

    def comboBox_sc_selected_changed(self):
        self.A_model.current_sc = self.A_model.scenes[self.A_view.comboBox_sc.currentIndex()]

    def comboBox_shot_selected_changed(self):
        self.A_model.current_shot = self.A_model.shots[self.A_view.comboBox_shot.currentIndex()]

    def checkBox_mytask_stateChanged(self):
        self.A_model.mytask = self.A_view.checkBox_mytask.isChecked()



    # ==处理model的信号==
    def handle_projects_changed(self, projects):
        self.update_comboBox_without_next_signal(self.A_view.comboBox_proj,[project.project_full_name for project in projects])


    def handle_current_project_change(self):
        self.A_model.stages = [Stage.model_validate(data) for data in cgt.get_stage_in_project_by_module(self.A_model.current_project.project_database)]
        self.update_project_settings_info()
        self.A_model.episodes = [Episode.model_validate(data) for data in cgt.get_eps_by_project_db(self.A_model.current_project.project_database)]


    def handle_stages_changed(self):
        self.update_comboBox_without_next_signal(self.A_view.comboBox_stage,[stage.entity for stage in self.A_model.stages if stage.module == 'shot'])
        self.A_model.current_stage = self.A_model.stages[self.A_view.comboBox_stage.currentIndex()]

    def handle_current_stage_changed(self):
        self.get_task("handle_current_stage_changed")


    def handle_episodes_changed(self):
        Yprint(self.A_model.episodes)
        self.update_comboBox_without_next_signal(self.A_view.comboBox_eps,[eps.eps_entity for eps in self.A_model.episodes])
        self.A_model.current_eps = self.A_model.episodes[self.A_view.comboBox_eps.currentIndex()]


    def handle_scenes_changed(self):
        Yprint(self.A_model.scenes)
        self.update_comboBox_without_next_signal(self.A_view.comboBox_sc,[sc.sc_entity for sc in self.A_model.scenes \
            if sc.eps_entity == self.A_model.current_eps.eps_entity])
        self.A_model.current_sc = self.A_model.scenes[self.A_view.comboBox_sc.currentIndex()]

    def handle_shots_changed(self):
        Yprint(self.A_model.shots)
        self.update_comboBox_without_next_signal(self.A_view.comboBox_shot,[shot.shot_entity for shot in self.A_model.shots \
            if shot.sc_entity == self.A_model.current_sc.sc_entity and shot.eps_entity == self.A_model.current_eps.eps_entity])
        self.A_model.current_shot = self.A_model.shots[self.A_view.comboBox_shot.currentIndex()]

    def handle_current_eps_changed(self):
        self.A_model.scenes = [Scene.model_validate(data) for data in cgt.get_sc_by_project_db(self.A_model.current_project.project_database)]
        

    def handle_current_sc_changed(self):
        self.A_model.shots = [Shot.model_validate(data) for data in cgt.get_shot_by_project_db(self.A_model.current_project.project_database)]
        

    def handle_current_shot_changed(self):
        self.get_task("handle_current_shot_changed")

    def handle_mytask_changed(self):
        """我的任务获取的是根据当前的任务类型决定的，如果是镜头，就是镜头任务，如果是场，就是场任务，但是
        镜头任务获取出来的包括集。场信息，需要去更新集、场数据"""
        self.get_task("handle_mytask_changed")



    # ==其他功能==
    def update_project_settings_info(self):
        """Update project settings information"""
        settings_info = [
            f'<span class="info-title">项目:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_full_name}</span>',
            f'<span class="info-title">分辨率:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_resolution}</span>',
            f'<span class="info-title">帧率:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_frame_rate}</span>',
            # f'<span class="info-title">项目状态:</span>'
            # f'<span class="info-desc">{i["project.status"]}</span>',
            f'<span class="info-title">maya版本:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_maya_version or "未设置,使用默认2020"}</span>',
            f'<span class="info-title">UE版本:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_ue_version}</span>',
            f'<span class="info-title">阿诺德版本:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_arnold_version}</span>',
            f'<span class="info-title">特效Houdini版本:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_vfx_houdini_version}</span>',
            f'<span class="info-title">解算Houdini版本:</span>'
            f'<span class="info-desc">{self.A_model.current_project.project_cfx_houdini_version}</span>'
        ]
        if not settings_info:
            html = f"{self.A_view.info_html_style}<div class='info-root'>无项目信息</div>"
        else:
            html = self.A_view.info_html_style + "<div class='info-root'>" + ("&nbsp;"*10).join(settings_info) + "</div>"
        self.A_view.textBrowser_proj_settings_info.setHtml(html)

    def update_comboBox_without_next_signal(self, combobox, items):
        '''更新combobox的值不触发信号，并在更新后恢复原来的选中值'''
        Yprint(f"{combobox.objectName()}初始的选项数量是:{combobox.count()},当前选中的值是: {combobox.currentText()}")
        
        combobox.blockSignals(True)
        combobox.clear()
        combobox.addItems(items)#sorted(items)
        
        # 检查原来的值是否存在于新的选项列表中
        if combobox.currentText() in items:
            index = combobox.findText(combobox.currentText())
        else:
            index = 0
        
        combobox.setCurrentIndex(index)
        combobox.blockSignals(False)
        Yprint(f"{combobox.objectName()}更新后的选项数量是:{combobox.count()},更新后选中的值是: {combobox.currentText()}")


    def get_task(self,obj):
        print("get_task","-"*30,"from","-"*10,obj)
        Yprint(self.A_model.current_project)
        Yprint(self.A_model.current_stage)
        Yprint(self.A_model.current_eps)
        Yprint(self.A_model.current_sc)
        Yprint(self.A_model.current_shot)
        Yprint(self.A_model.mytask)
        