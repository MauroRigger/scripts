import pymel.core as pm
import maya.cmds as cmds


class myPipeline_const():
    """
    Create constants function for myPipeline Tools.
    :param: Function for myPipelineTools
    """

    """
    Update reference loading latest rig and connecting to multiples animations selected.
    :param: load latest rig to update animations selected.
    :param: save files updated in path selected.
    """
    def update_reference_in_files(self, latest_rig, animation_files, folder_path, save_in):
        for animation_file in animation_files:
            cmds.file(prompt=False)
            print(f"Processing file: {animation_file.text()}")

            pm.openFile(folder_path + '/' + animation_file.text(), force=True)

            references = pm.listReferences()
            print(references)

            for ref in references:
                print(ref, references)
                try:
                    if ref.path != latest_rig:
                        print(f"Updating reference from {ref.path} to {latest_rig}")
                        ref.replaceWith(latest_rig)
                except Exception as e:
                    print(f"Error updating reference in {animation_file}: {e}")

            print(f"Path: {save_in}")
            cmds.file(rename=save_in + '/' + animation_file.text())
            cmds.file(save=True, defaultExtensions=False, type='mayaAscii')
            print(f"File saved: {save_in + '/' + animation_file.text()}")

