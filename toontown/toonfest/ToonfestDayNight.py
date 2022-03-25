from panda3d.core import *
from direct.interval.IntervalGlobal import *

# Load up our own sky models
nightSky = loader.loadModel("phase_8/models/props/DL_sky")
nightSky.setScale(0.8)
nightSky.setTransparency(1)
nightSky.setBin("background", 102)
daySky = loader.loadModel("phase_3.5/models/props/TT_sky")
daySky.setBin("background", 100)
dayCloud1 = daySky.find("**/cloud1")
dayCloud2 = daySky.find("**/cloud2")
dayCloud1.setBin("background", 101)
dayCloud2.setBin("background", 101)
dawnSky = loader.loadModel("phase_6/models/props/MM_sky")
dawnSky.setScale(0.8)
dawnSky.setTransparency(1)
dawnSky.setBin("background", 102)

pe = PolylightEffect.make()
brightness = 1.25
darkness = 0.8
pe.setWeight(brightness)


for sky in (nightSky, daySky, dawnSky):
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
    daySky.setColorScale(color, 1)

def lerpDawnSkyFunc(color):
    dawnSky.setColorScale(color, 1)

def lerpNightSkyFunc(color):
    nightSky.setColorScale(color, 1)

def lerpLightWeightFunc(weight):
    #base.localAvatar.node().setEffect(base.localAvatar.node().getEffect(PolylightEffect.getClassType()).setWeight(weight))
    pass

# Change this to change the day/night cycle length
t = 30
tSeg = 12
nightSky.setColorScale(onAlpha)
daySky.setColorScale(offAlpha)
dawnSky.setColorScale(offAlpha)
render.setColorScale(nightColor)
i = Parallel(Sequence(Parallel(LerpColorScaleInterval(render, tSeg, dawnColor),
                               LerpFunctionInterval(lerpLightWeightFunc, duration=tSeg, toData=darkness, fromData=brightness),
                               LerpFunctionInterval(lerpNightSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                               LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=onAlpha, fromData=offAlpha),
                               ),
                      Wait(tSeg),
                      Parallel(LerpFunctionInterval(lerpDawnSkyFunc, duration=tSeg, toData=offAlpha, fromData=onAlpha),
                               LerpFunctionInterval(lerpDaySkyFunc, duration=t, toData=dayColor, fromData=offAlpha),
                               LerpColorScaleInterval(render, tSeg, dayColor),
                               ),
                      Wait(tSeg),
                      Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=duskColor, fromData=dayColor),
                               LerpColorScaleInterval(render, tSeg, duskColor),
                               LerpFunctionInterval(lerpLightWeightFunc, duration=tSeg, toData=brightness, fromData=darkness),
                               ),
                      Parallel(LerpFunctionInterval(lerpDaySkyFunc, duration=tSeg, toData=offAlpha, fromData=duskColor),
                               LerpFunctionInterval(lerpNightSkyFunc, duration=t, toData=onAlpha, fromData=offAlpha),
                               LerpColorScaleInterval(render, tSeg, nightColor),
                               ),
                      Wait(tSeg),
                      ),
             )
i.loop()

def unload():
    del lerpLightWeightFunc
    del lerpNightSkyFunc
    del lerpDawnSkyFunc
    del lerpDaySkyFunc
    del nightSky
    del dawnSky
    del daySky
    del nightColor
    del dawnColor
    del dayColor