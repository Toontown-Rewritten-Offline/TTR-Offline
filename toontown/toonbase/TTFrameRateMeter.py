from panda3d.core import TextNode
from toontown.toonbase import ToontownGlobals
import random

class TTFrameRateMeter(TextNode):
    TEXT_COLORS = [(0, .8, .4, 1)]
    DELAY_TIME = 0.5

    def __init__(self, name='frameRateMeter'):
        TextNode.__init__(self, name)
        self.lastFrameRate = None
        self.setText("0.0 FPS")
        self.setTextColor(random.choice(self.TEXT_COLORS))
        self.setCardColor(1, 1, 1, .6)
        self.setCardAsMargin(0.5, 0.5, 0.5, 0.5)
        self.setAlign(TextNode.ARight)
        self.setFont(ToontownGlobals.getSignFont())
        self.frameRateMeter = base.a2dTopRight.attachNewNode(self)
        self.frameRateMeter.setBin("gui-popup", 10000)
        self.frameRateMeter.setScale(0.05)          
        self.frameRateMeter.setPos(-0.105, 0, -0.115)
        taskMgr.doMethodLater(self.DELAY_TIME, self.update, 'update-frame-rate')

    def update(self, task=None):
        averageFrameRate = round(globalClock.getAverageFrameRate(), 1)
        if not self.lastFrameRate == averageFrameRate:
            self.lastFrameRate = averageFrameRate
            self.setTextColor(random.choice(self.TEXT_COLORS))
            self.setText("{0} FPS".format(self.lastFrameRate))
        task.delayTime = self.DELAY_TIME
        return task.again

    def destroy(self):
        taskMgr.remove('update-frame-rate')
        self.frameRateMeter.removeNode()
        del self.frameRateMeter