import pymel.core as pm
from PySide2.QtCore import QFile, Qt
from PySide2 import QtWidgets, QtUiTools

class myPipeline_batch_fbx():

    """
    Functions for myPipelineTools -> Batch FBX tool.
    """

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
