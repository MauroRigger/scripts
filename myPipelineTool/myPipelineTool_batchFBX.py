import pymel.core as pm
from typing import List
import maya.cmds as cmds
import os

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

    def find_root_joint(self):
        joints = pm.ls(type='joint')
        for joint in joints:
            if not pm.listRelatives(joint, parent=True):
                return joint
        return None

    def export_fbx(self, _animation_files=[], _folder_path='', _save_in=''):
        for file_path in _animation_files:
            cmds.file(prompt=False)
            pm.openFile(_folder_path + '/' + file_path.text(), force=True)
            root_joint = self.find_root_joint()
            if root_joint:
                self.bake_animation(root_joint)
                self.exportSetup(root_joint, file_path=file_path, _save_in=_save_in)
        pm.newFile(force=True)

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

    def exportSetup(self, root_joint, file_path="", _save_in='', axis="y", bake=True):
        pm.select(root_joint, hierarchy=True)
        base_name = os.path.basename(file_path.text())
        fbx_name = os.path.splitext(base_name)[0] + '.fbx'
        fbx_path = os.path.join(_save_in, fbx_name)

        pm.mel.FBXResetExport()
        pm.mel.FBXExportBakeComplexAnimation(v=bake)
        pm.mel.FBXExportIncludeChildren(v=True)  ## Include childrens of selections
        pm.mel.FBXExportInputConnections(v=False)  ## Include Input conecctions
        pm.mel.FBXExportConstraints(v=False)
        pm.mel.FBXExportUseSceneName(v=False)
        pm.mel.FBXExportInAscii(v=True)
        pm.mel.FBXExportSkins(v=True)
        pm.mel.FBXExportSmoothMesh(v=True)
        pm.mel.FBXExportSmoothingGroups(v=True)
        pm.mel.FBXExportCameras(v=False)
        pm.mel.FBXExportLights(v=False)
        pm.mel.FBXExportUpAxis('%s' % axis)
        pm.mel.FBXExportFileVersion(v='FBX201800')
        pm.mel.FBXExport(s=True, f=fbx_path)
