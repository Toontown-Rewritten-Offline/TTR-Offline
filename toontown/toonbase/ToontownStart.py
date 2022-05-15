from panda3d.core import ConfigVariableBool

from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

if ConfigVariableBool('want-retro-rewritten', False):
    from . import ToontownStartOLD
else:
    from . import ToontownStartNEW