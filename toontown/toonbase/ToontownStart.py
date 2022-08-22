from panda3d.core import ConfigVariableBool, loadPrcFile

#if __debug__:
loadPrcFile('config/dev.prc')

from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

if ConfigVariableBool('want-retro-rewritten', False):
    from . import ToontownStartOLD
else:
    from . import ToontownStartNEW