from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton

from toontown.toonbase import ToontownGlobals
from toontown.toonfest import PrizeThrowableItem

class PrizeClerkPurchase(DirectObject):
    def __init__(self, doneEvent):
        self.doneEvent = doneEvent
        self.panels = []

    def createPage(self):
        self.page = DirectFrame(parent=self.prizePanel)

        self.accept("purchaseConfirmation", self.purchaseConfirmed)

        self.itemPanel0 = self.tokenGUI.find("**/item_panel_0")
        self.itemPanel0.reparentTo(self.prizePanel, 2)
        prizeItem0 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel0, amount=20, level=0, price=5)
        prizeItem0.createItemPanel()
        self.panels.append(prizeItem0)

        self.itemPanel1 = self.tokenGUI.find("**/item_panel_1")
        self.itemPanel1.reparentTo(self.prizePanel, 2)
        prizeItem1 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel1, amount=20, level=4, price=5)
        prizeItem1.createItemPanel()
        self.panels.append(prizeItem1)

        self.itemPanel2 = self.tokenGUI.find("**/item_panel_2")
        self.itemPanel2.reparentTo(self.prizePanel, 2)
        prizeItem2 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel2, amount=20, level=1, price=5)
        prizeItem2.createItemPanel()
        self.panels.append(prizeItem2)

        self.itemPanel3 = self.tokenGUI.find("**/item_panel_3")
        self.itemPanel3.reparentTo(self.prizePanel, 2)
        prizeItem3 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel3, amount=20, level=2, price=5)
        prizeItem3.createItemPanel()
        self.panels.append(prizeItem3)

        self.itemPanel4 = self.tokenGUI.find("**/item_panel_4")
        self.itemPanel4.reparentTo(self.prizePanel, 2)
        prizeItem4 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel4, amount=3, level=5, price=15)
        prizeItem4.createItemPanel()
        self.panels.append(prizeItem4)

        self.itemPanel5 = self.tokenGUI.find("**/item_panel_5")
        self.itemPanel5.reparentTo(self.prizePanel, 2)
        prizeItem5 = PrizeThrowableItem.PrizeThrowableItem(self.itemPanel5, amount=1, level=6, price=50)
        prizeItem5.createItemPanel()
        self.panels.append(prizeItem5)


    def purchaseConfirmed(self):
        self.updateTokenJar()
        for panel in self.panels:
            panel.updateBuyButton()

    def updateTokenJar(self):
        self.tokenDisplay.setText(str(base.localAvatar.getTokens()))

    def load(self):
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
        self.tokenDisplay = DirectLabel(
            parent=self.tokenJarOrigin,
            relief=None,
            text=str(base.localAvatar.getTokens()),
            text_scale=0.18,
            text_fg=(0.95, 0.95, 0, 1),
            text_shadow=(0, 0, 0, 1),
            text_pos=(0, -0.1, 0),
            image=self.tokenJarGui.find('**/jar'),
            text_font=ToontownGlobals.getSignFont()
        )

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

        self.prizePanel.reparentTo(aspect2d)

    def unload(self):
        self.ignore("purchaseConfirmation")

        self.tokenGUI.removeNode()
        del self.tokenGUI

        self.tokenJarGui.removeNode()
        del self.tokenJarGui

        self.tokenDisplay.destroy()
        self.tokenDisplay = None

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