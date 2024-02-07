from direct.gui.DirectGui import OnscreenGeom, OnscreenImage, OnscreenText
from direct.gui import DirectGuiGlobals
from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import LerpScaleInterval, Sequence, LerpFunc
from toontown.toonbase import ToontownGlobals
from panda3d.core import *

class NewLoadingScreen(DirectObject.DirectObject):

    def __init__(self):
        DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
        if ConfigVariableBool('want-retro-rewritten', False):
            base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        else:
            base.setBackgroundColor(Vec4(0.145, 0.368, 0.78, 1))

    def musicVolCont1(self, t):
        musPhase1.setVolume(t)
    
    def musicVolCont2(self, t):
        musPhase2.setVolume(t)

    def newMusic(self):
        base.musicManager.setConcurrentSoundLimit(2)
        global musPhase1
        global musPhase2
        musPhase1 = base.musicManager.getSound('phase_3/audio/bgm/ttr_d_theme_phase1.ogg')
        musPhase2 = base.musicManager.getSound('phase_3/audio/bgm/ttr_d_theme_phase2.ogg')
        if musPhase1:
            self.musicVolCont1(1)
            self.musicVolCont2(0)
            if not __debug__:
                musPhase1.setLoopStart(2.9)
                musPhase2.setLoopStart(2.9)
            musPhase1.setLoop(True)
            musPhase2.setLoop(True)
            musPhase1.play()
            musPhase2.play()
        base.musicManager.update()

    def musicLoadIn(self):
        phase1 = LerpFunc(self.musicVolCont1,
                    fromData=1,
                    toData=0,
                    duration=2,
                    blendType='easeIn',
                    extraArgs=[],
                    name=None)
        
        phase2 = LerpFunc(self.musicVolCont2,
                    fromData=0,
                    toData=1,
                    duration=2,
                    blendType='easeIn',
                    extraArgs=[],
                    name=None)

        phase1.start()
        phase2.start()

    def exitMusic(self):
        musPhase1.stop()
        musPhase2.stop()

    def newVersion(self):
        serverVersion = config.ConfigVariableString('server-version', 'no_version_set').getValue()
        global version
        version = OnscreenText(serverVersion, pos=(-1, -1.2), scale=0.055, font=loader.loadFont('phase_3/fonts/ImpressBT.ttf'), fg=Vec4(1, 1, 1, 1), align=TextNode.ALeft)
        version.setPos(0.12,0.045)
        version.reparentTo(base.a2dBottomLeft)
        stop = version.cleanup
        return version

    def connectBackground(self):
        global connectbg
        connectbg = OnscreenImage(image='phase_3/maps/tt_t_gui_pat_background.jpg', scale = (2, 2, 1))
        connectbg.setBin('background', 1)

    def newLogo(self):
        logobam = loader.loadModel('phase_3/models/gui/toontown-logo')
        findlogo = logobam.find('**/logo')
        global logo
        logo = OnscreenGeom(geom = findlogo, pos = (0, 0, 0.35))
        logoSeq = Sequence(
        LerpScaleInterval(logo, 3.25, Vec3(0.20625, 0.225, 0.20625), Vec3(0.1375, 0.3, 0.1375), blendType='easeInOut'),
        LerpScaleInterval(logo, 3.25, Vec3(0.1375, 0.3, 0.1375), Vec3(0.20625, 0.225, 0.20625), blendType='easeInOut')).loop()

    def cleanup(self):
        version.destroy()
        logo.destroy()
        connectbg.destroy()