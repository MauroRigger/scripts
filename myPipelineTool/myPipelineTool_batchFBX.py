import pymel.core as pm
from typing import List
import maya.cmds as cmds
import maya.mel as mel


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

    def export_fbx(self, _animation_files, _folder_path, _save_in):
        for file_path in _animation_files:
            cmds.file(prompt=False)
            file = pm.openFile(_folder_path + '/' + file_path.text(), force=True)
            start_frame = pm.playbackOptions(q=True, minTime=True)
            print(start_frame)
            end_frame = pm.playbackOptions(q=True, maxTime=True)
            print(end_frame)
            pm.select('*root*')
            pm.listRelatives(parent=True, type='joint')
            bake_joint = pm.ls(sl=True)
            print(bake_joint)
            pm.bakeResults(
                hierarchy="below",
                simulation=True,
                sampleBy=1,
                time=(start_frame, end_frame))
            for j in bake_joint:
                pm.delete(j, constraints=True)
            if file:
                mel.eval("FBXExportBakeComplexAnimation -v true")
                mel.eval("FBXExportBakeComplexStep -v 1")
                mel.eval("FBXExportUseSceneName -v false")
                mel.eval("FBXExportQuaternion -v euler")
                mel.eval("FBXExportShapes -v true")
                mel.eval("FBXExportSkins -v true")

                # Constraints
                mel.eval("FBXExportConstraints -v false")
                # Cameras
                mel.eval("FBXExportCameras -v false")
                # Lights
                mel.eval("FBXExportLights -v false")
                # Embed Media
                mel.eval("FBXExportEmbeddedTextures -v false")
                # Connections
                mel.eval("FBXExportInputConnections -v false")
                # Axis Conversion
                mel.eval("FBXExportUpAxis y")
            mel.eval('FBXExport -f "{0}" -s'.format(_save_in + '/' + file_path.text()))


    def bake_animation(self):
        start_frame = pm.playbackOptions(q=True, minTime=True)
        end_frame = pm.playbackOptions(q=True, maxTime=True)
        pm.bakeResults(
                       hierarchy="below",
                       simulation=True,
                       sampleBy=1,
                       time=(start_frame, end_frame))
        bake_joint = pm.listRelatives(type="joint")
        for j in bake_joint:
            pm.delete(j, constraints=True)


