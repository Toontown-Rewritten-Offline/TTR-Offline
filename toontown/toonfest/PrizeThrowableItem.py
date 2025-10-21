from toontown.toonfest.PrizeItem import PrizeItem
from toontown.toonfest import PrizeGlobals
from toontown.toonbase import ToontownGlobals, TTLocalizer, ToontownBattleGlobals
from toontown.battle.BattleProps import globalPropPool

from panda3d.core import Vec4
from direct.gui.DirectGui import OnscreenText, DGG, DirectButton

class PrizeThrowableItem(PrizeItem):
    def __init__(self, panelOrigin, level, amount, price):
        super().__init__()
        self.panelOrigin = panelOrigin
        self.level = level
        self.amount = amount
        self.name = TTLocalizer.BattleGlobalAvPropStringsPlural[4][self.level]
        self.price = price

    def createItemPanel(self):
        buttonModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        upButton = buttonModels.find('**/InventoryButtonUp')
        downButton = buttonModels.find('**/InventoryButtonDown')
        rolloverButton = buttonModels.find('**/InventoryButtonRollover')

        self.itemTypeTitle = OnscreenText(
            parent=self.panelOrigin,
            text=PrizeGlobals.throwablesTitle,
            font=ToontownGlobals.getInterfaceFont(),
            fg=(0.95, 0.95, 0, 1),
            shadow=(0, 0, 0, 1),
            scale=TTLocalizer.CIPtypeLabel,
            pos=(0, 0.24)
        )
        self.itemTypeCost = OnscreenText(
            parent=self.panelOrigin,
            text=TTLocalizer.ToonfestTokenCost % self.price,
            font=ToontownGlobals.getSignFont(),
            fg=(0.95, 0.95, 0, 1),
            shadow=(0, 0, 0, 1),
            scale=TTLocalizer.CIPpriceLabel,
            pos=(0, -0.30)
        )
        self.itemTypeAmount = OnscreenText(
            parent=self.panelOrigin,
            text=TTLocalizer.ToonfestPieAmount % (
                {"amount": self.amount, "name": TTLocalizer.BattleGlobalAvPropStringsPlural[4][self.level]}
            ),
            font=ToontownGlobals.getInterfaceFont(),
            fg=(0, 0, 0, 1),
            scale=TTLocalizer.CIPamountNameLabel,
            pos=(0, -0.22)
        )

        self.itemTypeBuyButton = DirectButton(
            parent=self.panelOrigin,
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
            command=self.purchaseItem
        )

        if self.isEligibleToPurchase() or base.localAvatar.getNumPies() > 0:
            self.itemTypeBuyButton['state'] = DGG.DISABLED
        else:
            self.itemTypeBuyButton['state'] = DGG.NORMAL

        throwableName = ToontownBattleGlobals.pieNames[self.level]
        throwableModel = globalPropPool.getProp(throwableName)

        self.createItemPanelImage(throwableModel)

    def updateBuyButton(self):
        if self.isEligibleToPurchase() or base.localAvatar.getNumPies() > 0:
            self.itemTypeBuyButton['state'] = DGG.DISABLED

    def verifyPurchase(self):
        status = self.verify.doneStatus
        self.ignore('verifyDone')
        self.verify.cleanup()
        del self.verify
        self.verify = None
        if status == 'ok':
            messenger.send("tokenTakerRequestPurchase", [self.amount, self.level, self.price])
            self.accept("prizeItemPurchased", self.sendConfirmation)
        return