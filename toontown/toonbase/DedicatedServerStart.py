import sys
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from toontown.toonbase.DedicatedServer import DedicatedServer

loadPrcFileData('private config', 'window-type none')

if __debug__:
    loadPrcFile('config/dev.prc')

# Settings (settings.json):
from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

ShowBase()
dedicatedServer = DedicatedServer(localServer=False)
dedicatedServer.start()
base.run()
