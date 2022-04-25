from panda3d.core import ConfigVariableBool

if ConfigVariableBool('want-new-ttrloader', False):
    from . import ToontownStartNEW
else:
    from . import ToontownStartOLD