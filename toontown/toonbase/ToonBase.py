from otp.otpbase import OTPBase
from otp.otpbase import OTPLauncherGlobals
from otp.otpbase import OTPGlobals
from direct.showbase.PythonUtil import *
from . import ToontownGlobals
from direct.directnotify import DirectNotifyGlobal
from . import ToontownLoader
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.showbase.Transitions import Transitions
from panda3d.core import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from otp.nametag.ChatBalloon import ChatBalloon
from otp.nametag import NametagGlobals
from otp.margins.MarginManager import MarginManager
import sys
import os
import math
import tempfile
import shutil
import atexit
from toontown.toonbase import ToontownAccess
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownBattleGlobals
from toontown.launcher import ToontownDownloadWatcher
from toontown.toontowngui import TTDialog
from sys import platform
from .DisplayOptions import DisplayOptions
import otp.ai.DiagnosticMagicWords
import time
from panda3d.core import TrueClock

class ToonBase(OTPBase.OTPBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToonBase')

    def __init__(self):
        self.display = DisplayOptions()
        OTPBase.OTPBase.__init__(self)
        base.enableMusic(self.display.settings.getBool('game', 'music', True))
        base.enableSoundEffects(self.display.settings.getBool('game', 'sfx', True))
        self.disableShowbaseMouse()
        self.addCullBins()
        base.debugRunningMultiplier /= OTPGlobals.ToonSpeedFactor
        self.toonChatSounds = self.config.ConfigVariableBool('toon-chat-sounds', 1).getValue()
        self.placeBeforeObjects = config.ConfigVariableBool('place-before-objects', 1).getValue()
        self.endlessQuietZone = False
        self.wantDynamicShadows = 0
        self.exitErrorCode = 0
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        self.camLens.setMinFov(ToontownGlobals.DefaultCameraFov/(4./3.))
        self.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        self.cam2d.node().setCameraMask(BitMask32.bit(1))
        self.musicManager.setVolume(0.65)
        self.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        tpm = TextPropertiesManager.getGlobalPtr()
        candidateActive = TextProperties()
        candidateActive.setTextColor(0, 0, 1, 1)
        tpm.setProperties('candidate_active', candidateActive)
        candidateInactive = TextProperties()
        candidateInactive.setTextColor(0.3, 0.3, 0.7, 1)
        tpm.setProperties('candidate_inactive', candidateInactive)
        self.transitions.IrisModelName = 'phase_3/models/misc/iris'
        self.transitions.FadeModelName = 'phase_3/models/misc/fade'
        self.snapshotSfx = base.loader.loadSfx('phase_4/audio/sfx/Photo_shutter.ogg')
        self.flashTrack = None
        self.exitFunc = self.userExit
        if 'launcher' in __builtins__ and launcher:
            launcher.setPandaErrorCode(11)
        globalClock.setMaxDt(0.2)
        if self.config.ConfigVariableBool('want-particles', 1).getValue() == 1:
            self.notify.debug('Enabling particles')
            self.enableParticles()

        self.accept(ToontownGlobals.ScreenshotHotkey, self.takeScreenShot)

        # OS X Specific Actions
        if platform == "darwin":
            self.acceptOnce(ToontownGlobals.QuitGameHotKeyOSX, self.exitOSX)
            self.accept(ToontownGlobals.QuitGameHotKeyRepeatOSX, self.exitOSX)
            self.acceptOnce(ToontownGlobals.HideGameHotKeyOSX, self.hideGame)
            self.accept(ToontownGlobals.HideGameHotKeyRepeatOSX, self.hideGame)
            self.acceptOnce(ToontownGlobals.MinimizeGameHotKeyOSX, self.minimizeGame)
            self.accept(ToontownGlobals.MinimizeGameHotKeyRepeatOSX, self.minimizeGame)

        self.accept('f3', self.toggleGui)
        self.accept('panda3d-render-error', self.panda3dRenderError)
        oldLoader = self.loader
        self.loader = ToontownLoader.ToontownLoader(self)
        __builtins__['loader'] = self.loader
        oldLoader.destroy()
        self.accept('PandaPaused', self.disableAllAudio)
        self.accept('PandaRestarted', self.enableAllAudio)
        self.friendMode = self.config.ConfigVariableBool('switchboard-friends', 0).getValue()
        self.wantPets = self.config.ConfigVariableBool('want-pets', 1).getValue()
        self.wantBingo = self.config.ConfigVariableBool('want-fish-bingo', 1).getValue()
        self.wantKarts = self.config.ConfigVariableBool('want-karts', 1).getValue()
        self.wantNewSpecies = self.config.ConfigVariableBool('want-new-species', 0).getValue()
        self.inactivityTimeout = self.config.GetFloat('inactivity-timeout', ToontownGlobals.KeyboardTimeout)
        if self.inactivityTimeout:
            self.notify.debug('Enabling Panda timeout: %s' % self.inactivityTimeout)
            self.mouseWatcherNode.setInactivityTimeout(self.inactivityTimeout)
        self.mouseWatcherNode.setEnterPattern('mouse-enter-%r')
        self.mouseWatcherNode.setLeavePattern('mouse-leave-%r')
        self.mouseWatcherNode.setButtonDownPattern('button-down-%r')
        self.mouseWatcherNode.setButtonUpPattern('button-up-%r')
        self.randomMinigameAbort = self.config.ConfigVariableBool('random-minigame-abort', 0).getValue()
        self.randomMinigameDisconnect = self.config.ConfigVariableBool('random-minigame-disconnect', 0).getValue()
        self.randomMinigameNetworkPlugPull = self.config.ConfigVariableBool('random-minigame-netplugpull', 0).getValue()
        self.autoPlayAgain = self.config.ConfigVariableBool('auto-play-again', 0).getValue()
        self.skipMinigameReward = self.config.ConfigVariableBool('skip-minigame-reward', 0).getValue()
        self.wantMinigameDifficulty = self.config.ConfigVariableBool('want-minigame-difficulty', 0).getValue()
        self.minigameDifficulty = self.config.GetFloat('minigame-difficulty', -1.0)
        if self.minigameDifficulty == -1.0:
            del self.minigameDifficulty
        self.minigameSafezoneId = self.config.ConfigVariableInt('minigame-safezone-id', -1).getValue()
        if self.minigameSafezoneId == -1:
            del self.minigameSafezoneId
        cogdoGameSafezoneId = self.config.ConfigVariableInt('cogdo-game-safezone-id', -1).getValue()
        cogdoGameDifficulty = self.config.GetFloat('cogdo-game-difficulty', -1)
        if cogdoGameDifficulty != -1:
            self.cogdoGameDifficulty = cogdoGameDifficulty
        if cogdoGameSafezoneId != -1:
            self.cogdoGameSafezoneId = cogdoGameSafezoneId
        ToontownBattleGlobals.SkipMovie = self.config.ConfigVariableBool('skip-battle-movies', 0).getValue()
        self.creditCardUpFront = self.config.ConfigVariableInt('credit-card-up-front', -1).getValue()
        if self.creditCardUpFront == -1:
            del self.creditCardUpFront
        else:
            self.creditCardUpFront = self.creditCardUpFront != 0
        self.housingEnabled = self.config.ConfigVariableBool('want-housing', 1).getValue()
        self.cannonsEnabled = self.config.ConfigVariableBool('estate-cannons', 0).getValue()
        self.fireworksEnabled = self.config.ConfigVariableBool('estate-fireworks', 0).getValue()
        self.dayNightEnabled = self.config.ConfigVariableBool('estate-day-night', 0).getValue()
        self.cloudPlatformsEnabled = self.config.ConfigVariableBool('estate-clouds', 0).getValue()
        self.greySpacing = self.config.ConfigVariableBool('allow-greyspacing', 0).getValue()
        self.goonsEnabled = self.config.ConfigVariableBool('estate-goon', 0).getValue()
        self.restrictTrialers = self.config.ConfigVariableBool('restrict-trialers', 1).getValue()
        self.roamingTrialers = self.config.ConfigVariableBool('roaming-trialers', 1).getValue()
        self.slowQuietZone = self.config.ConfigVariableBool('slow-quiet-zone', 0).getValue()
        self.slowQuietZoneDelay = self.config.GetFloat('slow-quiet-zone-delay', 5)
        self.killInterestResponse = self.config.ConfigVariableBool('kill-interest-response', 0).getValue()
        tpMgr = TextPropertiesManager.getGlobalPtr()
        WLDisplay = TextProperties()
        WLDisplay.setSlant(0.3)
        WLEnter = TextProperties()
        WLEnter.setTextColor(1.0, 0.0, 0.0, 1)
        tpMgr.setProperties('WLDisplay', WLDisplay)
        tpMgr.setProperties('WLEnter', WLEnter)
        del tpMgr
        self.lastScreenShotTime = globalClock.getRealTime()
        self.accept('InputState-forward', self.__walking)
        self.canScreenShot = 1
        self.glitchCount = 0
        self.walking = 0
        self.oldX = max(1, base.win.getXSize())
        self.oldY = max(1, base.win.getYSize())
        self.aspectRatio = float(self.oldX) / self.oldY
        self.localAvatarStyle = None
        return

    def openMainWindow(self, *args, **kw):
        result = OTPBase.OTPBase.openMainWindow(self, *args, **kw)
        self.setCursorAndIcon()
        return result

    def windowEvent(self, win):
        OTPBase.OTPBase.windowEvent(self, win)
        if not config.ConfigVariableInt('keep-aspect-ratio', 0).getValue():
            return
        x = max(1, win.getXSize())
        y = max(1, win.getYSize())
        maxX = base.pipe.getDisplayWidth()
        maxY = base.pipe.getDisplayHeight()
        cwp = win.getProperties()
        originX = 0
        originY = 0
        if cwp.hasOrigin():
            originX = cwp.getXOrigin()
            originY = cwp.getYOrigin()
            if originX > maxX:
                originX = originX - maxX
            if originY > maxY:
                oringY = originY - maxY
        maxX -= originX
        maxY -= originY
        if math.fabs(x - self.oldX) > math.fabs(y - self.oldY):
            newY = x / self.aspectRatio
            newX = x
            if newY > maxY:
                newY = maxY
                newX = self.aspectRatio * maxY
        else:
            newX = self.aspectRatio * y
            newY = y
            if newX > maxX:
                newX = maxX
                newY = maxX / self.aspectRatio
        wp = WindowProperties()
        wp.setSize(newX, newY)
        base.win.requestProperties(wp)
        base.cam.node().getLens().setFilmSize(newX, newY)
        self.oldX = newX
        self.oldY = newY

    def setCursorAndIcon(self):
        tempdir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, tempdir)
        vfs = VirtualFileSystem.getGlobalPtr()

        searchPath = DSearchPath()
        searchPath.appendDirectory(Filename('/phase_3/etc'))

        for filename in ['toonmono.cur', 'icon.ico']:
            p3filename = Filename(filename)
            found = vfs.resolveFilename(p3filename, searchPath)
            if not found:
                return # Can't do anything past this point.

            with open(os.path.join(tempdir, filename), 'wb') as f:
                f.write(vfs.readFile(p3filename, False))

        wp = WindowProperties()
        wp.setCursorFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'toonmono.cur')))
        wp.setIconFilename(Filename.fromOsSpecific(os.path.join(tempdir, 'icon.ico')))
        self.win.requestProperties(wp)

    def addCullBins(self):
        cbm = CullBinManager.getGlobalPtr()
        cbm.addBin('ground', CullBinManager.BTUnsorted, 18)
        cbm.addBin('shadow', CullBinManager.BTBackToFront, 19)
        cbm.addBin('gui-popup', CullBinManager.BTFixed, 60)

    def disableShowbaseMouse(self):
        self.useDrive()
        self.disableMouse()
        if self.mouseInterface: self.mouseInterface.detachNode()
        if self.mouse2cam: self.mouse2cam.detachNode()

    def __walking(self, pressed):
        self.walking = pressed

    def toggleGui(self):
        if aspect2d.isHidden():
            aspect2d.show()
        else:
            aspect2d.hide()

    def takeScreenShot(self):
        if not os.path.exists(TTLocalizer.ScreenshotPath):
            os.mkdir(TTLocalizer.ScreenshotPath)
            self.notify.info('Made new directory to save screenshots.')
        namePrefix = TTLocalizer.ScreenshotPath + launcher.logPrefix + 'screenshot'
        timedif = globalClock.getRealTime() - self.lastScreenShotTime
        if self.glitchCount > 10 and self.walking:
            return
        if timedif < 1.0 and self.walking:
            self.glitchCount += 1
            return
        if not hasattr(self, 'localAvatar'):
            self.screenshot(namePrefix=namePrefix)
            self.lastScreenShotTime = globalClock.getRealTime()
            return
        if self.flashTrack and self.flashTrack.isPlaying():
            self.flashTrack.finish()
        self.transitions.noFade()
        coordOnScreen = self.config.ConfigVariableBool('screenshot-coords', 0).getValue()
        self.localAvatar.stopThisFrame = 1
        ctext = self.localAvatar.getAvPosStr()
        self.screenshotStr = ''
        messenger.send('takingScreenshot')
        if coordOnScreen:
            coordTextLabel = DirectLabel(pos=(-0.81, 0.001, -0.87), text=ctext, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
            coordTextLabel.setBin('gui-popup', 0)
            strTextLabel = None
            if len(self.screenshotStr):
                strTextLabel = DirectLabel(pos=(0.0, 0.001, 0.9), text=self.screenshotStr, text_scale=0.05, text_fg=VBase4(1.0, 1.0, 1.0, 1.0), text_bg=(0, 0, 0, 0), text_shadow=(0, 0, 0, 1), relief=None)
                strTextLabel.setBin('gui-popup', 0)
        self.graphicsEngine.renderFrame()
        self.screenshot(namePrefix=namePrefix, imageComment=ctext + ' ' + self.screenshotStr)
        self.lastScreenShotTime = globalClock.getRealTime()
        self.transitions.setFadeColor(1, 1, 1)
        self.flashTrack = Sequence(
            Func(base.playSfx, self.snapshotSfx),
            Func(self.transitions.fadeOut, 0.15),
            Wait(0.2),
            Func(self.transitions.fadeIn, 0.8),
            Wait(1.0),
            Func(self.transitions.setFadeColor, 0, 0, 0)
        )
        self.flashTrack.start()
        if coordOnScreen:
            if strTextLabel != None:
                strTextLabel.destroy()
            coordTextLabel.destroy()
        return

    def addScreenshotString(self, str):
        if len(self.screenshotStr):
            self.screenshotStr += '\n'
        self.screenshotStr += str

    def initNametagGlobals(self):
        arrow = loader.loadModel('phase_3/models/props/arrow')
        card = loader.loadModel('phase_3/models/props/panel')
        speech3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox'))
        thought3d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_thought_cutout'))
        speech2d = ChatBalloon(loader.loadModel('phase_3/models/props/chatbox_noarrow'))
        chatButtonGui = loader.loadModel('phase_3/models/gui/chat_button_gui')
        NametagGlobals.setCamera(self.cam)
        NametagGlobals.setArrowModel(arrow)
        NametagGlobals.setNametagCard(card, VBase4(-0.5, 0.5, -0.5, 0.5))
        if self.mouseWatcherNode:
            NametagGlobals.setMouseWatcher(self.mouseWatcherNode)
        NametagGlobals.setSpeechBalloon3d(speech3d)
        NametagGlobals.setThoughtBalloon3d(thought3d)
        NametagGlobals.setSpeechBalloon2d(speech2d)
        NametagGlobals.setThoughtBalloon2d(thought3d)
        NametagGlobals.setPageButton(PGButton.SReady, chatButtonGui.find('**/Horiz_Arrow_UP'))
        NametagGlobals.setPageButton(PGButton.SDepressed, chatButtonGui.find('**/Horiz_Arrow_DN'))
        NametagGlobals.setPageButton(PGButton.SRollover, chatButtonGui.find('**/Horiz_Arrow_Rllvr'))
        NametagGlobals.setQuitButton(PGButton.SReady, chatButtonGui.find('**/CloseBtn_UP'))
        NametagGlobals.setQuitButton(PGButton.SDepressed, chatButtonGui.find('**/CloseBtn_DN'))
        NametagGlobals.setQuitButton(PGButton.SRollover, chatButtonGui.find('**/CloseBtn_Rllvr'))
        rolloverSound = DirectGuiGlobals.getDefaultRolloverSound()
        if rolloverSound:
            NametagGlobals.setRolloverSound(rolloverSound)
        clickSound = DirectGuiGlobals.getDefaultClickSound()
        if clickSound:
            NametagGlobals.setClickSound(clickSound)
        NametagGlobals.setToon(self.cam)

        self.marginManager = MarginManager()
        self.margins = self.aspect2d.attachNewNode(self.marginManager, DirectGuiGlobals.MIDGROUND_SORT_INDEX + 1)
        mm = self.marginManager

        # TODO: Dynamicaly add more and reposition cells
        padding = 0.0225

        # Order: Top to bottom
        self.leftCells = [
            mm.addGridCell(0.2 + padding, -0.45, base.a2dTopLeft), # Above boarding groups
            mm.addGridCell(0.2 + padding, -0.9, base.a2dTopLeft),  # 1
            mm.addGridCell(0.2 + padding, -1.35, base.a2dTopLeft)  # Below Boarding Groups
        ]

        # Order: Left to right
        self.bottomCells = [
            mm.addGridCell(-0.87, 0.2 + padding, base.a2dBottomCenter), # To the right of the laff meter
            mm.addGridCell(-0.43, 0.2 + padding, base.a2dBottomCenter), # 1
            mm.addGridCell(0.01, 0.2 + padding, base.a2dBottomCenter),  # 2
            mm.addGridCell(0.45, 0.2 + padding, base.a2dBottomCenter),  # 3
            mm.addGridCell(0.89, 0.2 + padding, base.a2dBottomCenter)   # To the left of the shtiker book
        ]

        # Order: Bottom to top
        self.rightCells = [
            mm.addGridCell(-0.2 - padding, -1.35, base.a2dTopRight), # Above the street map
            mm.addGridCell(-0.2 - padding, -0.9, base.a2dTopRight),  # Below the friends list
            mm.addGridCell(-0.2 - padding, -0.45, base.a2dTopRight)  # Behind the friends list
        ]

    def hideFriendMargins(self):
        middleCell = self.rightCells[1]
        topCell = self.rightCells[2]

        self.setCellsAvailable([middleCell, topCell], False)

    def showFriendMargins(self):
        middleCell = self.rightCells[1]
        topCell = self.rightCells[2]

        self.setCellsAvailable([middleCell, topCell], True)

    def setCellsAvailable(self, cell_list, available):
        for cell in cell_list:
            self.marginManager.setCellAvailable(cell, available)

    def cleanupDownloadWatcher(self):
        self.downloadWatcher.cleanup()
        self.downloadWatcher = None
        return

    def startShow(self, cr, launcherServer = None):
        self.cr = cr
        if self.display.antialias:
            render.setAntialias(AntialiasAttrib.MAuto)
        base.graphicsEngine.renderFrame()
        self.downloadWatcher = ToontownDownloadWatcher.ToontownDownloadWatcher(TTLocalizer.LauncherPhaseNames)
        if launcher.isDownloadComplete():
            self.cleanupDownloadWatcher()
        else:
            self.acceptOnce('launcherAllPhasesComplete', self.cleanupDownloadWatcher)
        gameServer = config.ConfigVariableString('game-server', '').getValue()
        if gameServer:
            self.notify.info('Using game-server from Configrc: %s ' % gameServer)
        elif launcherServer:
            gameServer = launcherServer
            self.notify.info('Using gameServer from launcher: %s ' % gameServer)
        else:
            gameServer = '127.0.0.1'
        serverPort = config.ConfigVariableInt('server-port', 7198).getValue()
        serverList = []
        for name in gameServer.split(';'):
            url = URLSpec(name, 1)
            if config.ConfigVariableBool('server-force-ssl', False).getValue():
                url.setScheme('s')
            if not url.hasPort():
                url.setPort(serverPort)
            serverList.append(url)

        if len(serverList) == 1:
            failover = config.ConfigVariableString('server-failover', '').getValue()
            serverURL = serverList[0]
            for arg in failover.split():
                try:
                    port = int(arg)
                    url = URLSpec(serverURL)
                    url.setPort(port)
                except:
                    url = URLSpec(arg, 1)

                if url != serverURL:
                    serverList.append(url)

        cr.loginFSM.request('connect', [serverList])
        self.ttAccess = ToontownAccess.ToontownAccess()
        self.ttAccess.initModuleInfo()

        if config.ConfigVariableBool('want-speedhack-fix', False).getValue():
            # Start checking for speedhacks.
            self.lastSpeedhackCheck = time.time()
            self.trueClock = TrueClock.getGlobalPtr()
            self.lastTrueClockTime = self.trueClock.getLongTime()
            taskMgr.add(self.__speedhackCheckTick, 'speedhack-tick')

    def __speedhackCheckTick(self, task):
        # Compare the time elapsed for time.time() and TrueClock. If the TrueClock is more
        # than 1 second ahead, assume that it's running faster than normal.
        # If the system time is dragged backwards between 2 iterations, this might cause
        # problems (as the TrueClock would then be ahead).
        elapsed = time.time() - self.lastSpeedhackCheck
        tc_elapsed = self.trueClock.getLongTime() - self.lastTrueClockTime
        if tc_elapsed > elapsed + 1:
            # They responded too fast. This indicates that the TrueClock is running faster
            # than normal, and possibly means they sped the process up.
            self.__killSpeedHacker()
            return task.done
        # Clean! Lets wait until the next iteration...
        self.lastSpeedhackCheck = time.time()
        self.lastTrueClockTime = self.trueClock.getLongTime()
        return task.cont

    def __killSpeedHacker(self):
        # go fuck yo' self and yo' cheat engine, fuck'r.
        self.cr.bootedIndex = 128
        self.cr.bootedText = 'SERVER CONNECTION FAILURE. CLIENT HAS EXCEEDED RATE-LIMIT.'
        self.cr.stopReaderPollTask()
        self.cr.lostConnection()

    def removeGlitchMessage(self):
        self.ignore('InputState-forward')
        print('ignoring InputState-forward')

    def exitShow(self, errorCode = None):
        self.notify.info('Exiting Toontown: errorCode = %s' % errorCode)
        if errorCode:
            launcher.setPandaErrorCode(errorCode)
        else:
            launcher.setPandaErrorCode(0)
        sys.exit()

    def setExitErrorCode(self, code):
        self.exitErrorCode = code
        if os.name == 'nt':
            exitCode2exitPage = {OTPLauncherGlobals.ExitEnableChat: 'chat',
             OTPLauncherGlobals.ExitSetParentPassword: 'setparentpassword',
             OTPLauncherGlobals.ExitPurchase: 'purchase'}
            if code in exitCode2exitPage:
                launcher.setRegistry('EXIT_PAGE', exitCode2exitPage[code])

    def getExitErrorCode(self):
        return self.exitErrorCode

    def userExit(self):
        try:
            self.localAvatar.d_setAnimState('TeleportOut', 1)
        except:
            pass

        if hasattr(self, 'ttAccess'):
            self.ttAccess.delete()
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectCloseWindow)
        base.cr._userLoggingOut = False
        try:
            localAvatar
        except:
            pass
        else:
            messenger.send('clientLogout')
            self.cr.dumpAllSubShardObjects()

        self.cr.loginFSM.request('shutdown')
        self.notify.warning('Could not request shutdown; exiting anyway.')
        self.ignore(ToontownGlobals.QuitGameHotKeyOSX)
        self.ignore(ToontownGlobals.QuitGameHotKeyRepeatOSX)
        self.ignore(ToontownGlobals.HideGameHotKeyOSX)
        self.ignore(ToontownGlobals.HideGameHotKeyRepeatOSX)
        self.ignore(ToontownGlobals.MinimizeGameHotKeyOSX)
        self.ignore(ToontownGlobals.MinimizeGameHotKeyRepeatOSX)
        self.exitShow()

    def panda3dRenderError(self):
        launcher.setPandaErrorCode(14)
        if self.cr.timeManager:
            self.cr.timeManager.setDisconnectReason(ToontownGlobals.DisconnectGraphicsError)
        self.cr.sendDisconnect()
        sys.exit()

    def getShardPopLimits(self):
        return (config.ConfigVariableInt('shard-low-pop', ToontownGlobals.LOW_POP).getValue(), config.ConfigVariableInt('shard-mid-pop', ToontownGlobals.MID_POP).getValue(), config.ConfigVariableInt('shard-high-pop', ToontownGlobals.HIGH_POP).getValue())

    def playMusic(self, music, looping = 0, interrupt = 1, volume = None, time = 0.0):
        OTPBase.OTPBase.playMusic(self, music, looping, interrupt, volume, time)


    # OS X Specific Actions
    def exitOSX(self):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.OptionsPageExitConfirm, style=TTDialog.TwoChoice)
        self.confirm.show()
        self.accept('confirmDone', self.handleConfirm)

    def handleConfirm(self):
        status = self.confirm.doneStatus
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm
        if status == 'ok':
            self.userExit()

    def hideGame(self):
        # Hacky, I know, but it works
        hideCommand = """osascript -e 'tell application "System Events"
                                            set frontProcess to first process whose frontmost is true
                                            set visible of frontProcess to false
                                       end tell'"""
        os.system(hideCommand)

    def minimizeGame(self):
        wp = WindowProperties()
        wp.setMinimized(True)
        base.win.requestProperties(wp)

