from panda3d.core import *
from otp.nametag.NametagConstants import *
from .DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from panda3d.core import *
from . import NPCToons
from toontown.toonfest.PrizeClerkPurchase import PrizeClerkPurchase
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task

class DistributedNPCPrizeClerk(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.purchase = None
        self.isLocalToon = 0
        self.av = None
        self.purchaseDoneEvent = 'purchaseDone'
        return

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        self.av = None
        base.localAvatar.posCamera(0, 0)
        DistributedNPCToonBase.disable(self)
        return

    def generate(self):
        DistributedNPCToonBase.generate(self)
        self.fishGuiDoneEvent = 'fishGuiDone'

    def announceGenerate(self):
        DistributedNPCToonBase.announceGenerate(self)

    def initToonState(self):
        self.setAnimState('neutral', 1.05, None, None)
        npcOrigin = self.cr.playGame.hood.loader.geom.find('**/npc_prizeclerk_origin_%s;+s' % str(int(self.posIndex) + 1))
        print('prizeclerk origin: ', npcOrigin)
        if not npcOrigin.isEmpty():
            self.reparentTo(npcOrigin)
            self.clearMat()
        else:
            self.notify.warning('announceGenerate: Could not find npc_prizeclerk_origin_' + str(self.posIndex + 1))
        return

    def getCollSphereRadius(self):
        return 1.0

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def resetClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPurchaseGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.purchase:
            self.purchase.exit()
            self.purchase.unload()
            self.purchase = None
        self.clearMat()
        self.startLookAround()
        self.detectAvatars()
        if self.isLocalToon:
            self.freeAvatar()
        return Task.done

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None
        return

    def setupAvatars(self, av):
        self.ignoreAvatars()
        av.stopLookAround()
        av.lerpLookAt(Point3(-0.5, 4, 0), time=0.5)
        self.stopLookAround()
        self.lerpLookAt(Point3(av.getPos(self)), time=0.5)

    def setMovie(self, mode, npcId, avId, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.PURCHASE_MOVIE_CLEAR:
            return
        elif mode == NPCToons.PURCHASE_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                camera.wrtReparentTo(render)
                self.cameraLerp = LerpPosQuatInterval(camera, 1, Point3(-3, 12, self.getHeight() - 0.5), Point3(-150, -2, 0), other=self, blendType='easeInOut')
                self.cameraLerp.start()
            self.setChatAbsolute(random.choice([TTLocalizer.PIEOWNER_GREETING1,
                                                TTLocalizer.PIEOWNER_GREETING2,
                                                TTLocalizer.PIEOWNER_GREETING3,
                                                TTLocalizer.PIEOWNER_GREETING4]), CFSpeech | CFTimeout)
            if self.isLocalToon:
                taskMgr.doMethodLater(1.0, self.popupPurchaseGUI, self.uniqueName('popupPurchaseGUI'))
        elif mode == NPCToons.PURCHASE_MOVIE_COMPLETE:
            self.setChatAbsolute(random.choice([TTLocalizer.PIEOWNER_GOODBYE1,
                                                TTLocalizer.PIEOWNER_GOODBYE2,
                                                TTLocalizer.PIEOWNER_GOODBYE3,
                                                TTLocalizer.PIEOWNER_GOODBYE4]), CFSpeech | CFTimeout)
            self.resetClerk()

    def popupPurchaseGUI(self, task):
        self.acceptOnce(self.purchaseDoneEvent, self.__handlePurchaseDone)
        self.purchase = PrizeClerkPurchase(self.purchaseDoneEvent)
        self.purchase.load()
        self.accept("tokenTakerRequestPurchase", self.d_requestPurchase)
        return Task.done

    def d_requestPurchase(self, amount, level, price):
        self.sendUpdate("requestPurchase", [amount, level, price])

    def itemPurchased(self):
        self.setChatAbsolute(random.choice([TTLocalizer.PIEOWNER_BOUGHT1,
                                            TTLocalizer.PIEOWNER_BOUGHT2,
                                            TTLocalizer.PIEOWNER_BOUGHT3,
                                            TTLocalizer.PIEOWNER_BOUGHT4]), CFSpeech | CFTimeout)
        messenger.send("prizeItemPurchased")

    def __handlePurchaseDone(self):
        self.purchase.unload()
        self.ignore("tokenTakerRequestPurchase")
        self.purchase = None
        self.d_setPrizes()
        return

    def d_setPrizes(self):
        self.sendUpdate('setPrizes')