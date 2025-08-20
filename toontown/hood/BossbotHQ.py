from . import CogHood
from toontown.toonbase import ToontownGlobals
from toontown.coghq import BossbotCogHQLoader
from toontown.hood import ZoneUtil
from panda3d.core import *
from direct.interval.LerpInterval import LerpHprInterval

class BossbotHQ(CogHood.CogHood):

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        CogHood.CogHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.BossbotHQ
        self.cogHQLoaderClass = BossbotCogHQLoader.BossbotCogHQLoader
        self.storageDNAFile = None
        self.skyFile = 'phase_12/models/bossbotHQ/ttr_m_bossbothq_sky'
        self.titleColor = (0.5, 0.5, 0.5, 1.0)
        self.whiteFogColor = Vec4(0.15, 0.15, 0.15, 1)
        self.skyLerp = None

    def load(self):
        CogHood.CogHood.load(self)
        self.sky.setScale(1.0)
        self.parentFSM.getStateNamed('BossbotHQ').addChild(self.fsm)
        self.fog = Fog('BBHQFog')

    def unload(self):
        self.parentFSM.getStateNamed('BossbotHQ').removeChild(self.fsm)
        del self.cogHQLoaderClass
        CogHood.CogHood.unload(self)
        self.fog = None

    def enter(self, *args):
        CogHood.CogHood.enter(self, *args)
        localAvatar.setCameraFov(ToontownGlobals.CogHQCameraFov)
        base.camLens.setNearFar(ToontownGlobals.BossbotHQCameraNear, ToontownGlobals.BossbotHQCameraFar)

    def exit(self):
        localAvatar.setCameraFov(ToontownGlobals.DefaultCameraFov)
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        CogHood.CogHood.exit(self)

    def spawnTitleText(self, zoneId, floorNum = None):
        if ZoneUtil.isMintInteriorZone(zoneId):
            text = '%s\n%s' % (ToontownGlobals.StreetNames[zoneId][-1], TTLocalizer.MintFloorTitle % (floorNum + 1))
            self.doSpawnTitleText(text)
        else:
            CogHood.CogHood.spawnTitleText(self, zoneId)

    def startSky(self):
        CogHood.CogHood.startSky(self)
        self.skyLerp = LerpHprInterval(self.sky.find('**/MiddleGroup'), 200, (0, 0, 0), (0, 0, 360))
        self.skyLerp.loop()

    def stopSky(self):
        self.skyLerp.finish()
        self.skyLerp = None
        CogHood.CogHood.stopSky(self)

    def setWhiteFog(self):
        if base.wantFog:
            self.fog.setColor(self.whiteFogColor)
            self.fog.setLinearRange(30.0, 800.0)
            render.clearFog()
            render.setFog(self.fog)
            self.sky.clearFog()
            self.sky.setFogOff()

    def setNoFog(self):
        if base.wantFog:
            render.clearFog()
            self.sky.clearFog()
