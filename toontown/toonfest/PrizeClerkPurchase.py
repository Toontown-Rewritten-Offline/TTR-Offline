from .TokenPurchaseBase import *
from . import PrizeScreen
#from toontown.toonbase import ToontownTimer
COUNT_UP_RATE = 0.15
DELAY_BEFORE_COUNT_UP = 1.25
DELAY_AFTER_COUNT_UP = 1.75
COUNT_DOWN_RATE = 0.075
DELAY_AFTER_COUNT_DOWN = 0.0
DELAY_AFTER_CELEBRATE = 3.0

class PrizeClerkPurchase(TokenPurchaseBase):
    activateMode = 'storePurchase'

    def __init__(self, toon, remain, doneEvent):
        TokenPurchaseBase.__init__(self, toon, doneEvent)
        self.remain = remain
        self.guiDoneEvent = 'phoneGuiDone'

    def load(self):
        self.tokenGUI = loader.loadModel('phase_6/models/gui/ttr_m_tf_gui_PrizePanel')
        TokenPurchaseBase.load(self, self.tokenGUI)
        self.phoneGui = PrizeScreen.PrizeScreen(phone=self, doneEvent=self.guiDoneEvent, prizes=True)
        self.phoneGui.show()
        self.accept(self.guiDoneEvent, self.__handleExitPanel)
        self.pageIndex = 0

        #prizePanelMain = self.tokenGUI.find('**/prizePanelMain')
        #self.prizePanel = DirectFrame(relief=None, image=prizePanelMain, pos=(-0.5, 0, 0))
        #self.prizePanel.hide()

        #self.cancelIcon = self.tokenGUI.find('**/cancelIcon')
        #self.cancelPressed = self.tokenGUI.find('**/cancelIcon_pressed')
        #self.cancelRollover = self.tokenGUI.find('**/cancelIcon_rollover')
        #self.cancelButton = DirectButton(parent=self.prizePanel, image=(self.cancelIcon,
        # self.cancelPressed,
        # self.cancelRollover), relief=None, command=self.__handleExitPanel)

        #self.leftArrow = self.tokenGUI.find('**/arrowLeft')
        #self.leftArrowPressed = self.tokenGUI.find('**/arrowLeft_pressed')
        #self.leftArrowRollover = self.tokenGUI.find('**/arrowLeft_rollover')
        #self.leftArrowFlat = self.tokenGUI.find('**/arrowLeft_inactive')
        #self.leftArrowButton = DirectButton(parent=self.prizePanel, image=(self.leftArrow,
        # self.leftArrowPressed,
        # self.leftArrowRollover,
        # self.leftArrowFlat), state=DGG.DISABLED, relief=None, command=self.showBackPage)

        #self.rightArrow = self.tokenGUI.find('**/arrowRight')
        #self.rightArrowPressed = self.tokenGUI.find('**/arrowRight_pressed')
        #self.rightArrowRollover = self.tokenGUI.find('**/arrowRight_rollover')
        #self.rightArrowFlat = self.tokenGUI.find('**/arrowRight_inactive')
        #self.rightArrowButton = DirectButton(parent=self.prizePanel, image=(self.rightArrow,
        # self.rightArrowPressed,
        # self.rightArrowRollover,
        # self.rightArrowFlat), relief=None, command=self.showNextPage)

        #self.timer = ToontownTimer.ToontownTimer()
        #self.timer.reparentTo(self.frame)
        #self.timer.posInTopRightCorner()
        self.tokenGUI.removeNode()
        return

    def unload(self):
        #self.timer.destroy()
        TokenPurchaseBase.unload(self)
        #del self.timer
        #del self.cancelButton
        #del self.prizePanel

    def showNextPage(self):
        taskMgr.remove('clarabelleHelpText1')
        messenger.send('wakeup')
        self.pageIndex = self.pageIndex + 1
        if self.pageIndex == 2:
            self.rightArrowButton['state'] = DGG.DISABLED
        self.leftArrowButton['state'] = DGG.NORMAL
        #self.showPageItems()
        return

    def showBackPage(self):
        taskMgr.remove('clarabelleHelpText1')
        messenger.send('wakeup')
        self.pageIndex = self.pageIndex - 1
        if self.pageIndex == 0:
            self.leftArrowButton['state'] = DGG.DISABLED
        elif self.pageIndex == 1:
            self.rightArrowButton['state'] = DGG.NORMAL
        #self.showPageItems()

    def showPageItems(self):
        self.hidePages()
        if self.pageIndex < 0:
            self.closeCover()
        else:
            if self.pageIndex == 0:
                self.openCover()
            page = self.pageList[self.pageIndex]
            newOrBackOrLoyalty = 0
            page.show()
            for panel in self.panelDict[page.get_key()]:
                panel.load()
                if panel.ival:
                    panel.ival.loop()
                self.visiblePanels.append(panel)

            pIndex = 0
            randGen = random.Random()
            randGen.seed(base.localAvatar.catalogScheduleCurrentWeek + (self.pageIndex << 8) + (newOrBackOrLoyalty << 16))
            for i in range(NUM_CATALOG_ROWS):
                for j in range(NUM_CATALOG_COLS):
                    if pIndex < len(self.visiblePanels):
                        type = self.visiblePanels[pIndex]['item'].getTypeCode()
                        self.squares[i][j].setColor(list(CatalogPanelColors.values())[randGen.randint(0, len(CatalogPanelColors) - 1)])
                        cs = 0.7 + 0.3 * randGen.random()
                        self.squares[i][j].setColorScale(0.7 + 0.3 * randGen.random(), 0.7 + 0.3 * randGen.random(), 0.7 + 0.3 * randGen.random(), 1)
                    else:
                        self.squares[i][j].setColor(CatalogPanelColors[CatalogItemTypes.CHAT_ITEM])
                        self.squares[i][j].clearColorScale()
                    pIndex += 1

            self.pageLabel['text'] = text + ' - %d' % (self.pageIndex + 1)
            self.adjustForSound()
            self.update()
        return

    def __handleExitPanel(self):
        #self.prizePanel.reparentTo(hidden)
        #self.prizePanel.hide()
        self.handleDone(0)

    def __timerExpired(self):
        self.handleDone(0)

    def enterPurchase(self):
        TokenPurchaseBase.enterPurchase(self)
        self.pointDisplay.reparentTo(self.toon.inventory.storePurchaseFrame)
        self.statusLabel.reparentTo(self.toon.inventory.storePurchaseFrame)
        #self.timer.countdown(self.remain, self.__timerExpired)

    def exitPurchase(self):
        TokenPurchaseBase.exitPurchase(self)
        self.pointDisplay.reparentTo(self.frame)
        self.statusLabel.reparentTo(self.frame)
        self.ignore('purchaseStateChange')
