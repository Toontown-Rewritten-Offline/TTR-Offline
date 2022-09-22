from panda3d.core import *
from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal

class DistributedToonfestDayNight(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonfestDayNight')

    def __init__(self, cr):
        DistributedObject .__init__(self, cr)
        self.cr = cr
        self.nightSky = loader.loadModel("phase_8/models/props/DL_sky")
        self.nightSky.setScale(0.8)
        self.nightSky.setTransparency(1)
        self.nightSky.setBin("background", 102)
        self.daySky = loader.loadModel("phase_3.5/models/props/TT_sky")
        self.daySky.setBin("background", 100)
        self.dayCloud1 = self.daySky.find("**/cloud1")
        self.dayCloud2 = self.daySky.find("**/cloud2")
        self.dayCloud1.setBin("background", 101)
        self.dayCloud2.setBin("background", 101)
        self.dawnSky = loader.loadModel("phase_6/models/props/MM_sky")
        self.dawnSky.setScale(0.8)
        self.dawnSky.setTransparency(1)
        self.dawnSky.setBin("background", 102)

        self.pe = PolylightEffect.make()
        self.brightness = 1.25
        self.darkness = 0.8
        self.pe.setWeight(self.brightness)
        self.begin()

    def lerpDaySkyFunc(self, color):
        self.daySky.setColorScale(color, 1)

    def lerpDawnSkyFunc(self, color):
        self.dawnSky.setColorScale(color, 1)

    def lerpNightSkyFunc(self, color):
        self.nightSky.setColorScale(color, 1)

    def begin(self):
        for sky in (self.nightSky, self.daySky, self.dawnSky):
            sky.reparentTo(camera)
            sky.setZ(0.0)
            sky.setHpr(0.0, 0.0, 0.0)
            ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
            sky.node().setEffect(ce)
            sky.setDepthTest(0)
            sky.setDepthWrite(0)

        # Color scale defines
        self.dawnColor = Vec4(1,0.8,0.4,1)
        self.dayColor = Vec4(1,1,1,1)
        self.duskColor = Vec4(0.8,0.4,0.7,1)
        self.nightColor = Vec4(0.3,0.3,0.5,1)
        self.onAlpha = Vec4(1,1,1,1)
        self.offAlpha = Vec4(1,1,1,0)

        # Change this to change the day/night cycle length
        t = 30
        tSeg = 12
        self.nightSky.setColorScale(self.onAlpha)
        self.daySky.setColorScale(self.offAlpha)
        self.dawnSky.setColorScale(self.offAlpha)
        self.cr.playGame.hood.loader.geom.setColorScale(self.nightColor)
        self.dayNightCycle = Parallel(Sequence(Parallel(LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, t, self.dawnColor),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, self.dawnColor),
                                       LerpFunctionInterval(self.lerpNightSkyFunc, duration=tSeg, toData=self.offAlpha, fromData=self.onAlpha),
                                       LerpFunctionInterval(self.lerpDawnSkyFunc, duration=tSeg, toData=self.onAlpha, fromData=self.offAlpha),
                                       ),
                              Wait(tSeg),
                              Parallel(LerpFunctionInterval(self.lerpDawnSkyFunc, duration=tSeg, toData=self.offAlpha, fromData=self.onAlpha),
                                       LerpFunctionInterval(self.lerpDaySkyFunc, duration=t, toData=self.dayColor, fromData=self.offAlpha),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, self.dayColor),
                                       ),
                              Wait(tSeg),
                              Parallel(LerpFunctionInterval(self.lerpDaySkyFunc, duration=tSeg, toData=self.duskColor, fromData=self.dayColor),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, self.duskColor),
                                       ),
                              Parallel(LerpFunctionInterval(self.lerpDaySkyFunc, duration=tSeg, toData=self.offAlpha, fromData=self.duskColor),
                                       LerpFunctionInterval(self.lerpNightSkyFunc, duration=t, toData=self.onAlpha, fromData=self.offAlpha),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, self.nightColor),
                                       ),
                              Wait(tSeg),
                              ),
                     )
        self.dayNightCycle.loop()

    def unload():
        self.dayNightCycle.finish()
        del self.dayNightCycle
        self.nightSky.removeNode()
        self.daySky.removeNode()
        self.dawnSky.removeNode()
        self.dayCloud1.removeNode()
        self.dayCloud2.removeNode()
        del self.dayCloud1
        del self.dayCloud2
        del self.nightSky
        del self.daySky
        del self.dawnSky
        del self.dawnColor
        del self.dayColor
        del self.duskColor
        del self.nightColor
        del self.onAlpha
        del self.offAlpha