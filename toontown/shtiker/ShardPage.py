from panda3d.core import *
from . import ShtikerPage
from direct.task.Task import Task
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.distributed import ToontownDistrictStats
from toontown.toontowngui import TTDialog
from otp.ai.MagicWordGlobal import *
POP_COLORS_NTT = (Vec4(0.0, 1.0, 0.0, 1.0), Vec4(1.0, 1.0, 0.0, 1.0), Vec4(1.0, 0.0, 0.0, 1.0))
POP_COLORS = (Vec4(0.4, 0.4, 1.0, 1.0), Vec4(0.4, 1.0, 0.4, 1.0), Vec4(1.0, 0.4, 0.4, 1.0))

class ShardPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShardPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.shardButtonMap = {}
        self.shardButtons = []
        self.scrollList = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.ShardInfoUpdateInterval = 5.0
        self.lowPop, self.midPop, self.highPop = base.getShardPopLimits()
        self.showPop = config.GetBool('show-total-population', 0)
        self.noTeleport = config.GetBool('shard-page-disable', 0)
        self.adminForceReload = 0
        return

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        helpText_ycoord = 0.303
        self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, helpText_ycoord))
        self.iconModels = loader.loadModel('phase_3.5/models/gui/sos_textures')
        self.iconGeom = self.iconModels.find('**/district')
        self.icon = OnscreenGeom(parent=self, geom=self.iconGeom, pos=(0.4, 0.0, -0.065), scale=(0.38))
        self.icon.hide()
        shardPop_ycoord = 0.403 - 0.523
        totalPop_ycoord = shardPop_ycoord - -0.6375
        self.totalPopulationText = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPagePopulationTotal, text_scale=main_text_scale, text_wordwrap=15, textMayChange=1, text_fg=(0.49803922, 0.09803922, 0.09803922, 1), text_align=TextNode.ACenter, pos=(0, 0, totalPop_ycoord))
        self.totalPopulationText.show()
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293
        self.regenerateScrollList()
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))
        return

    def unload(self):
        self.gui.removeNode()
        del self.title
        self.scrollList.destroy()
        del self.scrollList
        del self.shardButtons
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.unload(self)

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for button in self.shardButtons:
                button.detachNode()

            self.scrollList.destroy()
            self.scrollList = None
        self.scrollList = DirectScrolledList(parent=self, relief=None, pos=(-0.5, 0, -0.03), incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale), incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale), decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.125), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
         self.listXorigin + self.listFrameSizeX,
         self.listZorigin,
         self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.shardButtons)
        self.scrollList.scrollTo(selectedIndex)
        return

    def askForShardInfoUpdate(self, task = None):
        ToontownDistrictStats.refresh('shardInfoUpdated')
        taskMgr.doMethodLater(self.ShardInfoUpdateInterval, self.askForShardInfoUpdate, 'ShardPageUpdateTask-doLater')
        return Task.done

    def makeShardButton(self, shardId, shardName, shardPop):
        shardButtonParent = DirectFrame()
        teleportButtonModel = loader.loadModel('phase_4/models/parties/schtickerbookHostingGUI')
        pos = teleportButtonModel.find('**/startParty_text_locator').getPos()
        self.teleportButton = DirectButton(parent=self, relief=None, geom=(teleportButtonModel.find('**/startPartyButton_up'),
         teleportButtonModel.find('**/startPartyButton_down'),
         teleportButtonModel.find('**/startPartyButton_rollover'),
         teleportButtonModel.find('**/startPartyButton_inactive')), text=TTLocalizer.ShardPageTeleportButton, pos=(-0.125, 0, -0.925), scale=1.35, text_scale=0.0335, text_pos=(0.395, 0.325), command=self.choseShard, extraArgs=[shardId])
        shardButtonL = DirectButton(parent=shardButtonParent, relief=None, text=shardName, text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0, command=self.getPopChoiceHandler(shardPop), extraArgs=[shardId, shardName, shardPop])
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        shardButtonR = DirectButton(parent=shardButtonParent, relief=None, image=button, image_scale=(0.3, 1, 0.3), image2_scale=(0.35, 1, 0.35), image_color=self.getPopColor(shardPop), pos=(0.6, 0, 0.0125), text=self.getPopText(shardPop), text_scale=0.06, text_align=TextNode.ACenter, text_pos=(-0.0125, -0.0125), text_fg=Vec4(0, 0, 0, 0), text1_fg=Vec4(0, 0, 0, 0), text2_fg=Vec4(0, 0, 0, 1), text3_fg=Vec4(0, 0, 0, 0), command=self.getPopChoiceHandler(shardPop), extraArgs=[shardId, shardName, shardPop])
        del model
        del button
        return (shardButtonParent, shardButtonR, shardButtonL)

    def selectShard(self, shardId, shardName, shardPop):
        try:
            self.districtName.hide()
            self.districtPop.hide()
        except:
            pass
        currentShardId = self.getCurrentShardId()
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        selectedShardName = shardName
        self.teleportButton['extraArgs'] = [shardId]

        pop = base.cr.activeDistrictMap[shardId].avatarCount

        self.districtPop['text'] = ('Population: %s' % str(pop))
        self.districtName = OnscreenText(parent=self, text=shardName, pos=(0.4, 0.3, 0), scale=0.1)
        self.districtName.hide()
        self.helpText.hide()
        if shardName != None:
            self.icon.show()
            self.districtName.show()
            self.districtPop.show()
        else:
            pass
        if selectedShardName == shardName:
            if shardId == currentShardId:
                self.teleportButton['state'] = DGG.DISABLED
                return
            elif shardId == ToontownGlobals.WelcomeValleyToken:
                self.teleportButton['state'] = DGG.NORMAL
                return
            elif shardId != currentShardId:
                self.teleportButton['state'] = DGG.NORMAL
        else:
            self.districtName['text'] = shardName

    def getPopColor(self, pop):
        if config.GetBool('want-lerping-pop-colors', False):
            if pop < self.midPop:
                color1 = POP_COLORS_NTT[0]
                color2 = POP_COLORS_NTT[1]
                popRange = self.midPop - self.lowPop
                pop = pop - self.lowPop
            else:
                color1 = POP_COLORS_NTT[1]
                color2 = POP_COLORS_NTT[2]
                popRange = self.highPop - self.midPop
                pop = pop - self.midPop
            popPercent = pop / float(popRange)
            if popPercent > 1:
                popPercent = 1
            newColor = color2 * popPercent + color1 * (1 - popPercent)
        elif pop <= self.lowPop:
            newColor = POP_COLORS[0]
        elif pop <= self.midPop:
            newColor = POP_COLORS[1]
        else:
            newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop):
        if pop <= self.lowPop:
            popText = TTLocalizer.ShardPageLow
        elif pop <= self.midPop:
            popText = TTLocalizer.ShardPageMed
        else:
            popText = TTLocalizer.ShardPageHigh
        return popText

    def getPopChoiceHandler(self, pop):
        #if base.cr.productName == 'JP':
        #    handler = self.choseShard
        #elif pop <= self.midPop:
        #    if self.noTeleport and not self.showPop:
        #        handler = self.shardChoiceReject
        #    else:
        #        handler = self.choseShard
        #elif self.showPop:
        #    handler = self.choseShard
        #else:
        #    handler = self.shardChoiceReject
        handler = self.selectShard
        return handler

    def getCurrentZoneId(self):
        try:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        except:
            zoneId = None

        return zoneId

    def getCurrentShardId(self):
        zoneId = self.getCurrentZoneId()
        if zoneId != None and ZoneUtil.isWelcomeValley(zoneId):
            return ToontownGlobals.WelcomeValleyToken
        else:
            return base.localAvatar.defaultShard
        return

    def updateScrollList(self):
        curShardTuples = base.cr.listActiveShards()

        def compareShardTuples(a, b):
            if a[1] < b[1]:
                return -1
            elif b[1] < a[1]:
                return 1
            else:
                return 0

        curShardTuples.sort()
        if base.cr.welcomeValleyManager:
            curShardTuples.append((ToontownGlobals.WelcomeValleyToken,
             TTLocalizer.WelcomeValley[-1],
             0,
             0))
        currentShardId = self.getCurrentShardId()
        actualShardId = base.localAvatar.defaultShard
        actualShardName = None
        anyChanges = 0
        totalPop = 0
        totalWVPop = 0
        currentMap = {}
        self.shardButtons = []
        for i in range(len(curShardTuples)):
            shardId, name, pop, WVPop = curShardTuples[i]
            if shardId == actualShardId:
                actualShardName = name
            totalPop += pop
            totalWVPop += WVPop
            currentMap[shardId] = 1
            buttonTuple = self.shardButtonMap.get(shardId)
            if buttonTuple == None or self.adminForceReload:
                buttonTuple = self.makeShardButton(shardId, name, pop)
                self.shardButtonMap[shardId] = buttonTuple
                anyChanges = 1
            elif self.showPop:
                buttonTuple[3]['text'] = ('Population: %s' % str(pop))
                buttonTuple[1]['image_color'] = self.getPopColor(pop)
                if not base.cr.productName == 'JP':
                    buttonTuple[1]['text'] = self.getPopText(pop)
                    buttonTuple[1]['command'] = self.getPopChoiceHandler(pop)
                    buttonTuple[2]['command'] = self.getPopChoiceHandler(pop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(pop)
                if not base.cr.productName == 'JP':
                    buttonTuple[1]['text'] = self.getPopText(pop)
                    buttonTuple[1]['command'] = self.getPopChoiceHandler(pop)
                    buttonTuple[2]['command'] = self.getPopChoiceHandler(pop)
            self.shardButtons.append(buttonTuple[0])
            #if shardId == currentShardId or self.book.safeMode:
            #    buttonTuple[1]['state'] = DGG.DISABLED
            #    buttonTuple[2]['state'] = DGG.DISABLED
            #else:
            #    buttonTuple[1]['state'] = DGG.NORMAL
            #    buttonTuple[2]['state'] = DGG.NORMAL

        for shardId, buttonTuple in list(self.shardButtonMap.items()):
            if shardId not in currentMap:
                buttonTuple[0].destroy()
                del self.shardButtonMap[shardId]
                anyChanges = 1

        buttonTuple = self.shardButtonMap.get(ToontownGlobals.WelcomeValleyToken)
        if buttonTuple:
            if self.showPop:
                buttonTuple[3]['text'] = ('Population: %s' % str(totalWVPop))
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(totalWVPop)
                if not base.cr.productName == 'JP':
                    buttonTuple[1]['text'] = self.getPopText(totalWVPop)
                    buttonTuple[1]['command'] = self.getPopChoiceHandler(totalWVPop)
                    buttonTuple[2]['command'] = self.getPopChoiceHandler(totalWVPop)

        if anyChanges or self.adminForceReload:
            self.regenerateScrollList()
        self.totalPopulationText['text'] = TTLocalizer.ShardPagePopulationTotal % totalPop
        helpText = TTLocalizer.ShardPageHelpIntro
        if actualShardName:
            if currentShardId == ToontownGlobals.WelcomeValleyToken:
                helpText += TTLocalizer.ShardPageHelpWelcomeValley % actualShardName
            else:
                helpText += TTLocalizer.ShardPageHelpWhere % actualShardName
        if not self.book.safeMode:
            helpText += TTLocalizer.ShardPageHelpMove
        self.helpText['text'] = helpText
        if self.adminForceReload:
            self.adminForceReload = 0
        return

    def enter(self):
        self.askForShardInfoUpdate()
        self.updateScrollList()
        self.districtPop = OnscreenText(parent=self, text=(''), pos=(0.4, 0.2, 0), scale=0.06)
        self.districtPop.hide()
        self.helpText.show()
        self.teleportButton['state'] = DGG.DISABLED
        self.icon.hide()
        try:
            self.districtName.hide()
            self.districtPop.hide()
        except:
            pass
        currentShardId = self.getCurrentShardId()
        buttonTuple = self.shardButtonMap.get(currentShardId)
        if buttonTuple:
            i = self.shardButtons.index(buttonTuple[0])
            self.scrollList.scrollTo(i, centered=1)
        ShtikerPage.ShtikerPage.enter(self)
        self.accept('shardInfoUpdated', self.updateScrollList)

    def exit(self):
        self.districtPop.hide()
        self.districtPop = None
        self.ignore('shardInfoUpdated')
        self.ignore('confirmDone')
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.exit(self)

    def shardChoiceReject(self, shardId):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.ShardPageChoiceReject, style=TTDialog.Acknowledge)
        self.confirm.show()
        self.accept('confirmDone', self.__handleConfirm)

    def __handleConfirm(self):
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm

    def choseShard(self, shardId):
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        currentShardId = self.getCurrentShardId()
        if shardId == currentShardId:
            return
        elif shardId == ToontownGlobals.WelcomeValleyToken:
            self.doneStatus = {'mode': 'teleport',
             'hood': ToontownGlobals.WelcomeValleyToken}
            messenger.send(self.doneEvent)
        elif shardId == base.localAvatar.defaultShard:
            self.doneStatus = {'mode': 'teleport',
             'hood': canonicalHoodId}
            messenger.send(self.doneEvent)
        else:
            try:
                place = base.cr.playGame.getPlace()
            except:
                try:
                    place = base.cr.playGame.hood.loader.place
                except:
                    place = base.cr.playGame.hood.place

            place.requestTeleport(canonicalHoodId, canonicalHoodId, shardId, -1)

@magicWord(category=CATEGORY_MODERATION)
def togpop():
    """
    Moderation command to toggle shard population. If toggled off, moderators can teleport in
    to full districts, regardless of their population.

    This command should NOT be abused for normal game play, as districts have a "full" status
    for a reason, and cramming more toons in to a district can cause stability issues.
    """
    base.localAvatar.shardPage.showPop = not base.localAvatar.shardPage.showPop
    base.localAvatar.shardPage.adminForceReload = 1
    base.localAvatar.shardPage.updateScrollList()
    return "District population has been %s." % ("enabled" if base.localAvatar.shardPage.showPop else "disabled")
