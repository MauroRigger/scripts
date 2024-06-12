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
