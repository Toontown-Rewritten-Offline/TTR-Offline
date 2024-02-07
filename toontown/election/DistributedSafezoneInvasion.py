# Embedded file name: toontown.election.DistributedSafezoneInvasion
from panda3d.core import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
from otp.avatar import Emote
from toontown.toontowngui import TTDialog
import webbrowser
from . import SafezoneInvasionGlobals

class DistributedSafezoneInvasion(DistributedObject):
    deferFor = 1

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        cr.invasion = self
        self.invasionOn = False
        self.accept('localPieSplat', self.__localPieSplat)
        self.accept('enterSuitAttack', self.__localToonHit)
        self.showFloor = base.render.find('**/ShowFloor')
        self.geom = base.cr.playGame.hood.loader.geom
        self.sky = loader.loadModel(SafezoneInvasionGlobals.CogSkyFile)
        self.sky.setBin('background', 100)
        self.sky.setColor(0.3, 0.3, 0.28, 1)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        self.sky.setDepthTest(0)
        self.sky.setDepthWrite(0)
        self.sky.setFogOff()
        self.sky.setZ(-20.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        self.fadeIn = self.sky.colorScaleInterval(5.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeInOut')
        self.cogSkyBegin = LerpColorScaleInterval(self.geom, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.cogSkyBeginStage = LerpColorScaleInterval(self.showFloor, 6.0, Vec4(0.4, 0.4, 0.4, 1), blendType='easeInOut')
        self.beginSkySequence = Sequence(Func(self.fadeIn.start), Func(self.cogSkyBegin.start), Func(self.cogSkyBeginStage.start))
        self.fadeOut = self.sky.colorScaleInterval(6.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut')
        self.cogSkyEnd = LerpColorScaleInterval(self.geom, 7.0, Vec4(1, 1, 1, 1), blendType='easeInOut')
        self.cogSkyEndStage = LerpColorScaleInterval(self.showFloor, 7.0, Vec4(1, 1, 1, 1), blendType='easeInOut')
        self.endSkySequence = Sequence(Func(self.fadeOut.start), Func(self.cogSkyEnd.start), Func(self.cogSkyEndStage.start), Wait(7), Func(self.sky.removeNode))
        base.cr.playGame.hood.loader.music.stop()
        self.musicEnter = base.loader.loadMusic(SafezoneInvasionGlobals.InvasionMusicEnter)
        self.victoryMusic = base.loader.loadMusic('phase_9/audio/bgm/CogHQ_finale.ogg')

    def delete(self):
        self.cr.invasion = None
        if self.invasionOn:
            del self.fadeIn
            del self.fadeOut
            del self.cogSkyBegin
            del self.cogSkyEnd
            del self.cogSkyBeginStage
            del self.cogSkyEndStage
            del self.musicEnter
            del self.beginSkySequence
            del self.endSkySequence
        DistributedObject.delete(self)
        self.ignoreAll()
        return

    def setInvasionStarted(self, started):
        if started and not self.invasionOn:
            self.sky.reparentTo(camera)
            self.beginSkySequence.start()
            base.playMusic(self.musicEnter, looping=1, volume=1.0)
        elif not started and self.invasionOn:
            self.endInvasion()
        else:
            return
        self.invasionOn = started

    def endInvasion(self):
        self.endSkySequence.start()
        base.playMusic(self.victoryMusic, looping=0, volume=0.9)
        self.victoryIval = Sequence(Func(Emote.globalEmote.disableAll, base.localAvatar, 'dbattle, enterReward'), Func(base.localAvatar.disableAvatarControls), Func(base.localAvatar.b_setEmoteState, 6, 1.0), Wait(5.15), Func(Emote.globalEmote.releaseAll, base.localAvatar, 'dbattle, enterReward'), Func(base.localAvatar.enableAvatarControls))
        self.victoryIval.start()

    def startCogSky(self):
        self.fadeIn.start()
        self.cogSkyBegin.start()
        self.cogSkyBeginStage.start()

    def stopCogSky(self):
        if self.invasionOn:
            cogSkySequence = Sequence(Func(self.cogSkyEnd.start), Func(self.cogSkyEndStage.start), Func(self.fadeOut.start), Wait(7), Func(self.sky.removeNode))

    def stopMusic(self):
        self.musicEnter.stop()

    def showThanks(self):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=SafezoneInvasionGlobals.Thanks, style=TTDialog.Acknowledge, suppressKeys=True)
        self.confirm.show()
        self.accept('confirmDone', self.handleConfirm)

    def handleConfirm(self):
        status = self.confirm.doneStatus
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if status == 'ok':
            webbrowser.open('http://toontownrewritten.com')
            abort()

    def __localPieSplat(self, pieCode, entry):
        if pieCode == ToontownGlobals.PieCodeToon:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Toon %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_pieHitToon(doId)
        elif pieCode == ToontownGlobals.PieCodeInvasionSuit:
            avatarDoId = entry.getIntoNodePath().getNetTag('avatarDoId')
            if avatarDoId == '':
                self.notify.warning('Suit %s has no avatarDoId tag.' % repr(entry.getIntoNodePath()))
                return
            doId = int(avatarDoId)
            if doId != localAvatar.doId:
                self.d_pieHitSuit(doId)

    def __localToonHit(self, entry):
        damage = int(entry.getIntoNode().getTag('damage'))
        self.d_takeDamage(damage)

    def d_pieHitToon(self, doId):
        self.sendUpdate('pieHitToon', [doId])

    def d_pieHitSuit(self, doId):
        self.sendUpdate('pieHitSuit', [doId])

    def d_takeDamage(self, damage):
        self.sendUpdate('takeDamage', [damage])