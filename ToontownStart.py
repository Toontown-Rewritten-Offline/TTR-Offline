from panda3d.core import ConfigVariableBool, loadPrcFile

loadPrcFile("config/dev.prc")

if ConfigVariableBool('want-new-ttrloader', False):
    import toontown.toonbase.ToontownStartNEW
else:
    import toontown.toonbase.ToontownStartOLD