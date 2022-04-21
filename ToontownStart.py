from panda3d.core import ConfigVariableBool, loadPrcFile

loadPrcFile("config/dev.prc")

from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

if ConfigVariableBool('want-new-ttrloader', False):
    import toontown.toonbase.ToontownStartNEW
else:
    import toontown.toonbase.ToontownStartOLD