from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton, DGG, OnscreenText
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog
from direct.interval.IntervalGlobal import LerpHprInterval

class PrizeClerkPurchase(DirectObject):
    def __init__(self, doneEvent):
        self.doneEvent = doneEvent

        self.tokenGUI = loader.loadModel("phase_6/models/gui/ttr_m_tf_gui_PrizePanel")

        self.mainPanel = self.tokenGUI.find("**/prizePanelMain")
        self.prizePanel = DirectFrame(
            relief=None,
            image=self.mainPanel,
            pos=(-0.5, 0, 0)
        )

        self.tokenJarOrigin = self.tokenGUI.find("**/jar_origin")
        self.tokenJarOrigin.reparentTo(self.prizePanel)
        self.tokenJarGui = loader.loadModel('phase_6/models/gui/ttr_m_tf_gui_tokens')
        self.tokenDisplay = DirectLabel(parent=self.tokenJarOrigin, relief=None, text=str(base.localAvatar.getTokens()), text_scale=0.18, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_pos=(0, -0.1, 0), image=self.tokenJarGui.find('**/jar'), text_font=ToontownGlobals.getSignFont())
        self.tokenJarGui.removeNode()

        self.cancelIcon = self.tokenGUI.find("**/cancelIcon")
        self.cancelPressed = self.tokenGUI.find("**/cancelIcon_pressed")
        self.cancelRollover = self.tokenGUI.find("**/cancelIcon_rollover")
        self.cancelButton = DirectButton(
            parent=self.prizePanel,
            image=(
                self.cancelIcon,
                self.cancelPressed,
                self.cancelRollover
            ),
            relief=None,
            command=self.closingTime
        )

        self.leftArrow = self.tokenGUI.find("**/arrowLeft")
        self.leftArrowPressed = self.tokenGUI.find("**/arrowLeft_pressed")
        self.leftArrowRollover = self.tokenGUI.find("**/arrowLeft_rollover")
        self.leftArrowFlat = self.tokenGUI.find("**/arrowLeft_inactive")
        self.leftArrowButton = DirectButton(
            parent=self.prizePanel,
            image=(
                self.leftArrow,
                self.leftArrowPressed,
                self.leftArrowRollover,
                self.leftArrowFlat
            ),
            relief=None
        )

        self.rightArrow = self.tokenGUI.find("**/arrowRight")
        self.rightArrowPressed = self.tokenGUI.find("**/arrowRight_pressed")
        self.rightArrowRollover = self.tokenGUI.find("**/arrowRight_rollover")
        self.rightArrowFlat = self.tokenGUI.find("**/arrowRight_inactive")
        self.rightArrowButton = DirectButton(
            parent=self.prizePanel,
            image=(
                self.rightArrow,
                self.rightArrowPressed,
                self.rightArrowRollover,
                self.rightArrowFlat
            ),
            relief=None
        )

        self.createPage()

    def createPage(self):
        self.page = DirectFrame(parent=self.prizePanel)

        self.itemPanel0 = self.tokenGUI.find("**/item_panel_0")
        self.itemPanel0.reparentTo(self.prizePanel, 2)
        self.createItemPanel(self.itemPanel0, amount=100, track=4, level=4, price=25)

        self.itemPanel1 = self.tokenGUI.find("**/item_panel_1")
        self.itemPanel2 = self.tokenGUI.find("**/item_panel_2")
        self.itemPanel3 = self.tokenGUI.find("**/item_panel_3")
        self.itemPanel4 = self.tokenGUI.find("**/item_panel_4")
        self.itemPanel5 = self.tokenGUI.find("**/item_panel_5")

    def createItemPanel(self, panelOrigin, amount, track, level, price):
        buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        upButton = buttonModels.find('**/InventoryButtonUp')
        downButton = buttonModels.find('**/InventoryButtonDown')
        rolloverButton = buttonModels.find('**/InventoryButtonRollover')

        self.itemTypeTitle = OnscreenText(parent=panelOrigin, text=TTLocalizer.ToonfestPieTypeName, font=ToontownGlobals.getInterfaceFont(), fg=(0.95, 0.95, 0, 1), shadow=(0, 0, 0, 1), scale=TTLocalizer.CIPtypeLabel, pos=(0, 0.24))
        self.itemTypeCost = OnscreenText(parent=panelOrigin, text=TTLocalizer.ToonfestTokenCost % price, font=ToontownGlobals.getSignFont(), fg=(0.95, 0.95, 0, 1), shadow=(0, 0, 0, 1), scale=TTLocalizer.CIPpriceLabel, pos=(0, -0.30))
        self.itemTypeAmount = OnscreenText(parent=panelOrigin, text=TTLocalizer.ToonfestPieAmount % ({"amount": amount, "name": TTLocalizer.BattleGlobalAvPropStringsPlural[track][level]}), font=ToontownGlobals.getInterfaceFont(), fg=(0, 0, 0, 1), scale=TTLocalizer.CIPamountNameLabel, pos=(0, -0.22))

        self.itemTypeBuyButton = DirectButton(
            parent=panelOrigin,
            state=DGG.DISABLED,
            relief=None,
            pos=(0.2, 0, 0.15),
            scale=(0.7, 1, 0.8),
            text=TTLocalizer.CatalogBuyText,
            text_scale=TTLocalizer.CIPbuyButton,
            text_pos=(-0.005, -0.01),
            image=(
                upButton,
                downButton,
                rolloverButton,
                upButton
            ),
            image_color=(1.0, 0.2, 0.2, 1),
            image0_color=Vec4(1.0, 0.4, 0.4, 1),
            image3_color=Vec4(1.0, 0.4, 0.4, 0.4),
            command=self.purchaseItem,
            extraArgs=[amount, track, level, price]
        )

        if base.localAvatar.getTokens() < price or base.localAvatar.getNumPies() > 0:
            self.itemTypeBuyButton['state'] = DGG.DISABLED
        else:
            self.itemTypeBuyButton['state'] = DGG.NORMAL

        self.createItemPanelImage(panelOrigin)

    def createItemPanelImage(self, panelOrigin):
        self.itemPanelFrame = DirectFrame(parent=panelOrigin, frameSize=(-1.0, 1.0, -1.0, 1.0), relief=None)
        self.itemPanelFrame.setScale(0.15)
        self.itemTypeModel = loader.loadModel("phase_3.5/models/props/ttr_m_prp_bat_pie")

        if self.itemTypeModel:
            model = self.itemTypeModel
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
            self.rotateLerp = LerpHprInterval(model, 10, hpr=(360, 10, 0), startHpr=(0, 10, 0))
            self.rotateLerp.loop()

    def purchaseItem(self, amount, track, level, price):
        self.verify = TTDialog.TTGlobalDialog(doneEvent='verifyDone', message=(TTLocalizer.ToonfestVerifyPurchase % {"item": TTLocalizer.BattleGlobalAvPropStringsPlural[track][level], "price": price}), style=TTDialog.TwoChoice)
        self.verify.show()
        self.accept('verifyDone', self.verifyPurchase, [amount, level, price])

    def verifyPurchase(self, amount, level, price):
        status = self.verify.doneStatus
        self.ignore('verifyDone')
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if status == 'ok':
            messenger.send("tokenTakerRequestPurchase", [amount, level, price])
            self.accept("prizeItemPurchased", self.purchaseConfirmed, [price])
        return

    def purchaseConfirmed(self, price):
        self.updateBuyButton(price)
        self.updateTokenJar()

    def updateBuyButton(self, price):
        if base.localAvatar.getTokens() < price or base.localAvatar.getNumPies() > 0:
            self.itemTypeBuyButton['state'] = DGG.DISABLED

    def updateTokenJar(self):
        self.tokenDisplay.setText(str(base.localAvatar.getTokens()))

    def load(self):
        self.prizePanel.reparentTo(aspect2d)

    def unload(self):
        self.prizePanel.destroy()
        self.prizePanel = None

        self.cancelButton.destroy()
        self.cancelButton = None
        self.leftArrowButton.destroy()
        self.leftArrowButton = None
        self.rightArrowButton.destroy()
        self.rightArrowButton = None

    def closingTime(self):
        messenger.send(self.doneEvent)