import sys
from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase
import DedicatedServer

loadPrcFileData('private config', 'window-type none')

loadPrcFile('config/dev')

# Settings (settings.json):
from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

ShowBase()
dedicatedServer = DedicatedServer.DedicatedServer(localServer=False)
dedicatedServer.start()
base.run()
