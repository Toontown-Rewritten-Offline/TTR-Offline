from panda3d.core import ConfigVariableBool

if ConfigVariableBool('want-retro-rewritten', False):
    from . import ToontownStartOLD
else:
    from . import ToontownStartNEW