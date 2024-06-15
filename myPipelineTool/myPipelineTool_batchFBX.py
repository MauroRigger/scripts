import pymel.core as pm
import os
from typing import List
import maya.cmds as cmds
import maya.mel as mel
from PySide2.QtCore import QFile, Qt
from PySide2 import QtWidgets, QtUiTools

class myPipeline_batch_fbx():

    """
    Functions for myPipelineTools -> Batch FBX tool.
    """
    def __int__(self):
        self.select_files: List[str] = ['']
        self.path_save_in: str = ''

    """
    Check if FBX plugin is on.
    :param: If FBX plugin is off, will be turn on automatically
    """
    def check_fbx_plugin_on(self):
        try:
            pm.loadPlugin('fbxmaya')
        except:
            print("We can't load FBX plug-in :( !! ")

    """
    PlaybackOptions set to.
    :param: Function to connect playbackOption to spinBox qWidget 
    """
    def play_back_options_min_time(self, _min_value):
        pm.playbackOptions(minTime=_min_value)
        print(f"minTime set to -> {_min_value}")

    def play_back_options_max_time(self, _max_value):
        pm.playbackOptions(maxTime=_max_value)
        print(f"maxTime set to -> {_max_value}")

    # def export_fbx(self, _animation_files, _save_in):
    #     for file_path in _animation_files:
    #         pm.openFile(file_path, force=True)
    #         root_joint = self.select_joint_root()
    #         if root_joint:
    #             self.bake_animation(root_joint)
    #             self.export_files_selected_to_fbx(root_joint, animations_file=_animation_files, _save_in=_save_in)
    #     pm.newFile(force=True)
    #     QtWidgets.QMessageBox.information(self, 'Export Complete', 'FBX export completed successfully.')

    def select_joint_root(self):
        joints = pm.ls(type='joint')
        for joint in joints:
            if not pm.listRelatives(joint, parent=True):
                return joint
        return None

    def bake_animation(self, root_joint):
        # Bake the animation for the selected root joint hierarchy
        pm.select(root_joint, hierarchy=True)
        pm.bakeResults(
            simulation=True,
            time=(pm.playbackOptions(q=True, min=True), pm.playbackOptions(q=True, max=True)),
            sampleBy=1,
            oversamplingRate=1,
            disableImplicitControl=True,
            preserveOutsideKeys=True,
            sparseAnimCurveBake=False,
            removeBakedAttributeFromLayer=False,
            bakeOnOverrideLayer=False,
            minimizeRotation=True,
            controlPoints=False,
            shape=False
        )

    # def export_files_selected_to_fbx(self, root_joint, animations_file, _save_in):
    #     pm.select(root_joint, hierarchy=True)
    #     base_name = os.path.basename(animations_file)
    #     fbx_name = os.path.splitext(base_name)[0] + '.fbx'
    #     fbx_path = os.path.join(_save_in, fbx_name)
    #     pm.mel.FBXExport('-f', fbx_path, '-s')

    def export_files_selected_to_fbx(self, root_joint, file_path):
        pm.select(root_joint, hierarchy=True)
        base_name = os.path.basename(file_path)
        fbx_name = os.path.splitext(base_name)[0] + '.fbx'
        fbx_path = os.path.join(self.path_save_in, fbx_name)
        pm.mel.FBXExport('-f', fbx_path, '-s')

