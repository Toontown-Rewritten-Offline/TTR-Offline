from panda3d.core import ConfigVariableBool, loadPrcFile

loadPrcFile('config/dev.prc')

from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

if ConfigVariableBool('want-retro-rewritten', False):
    from toontown.toonbase import ToontownStartOLD
else:
    from toontown.toonbase import ToontownStartNEW