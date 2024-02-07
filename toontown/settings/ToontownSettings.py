from direct.directnotify import DirectNotifyGlobal
from panda3d.core import loadPrcFileData
from otp.otpbase.Settings import Settings

class ToontownSettings:
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownSettings')

    def __init__(self):
        self.settings = Settings()
        self.loadFromSettings()

    def loadFromSettings(self):
        # Extract settings from the configuration files
        mongoDB = self.settings.getBool('game', 'mongodb-client', False)
        localServerAutoStart = self.settings.getBool('game', 'auto-start-server', True)
        electionEvent = self.settings.getBool('game', 'elections', False)
        smoothAnimations = self.settings.getBool('game', 'smoothanimations', True)
        newTTR = self.settings.getBool('game', 'retro-rewritten', False)
        
        # Load settings into Panda3D's configuration system
        loadPrcFileData('toonBase Settings MongoDB', 'want-mongo-client %s' % mongoDB)
        loadPrcFileData('toonBase Auto Start Server', 'auto-start-server %s' % localServerAutoStart)
        loadPrcFileData('toonBase Settings Election', 'want-doomsday %s' % electionEvent)
        loadPrcFileData('toonBase Settings Smooth Animations', 'want-smooth-animations %s' % smoothAnimations)
        loadPrcFileData('toonBase Settings Original TTR Start', 'want-retro-rewritten %s' % newTTR)
        
        # Update the settings in the class instance
        self.settings.updateSetting('game', 'mongodb-client', mongoDB)
        self.settings.updateSetting('game', 'auto-start-server', localServerAutoStart)
        self.settings.updateSetting('game', 'elections', electionEvent)
        self.settings.updateSetting('game', 'smoothanimations', smoothAnimations)
        self.settings.updateSetting('game', 'retro-rewritten', newTTR)
