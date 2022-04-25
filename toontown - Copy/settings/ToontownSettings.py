from direct.directnotify import DirectNotifyGlobal
from panda3d.core import loadPrcFileData
from otp.otpbase.Settings import Settings

class ToontownSettings:
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownSettings')

    def __init__(self):
        self.settings = Settings()
        self.loadFromSettings()

    def loadFromSettings(self):
        electionEvent = self.settings.getBool('game', 'elections', False)
        loadPrcFileData('toonBase Settings Election', 'want-doomsday %s' % electionEvent)
        self.settings.updateSetting('game', 'elections', electionEvent)
        smoothAnimations = self.settings.getBool('game', 'smoothanimations', False)
        loadPrcFileData('toonBase Settings Smooth Animations', 'want-smooth-animations %s' % smoothAnimations)
        self.settings.updateSetting('game', 'smoothanimations', smoothAnimations)
        newTTR = self.settings.getBool('game', 'new-ttrloader', False)
        loadPrcFileData('toonBase Settings Original TTR Start', 'want-new-ttrloader %s' % newTTR)
        self.settings.updateSetting('game', 'new-ttrloader', newTTR)