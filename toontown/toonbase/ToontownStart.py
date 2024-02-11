from panda3d.core import *
import builtins
import os

if __debug__:
    loadPrcFile('config/dev.prc')

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

# Temporary Content Pack Loader (put Multifiles in "resources" folder)
import glob
for file in glob.glob('resources/*.mf'):
    mf = Multifile()
    mf.openReadWrite(Filename(file))
    names = mf.getSubfileNames()
    for name in names:
        ext = os.path.splitext(name)[1]
        if ext not in ['.jpg', '.jpeg', '.ogg', '.rgb']:
            mf.removeSubfile(name)
    vfs.mount(mf, Filename('/'), 0)

# Configure/Start Toontown Client
class game:
    name = 'toontown'
    process = 'client'

print('TTRPrivate: Ongoing project by RegDogg')
print('ToontownStart: Starting the game.')
builtins.game = game()
import time
import sys
import random
import builtins
try:
    launcher
except:
    from toontown.launcher.TTRLauncher import TTRLauncher
    launcher = TTRLauncher()
    builtins.launcher = launcher

if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = Loader()

# Settings
print('ToontownStart: loading game settings')
from toontown.settings.ToontownSettings import ToontownSettings
settings = ToontownSettings()
settings.loadFromSettings()

if ConfigVariableBool('want-retro-rewritten', False):
    # Poll for game finished
    pollingDelay = 0.5
    print('TTRPrivate: Ongoing project by RegDogg')
    print('ToontownStart: Polling for game2 to finish...')
    while not launcher.getGame2Done():
        time.sleep(pollingDelay)
    print('ToontownStart: Game2 is finished.')
    print('ToontownStart: Starting the game.')
    if launcher.isDummy():
        http = HTTPClient()
    else:
        http = launcher.http
    tempLoader = Loader()
    backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background-old'))

# Prepare GUI Font
from direct.gui import DirectGuiGlobals
print('ToontownStart: setting default font')
from . import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
from . import ToonBase
ToonBase.ToonBase()
from panda3d.core import *
if base.win == None:
    print('Unable to open window; aborting.')
    sys.exit()
from direct.gui.DirectGui import *

if not ConfigVariableBool('want-retro-rewritten', False):
    # Prepare new startup screen
    launcher.setPandaErrorCode(0)
    launcher.setPandaWindowOpen()
    ConfigVariableDouble('decompressor-step-time').setValue(0.01)
    ConfigVariableDouble('extractor-step-time').setValue(0.01)
    backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/entering-background'))
    eyes = loader.loadModel('phase_3/models/gui/toontown-logo')
    findeyes = eyes.find('**/eyes')
    backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
    backgroundNodePath.setPos(0.0, 0.0, 0.0)
    backgroundNodePath.setScale(aspect2d, VBase3(2))
    eyes = OnscreenGeom(geom = findeyes, pos = (0, 0, 0), scale = (0.25, 0.25, 0.25))
else:
    # Prepare old startup screen
    launcher.setPandaErrorCode(0)
    launcher.setPandaWindowOpen()
    ConfigVariableDouble('decompressor-step-time').setValue(0.01)
    ConfigVariableDouble('extractor-step-time').setValue(0.01)
    backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
    backgroundNodePath.setPos(0.0, 0.0, 0.0)
    backgroundNodePath.setScale(render2d, VBase3(1))
    backgroundNodePath.find('**/fg').setBin('fixed', 20)
    backgroundNodePath.find('**/bg').setBin('fixed', 10)
    base.graphicsEngine.renderFrame()

# Framerate meter for TTR Private: Change in 'dev.prc' to toggle
if ConfigVariableBool('tt-framerate', False):
    from toontown.toonbase.TTFrameRateMeter import TTFrameRateMeter
    TTFrameRateMeter()

base.graphicsEngine.renderFrame()

# Prepare GUI
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
from . import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)

# Prepare GUI Sounds
print('ToontownStart: Loading default gui sounds')
DirectGuiGlobals.setDefaultRolloverSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loader.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))

