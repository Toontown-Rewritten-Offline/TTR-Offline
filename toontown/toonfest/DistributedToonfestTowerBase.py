# Embedded file name: toontown.election.DistributedToonfestTowerBase
from panda3d.core import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import OnscreenText
from direct.distributed import DistributedObject
from panda3d.core import NodePath
from toontown.toonbase import ToontownGlobals
ChangeDirectionDebounce = 1.0
ChangeDirectionTime = 1.0

class DistributedToonfestTowerBase(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.spinStartTime = 0.0
        self.rpm = 5.0
        self.degreesPerSecond1 = self.rpm / 60.0 * 360.0
        self.degreesPerSecond2 = self.rpm / 60.0 * 360.0
        self.degreesPerSecond3 = self.rpm / 60.0 * 360.0
        self.offset = 0.0
        self.oldOffset = 0.0
        self.lerpStart = 0.0
        self.lerpFinish = 1.0
        self.speedUpSequence = None
        self.slowDownSequence = None
        self.reverseSequence = None
        self.lastChangeDirection = 0.0
        self.cr.tfb = self
        return

    def generate(self):
        self.base1 = base.cr.playGame.hood.loader.base1
        self.base2 = base.cr.playGame.hood.loader.base2
        self.base3 = base.cr.playGame.hood.loader.base3
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTowerLarge, self.base1)
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTowerMed, self.base2)
        base.cr.parentMgr.registerParent(ToontownGlobals.SPToonfestTowerSmall, self.base3)
        self.accept('enterbase1_collision', self.__handleOnBase1)
        self.accept('exitbase1_collision', self.__handleOffBase1)
        self.accept('enterbase2_collision', self.__handleOnBase2)
        self.accept('exitbase2_collision', self.__handleOffBase2)
        self.accept('enterbase3_collision', self.__handleOnBase3)
        self.accept('exitbase3_collision', self.__handleOffBase3)
        self.speedUpSound = base.loader.loadSfx('phase_4/audio/sfx/MG_Tag_C.ogg')
        self.slowDownSound = base.loader.loadSfx('phase_4/audio/sfx/MG_Tag_A.ogg')
        self.changeDirectionSound = base.loader.loadSfx('phase_3/audio/sfx/clock03.ogg')
        self.__setupSpin()
        DistributedObject.DistributedObject.generate(self)

    def __setupSpin(self):
        taskMgr.add(self.__updateSpin, self.taskName('pianoSpinTask'))

    def __stopSpin(self):
        taskMgr.remove(self.taskName('pianoSpinTask'))

    def __updateSpin(self, task):
        now = globalClock.getFrameTime()
        if now > self.lerpFinish:
            offset = self.offset
        elif now > self.lerpStart:
            t = (now - self.lerpStart) / (self.lerpFinish - self.lerpStart)
            offset = self.oldOffset + t * (self.offset - self.oldOffset)
        else:
            offset = self.oldOffset
        heading1 = self.degreesPerSecond1 * (now - self.spinStartTime) + offset
        heading2 = self.degreesPerSecond2 * (now - self.spinStartTime) + offset
        heading3 = self.degreesPerSecond3 * (now - self.spinStartTime) + offset
        self.base1.setHprScale(heading1 % 360.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        self.base2.setHprScale(heading2 % 360.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        self.base3.setHprScale(heading3 % 360.0, 0.0, 0.0, 1.0, 1.0, 1.0)
        return Task.cont

    def disable(self):
        del self.base1
        del self.base2
        del self.base3
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTowerLarge)
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTowerMed)
        base.cr.parentMgr.unregisterParent(ToontownGlobals.SPToonfestTowerSmall)
        self.ignore('enterbase1_collision')
        self.ignore('exitbase1_collision')
        self.ignore('enterbase2_collision')
        self.ignore('exitbase2_collision')
        self.ignore('enterbase3_collision')
        self.ignore('exitbase3_collision')
        self.speedUpSound = None
        self.slowDownSound= None
        self.changeDirectionSound = None
        self.__stopSpin()
        DistributedObject.DistributedObject.disable(self)
        return

    def setSpeed(self, degreesPerSecond1, degreesPerSecond2, degreesPerSecond3):
        self.degreesPerSecond1 = degreesPerSecond1
        self.degreesPerSecond2 = degreesPerSecond2
        self.degreesPerSecond3 = degreesPerSecond3

    def cleanupTowerMessage(self):
        self.towerMessage.hide()
        if self.speedUpSequence:
            if self.speedUpSequence.isPlaying():
                self.speedUpSequence.finish()
        if self.slowDownSequence:
            if self.slowDownSequence.isPlaying():
                self.slowDownSequence.finish()
        if self.reverseSequence:
            if self.reverseSequence.isPlaying():
                self.reverseSequence.finish()

    def playSfxMessage(self, operation, avatarName):
        self.towerMessage = OnscreenText(parent = aspect2d, text='', font = ToontownGlobals.getMickeyFontMaximum(), fg = (0.97647059, 0.81568627, 0.13333333, 1), align=TextNode.ACenter, scale=0, pos=(0, 0.75))
        self.towerMessage.hide()
        tpMgr = TextPropertiesManager.getGlobalPtr()
        avName = TextProperties()
        avName.setTextColor(0, 0.871, 0.498, 1)
        avName.setTextScale(1.25)
        towerText = TextProperties()
        towerText.setTextColor(1, 0.906, 0.224, 1)
        towerText.setTextScale(0.95)
        tpMgr.setProperties('avName', avName)
        tpMgr.setProperties('towerText', towerText)

        def setScale(t):
            self.towerMessage['scale'] = t
        fadeOut = self.towerMessage.colorScaleInterval(0.5, Vec4(1.0, 1.0, 1.0, 0.0))

        bouncyTextMsg = Sequence(LerpFunc(setScale, duration=0.5, fromData=0, toData=0.15, blendType='easeInOut', extraArgs=[], name='bouncyTextMsg'), LerpFunc(setScale, duration=0.2, fromData=0.15, toData=0.12, blendType='easeInOut', extraArgs=[], name='bouncyTextMsg'))
        if operation == 'SpeedUp':
            self.cleanupTowerMessage()
            self.towerMessage['text'] = '\1avName\1%s\1towerText\1\nhas sped up part of the ToonFest Tower!' % avatarName
            self.towerMessage.show()
            self.speedUpSequence = Sequence(Func(self.speedUpSound.play), bouncyTextMsg, Wait(10), fadeOut, Func(self.towerMessage.hide))
            self.speedUpSequence.start()
        elif operation == 'SlowDown':
            self.cleanupTowerMessage()
            self.towerMessage['text'] = '\1avName\1%s\1towerText\1\nhas slowed down part of the ToonFest Tower!' % avatarName
            self.towerMessage.show()
            self.slowDownSequence = Sequence(Func(self.slowDownSound.play), bouncyTextMsg, Wait(10), fadeOut, Func(self.towerMessage.hide))
            self.slowDownSequence.start()
        elif operation == 'Reverse':
            self.cleanupTowerMessage()
            self.towerMessage['text'] = '\1avName\1%s\1towerText\1\nhas reversed part of the ToonFest Tower!' % avatarName
            self.towerMessage.show()
            self.reverseSequence = Sequence(Func(self.changeDirectionSound.play), bouncyTextMsg, Wait(10), fadeOut, Func(self.towerMessage.hide))
            self.reverseSequence.start()

    def playSpeedUp(self, avId, base):
        if avId != base.localAvatar.doId:
            pass

    def playChangeDirection(self, avId):
        if avId != base.localAvatar.doId:
            pass

    def __handleOnBase1(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('OnBase1')
        self.sendUpdate('requestSpeedUp', [])

    def __handleOffBase1(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('off')

    def __handleOnBase2(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('OnBase2')
        self.sendUpdate('requestSpeedUp', [])

    def __handleOffBase2(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('off')

    def __handleOnBase3(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('OnBase3')
        self.sendUpdate('requestSpeedUp', [])

    def __handleOffBase3(self, collEntry):
        self.cr.playGame.getPlace().towerFsm.request('off')

    def __handleSpeedUpButton(self, collEntry):
        self.sendUpdate('requestSpeedUp', [])

    def __handleChangeDirectionButton(self, collEntry):
        now = globalClock.getFrameTime()
        if now - self.lastChangeDirection < ChangeDirectionDebounce:
            return
        self.lastChangeDirection = now
        self.sendUpdate('requestChangeDirection', [])