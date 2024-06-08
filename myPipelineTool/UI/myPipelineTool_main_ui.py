import importlib
import os.path
import sys
from typing import List
from PySide2.QtCore import QFile, Qt
from PySide2 import QtWidgets, QtUiTools
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import myPipelineTool.myPipelineTool_constants as myPipe_const
importlib.reload(myPipe_const)

"""
UI path
"""
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
ui_file = os.path.join(file_dir, "", "myPipelineToolUI.ui")

def get_maya_window():
    """
    Get Maya window
    ::return: Maya window
    """
    maya_windows = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_windows), QtWidgets.QTabWidget)

class myPipelineToolUI(QtWidgets.QWidget):
    """
    Make inheritance.
    """
    def __init__(self, ui_file="",
                 title="",
                 parent=get_maya_window()):
        super(myPipelineToolUI, self).__init__(parent)
        self.setWindowFlag(Qt.Window)
        self.setWindowTitle(title)
        self.path_ui = ui_file
        self.read_ui()

    def read_ui(self):
        uifile = QFile(self.path_ui)
        uifile.open(QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.my_widget = loader.load(uifile, parentWidget=self)
        uifile.close()

class myPipelineTool_reference_updated_buttons():

    latest_rig = []

    def __int__(self, *args, **kwargs):
        super(myPipelineTool_reference_updated_buttons, self).__init__(*args, **kwargs)
        self.ma_folder_path: str = ''
        self.files_list: List[str] = ['']
        self.latest_rig: str = ''
        self.path_save_in: str = ''

    def reference_updated_buttons_pushed(self):
        self.ui = open_window()
        self.ui.pushButton_browse_latest_rig.clicked.connect(lambda: self.ref_update_get_latest_rig())
        self.ui.pushButton_browse_ma_files.clicked.connect(lambda: self.ref_update_get_ma_folder())
        self.ui.pushButton_select_all.clicked.connect(lambda: self.ref_update_select_all())
        self.ui.pushButton_clear_selection.clicked.connect(self.ui.listWidget_ma_files_loaded.clearSelection)
        self.ui.pushButton_save_in.clicked.connect(lambda: self.ref_update_save_new_maya_files())
        self.ui.pushButton_save_references_files_updated.clicked.connect(lambda: self.ref_update_save_files())

    def get_namespace(self) -> str or None:
        if self.latest_rig:
            print(self.latest_rig)
            return os.path.splitext(os.path.basename(self.latest_rig))[0]


    def ref_update_save_files(self):
        myPipe_const.myPipeline_const.update_reference_in_files(self, latest_rig=self.latest_rig,
                                                                animation_files=self.ui.listWidget_ma_files_loaded.selectedItems(),
                                                                folder_path=self.ma_folder_path,
                                                                save_in=self.path_save_in)

    def ref_update_get_latest_rig(self):
        get_fileDialog = QtWidgets.QFileDialog()
        get_fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        get_fileDialog.setNameFilter("Maya Files (*.ma *.MA)")
        get_fileDialog.setViewMode(QtWidgets.QFileDialog.Detail)
        get_fileDialog.exec_()
        rig_path = get_fileDialog.selectedFiles()[0]

        self.ui.lineEdit_path_latest_rig.setText(rig_path)
        self.latest_rig = rig_path

        namespace = self.get_namespace()
        self.ui.lineEdit_new_namespace.setText(namespace)
        print(self.latest_rig)


    def ref_update_get_ma_folder(self):
        get_fileDialog = QtWidgets.QFileDialog()
        get_fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        get_fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        get_fileDialog.setViewMode(QtWidgets.QFileDialog.Detail)
        get_fileDialog.exec_()
        self.ma_folder_path = get_fileDialog.selectedFiles()[0]
        self.ui.lineEdit_browse_ma_files.setText(self.ma_folder_path)
        files_list = os.listdir(self.ma_folder_path)
        self.files_list = [file for file in files_list if ".ma" in file.lower()]

        self.ui.listWidget_ma_files_loaded.clear()
        self.ui.listWidget_ma_files_loaded.addItems(self.files_list)
        print(self.files_list)
        print(self.ma_folder_path)

    def ref_update_select_all(self):
        for select_files in range(self.ui.listWidget_ma_files_loaded.count()):
            item = self.ui.listWidget_ma_files_loaded.item(select_files)
            item.setSelected(True)
            print(item)

    def ref_update_save_new_maya_files(self):
        get_fileDialog = QtWidgets.QFileDialog()
        get_fileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        get_fileDialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        get_fileDialog.setViewMode(QtWidgets.QFileDialog.Detail)
        get_fileDialog.exec_()

        self.path_save_in = get_fileDialog.selectedFiles()[0]
        self.ui.lineEdit_path_save_in.setText(self.path_save_in)
        print(self.path_save_in)

def open_window():
    """
    Open window function
    ::return: Open window
    """
    global window
    window = myPipelineToolUI(ui_file, title="myPipeline Tool - V1")
    window.show()
    return window.my_widget
