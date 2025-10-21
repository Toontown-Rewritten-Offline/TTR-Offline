from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import OnscreenText, DGG, DirectButton, DirectFrame
from direct.interval.IntervalGlobal import LerpHprInterval
from panda3d.core import Vec3

from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.toontowngui import TTDialog

class PrizeItem(DirectObject):
    def __init__(self):
        super().__init__()
        self.panelOrigin = None
        self.name = None
        self.amount = None
        self.price = None

    def purchaseItem(self):
        self.verify = TTDialog.TTGlobalDialog(
            doneEvent='verifyDone',
            message=TTLocalizer.ToonfestVerifyPurchase % {
                "item": self.name, "price": self.price
            },
            style=TTDialog.TwoChoice
        )

        self.verify.show()
        self.accept('verifyDone', self.verifyPurchase)

    def sendConfirmation(self):
        self.ignore("prizeItemPurchased")
        messenger.send("purchaseConfirmation")

    def isEligibleToPurchase(self):
        return base.localAvatar.getTokens() < self.price

    def createItemPanelImage(self, itemTypeModel=None):
        self.itemPanelFrame = DirectFrame(
            parent=self.panelOrigin,
            frameSize=(-1.0, 1.0, -1.0, 1.0),
            relief=None
        )

        self.itemPanelFrame.setScale(0.15)

        if itemTypeModel:
            model = itemTypeModel
            model.setDepthTest(1)
            model.setDepthWrite(1)
            pitch = self.itemPanelFrame.attachNewNode('pitch')
            rotate = pitch.attachNewNode('rotate')
            scale = rotate.attachNewNode('scale')
            model.reparentTo(scale)
            bMin, bMax = model.getTightBounds()
            center = (bMin + bMax) / 2.0
            model.setPos(-center[0], -center[1], -center[2])
            pitch.setP(20)
            bMin, bMax = pitch.getTightBounds()
            center = (bMin + bMax) / 2.0
            corner = Vec3(bMax - center)
            scale.setScale(1.0 / max(corner[0], corner[1], corner[2]))
            pitch.setY(2)
            rotateLerp = LerpHprInterval(model, 10, hpr=(360, 10, 0), startHpr=(0, 10, 0))
            rotateLerp.loop()

    def verifyPurchase(self):
        pass

    def updateBuyButton(self):
        pass

    def createItemPanel(self):
        pass
