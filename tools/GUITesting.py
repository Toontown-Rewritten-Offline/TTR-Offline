from direct.showbase.MessengerGlobal import *
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFile
from direct.gui import DirectGuiGlobals

loadPrcFile('config/dev.prc')

'''Prepare VFS'''
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

base = MyApp()

'''Prepare GUI Globals'''
DirectGuiGlobals.setDefaultDialogGeom(base.loader.loadModel('phase_3/models/gui/dialog_box_gui'))
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultFont(base.loader.loadFont('phase_3/fonts/ImpressBT.ttf'))

base.run()