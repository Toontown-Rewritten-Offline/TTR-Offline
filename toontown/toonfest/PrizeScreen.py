from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal

class PrizeScreen(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PrizeScreen')

    def __init__(self, parent = aspect2d, prizes=False, **kw):
        return
