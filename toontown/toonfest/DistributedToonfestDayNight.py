from panda3d.core import *
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal

class DistributedToonfestDayNight(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonfestDayNight')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
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
        dawnColor = Vec4(1,0.8,0.4,1)
        dayColor = Vec4(1,1,1,1)
        duskColor = Vec4(0.8,0.4,0.7,1)
        nightColor = Vec4(0.3,0.3,0.5,1)
        onAlpha = Vec4(1,1,1,1)
        offAlpha = Vec4(1,1,1,0)

        def lerpDaySkyFunc(color):
            self.daySky.setColorScale(color, 1)

        def lerpDawnSkyFunc(color):
            self.dawnSky.setColorScale(color, 1)

        def lerpNightSkyFunc(color):
            self.nightSky.setColorScale(color, 1)

        # Change this to change the day/night cycle length
        t = 30
        tSeg = 12
        self.nightSky.setColorScale(onAlpha)
        self.daySky.setColorScale(offAlpha)
        self.dawnSky.setColorScale(offAlpha)
        self.cr.playGame.hood.loader.geom.setColorScale(nightColor)
        i = Parallel(Sequence(Parallel(LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, t, dawnColor),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, dawnColor),
                                       LerpFunctionInterval(lerpNightSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                                       LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=onAlpha, fromData=offAlpha),
                                       ),
                              Wait(tSeg),
                              Parallel(LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                                       LerpFunctionInterval(lerpDaySkyFunc, duration=t, toData=dayColor, fromData=offAlpha),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, dayColor),
                                       ),
                              Wait(tSeg),
                              Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=duskColor, fromData=dayColor),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, duskColor),
                                       ),
                              Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=offAlpha, fromData=duskColor),
                                       LerpFunctionInterval(lerpNightSkyFunc, duration=t, toData=onAlpha, fromData=offAlpha),
                                       LerpColorScaleInterval(self.cr.playGame.hood.loader.geom, tSeg, nightColor),
                                       ),
                              Wait(tSeg),
                              ),
                     )
        i.loop()

    def unload():
        del lerpNightSkyFunc
        del lerpDawnSkyFunc
        del lerpDaySkyFunc
        del nightSky
        del dawnSky
        del daySky
        del nightColor
        del dawnColor
        del dayColor