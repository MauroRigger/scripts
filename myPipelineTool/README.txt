Save myPipelineTool in:

1 - Save **myPipelineTool** folder in C:\*\Documents\maya\2022\scripts
2 - run the snipped in your python tab.

Snipped:

import importlib
import myPipelineTool.UI.myPipelineTool_main_ui as myPipelineTool_ui
importlib.reload(myPipelineTool_ui)
ui = myPipelineTool_ui.myPipelineTool_connect_buttons()
ui.buttons_pushed()