if not ConfigVariableBool('want-retro-rewritten', False):
    # Prepare Music and Server Version
    music = base.musicManager.getSound('phase_3/audio/bgm/ttr_d_theme_phase2.ogg')
    from . import ToontownLoader
    from direct.gui.DirectGui import *
    serverVersion = config.ConfigVariableString('server-version', 'no_version_set').getValue()
    print('ToontownStart: serverVersion: ', serverVersion)
    from .ToonBaseGlobal import *
    from direct.showbase.MessengerGlobal import *
    from toontown.distributed import ToontownClientRepository
    cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
    cr.music = music
    base.sfxManagerList[0].setVolume(0.2)
    base.musicManager.setVolume(0.2)
    base.initNametagGlobals()
    base.cr = cr
    loader.endBulkLoad('init')
else:
    # Prepare Music
    if base.musicManagerIsValid:
        music = base.musicManager.getSound('phase_3/audio/bgm/ttr_theme.ogg')
        if music:
            music.setLoop(1)
            music.setVolume(0.8)
            music.play()
    else:
        music = None

    # Server Version
    from . import ToontownLoader
    serverVersion = config.ConfigVariableString('server-version', 'no_version_set').getValue()
    print('ToontownStart: serverVersion: ', serverVersion)
    version = OnscreenText(serverVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
    loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE)
    from .ToonBaseGlobal import *
    from direct.showbase.MessengerGlobal import *
    from toontown.distributed import ToontownClientRepository
    cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)

    # Exiting Startup Screen
    cr.music = music
    del music
    base.initNametagGlobals()
    base.cr = cr
    loader.endBulkLoad('init')

# Prepare Friends Manager
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')

if not ConfigVariableBool('want-retro-rewritten', False):
    # Prepare for new loading screen
    if not launcher.isDummy() and not config.ConfigVariableBool('auto-start-server', False).getValue():
        base.startShow(cr, launcher.getGameServer())
    else:
        base.startShow(cr)

    time.sleep(0.5)
    backgroundNodePath.reparentTo(hidden)
    backgroundNodePath.removeNode()
    del backgroundNodePath
    del backgroundNode
    eyes.destroy()
    del eyes
    del tempLoader

    '''New Loading Screen'''
    from toontown.toontowngui import NewLoadingScreen

    loading = NewLoadingScreen.NewLoadingScreen()

    loading.newMusic()
    loading.newVersion()
    loading.connectBackground()
    loading.newLogo()

if config.ConfigVariableBool('auto-start-server', False).getValue():
    # Start DedicatedServer
    from otp.otpbase.OTPLocalizer import CRLoadingGameServices

    dialogClass = ToontownGlobals.getGlobalDialogClass()
    builtins.gameServicesDialog = dialogClass(message=CRLoadingGameServices)
    builtins.gameServicesDialog.show()

    from toontown.toonbase.DedicatedServer import DedicatedServer

    builtins.clientServer = DedicatedServer(localServer=True)
    builtins.clientServer.start()

    def localServerReady():
        builtins.gameServicesDialog.cleanup()
        del builtins.gameServicesDialog
        if not ConfigVariableBool('want-retro-rewritten', False):
            messenger.send('AllowPressKey')
        else:
            base.startShow(cr)

    base.accept('localServerReady', localServerReady)
else:
    if not ConfigVariableBool('want-retro-rewritten', False):
        messenger.send('AllowPressKey')

if ConfigVariableBool('want-retro-rewritten', False):
    backgroundNodePath.reparentTo(hidden)
    backgroundNodePath.removeNode()
    del backgroundNodePath
    del backgroundNode
    del tempLoader
    version.cleanup()
    del version

# Options Button
# from .OptionsPage import OptionsPage
# __builtins__.OptionsButton = OptionsPage()

base.loader = base.loader
builtins.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun:
    try:
        base.run()
    except SystemExit:
        raise
    except:
        import traceback
        traceback.print_exc()
