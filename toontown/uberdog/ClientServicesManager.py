from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.otpbase import OTPLocalizer, OTPGlobals
from otp.margins.WhisperPopup import *
from panda3d.core import *
import hashlib
import hmac

FIXED_KEY = "wedidntbuildttrinaday,thinkaboutwhatyouredoing"

class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')

    systemMessageSfx = None
    avIdsReportedThisSession = []

    # --- LOGIN LOGIC ---
    def performLogin(self, doneEvent):
        self.doneEvent = doneEvent

        # Encode the login info
        cookie = self.cr.playToken or 'dev'
        cookie = cookie.encode('utf-8') # PY3
        
        key = config.GetString('csmud-secret', 'streetlamps') + config.GetString('server-version', 'no_version_set') + FIXED_KEY
        key = key.encode('utf-8') # PY3

        # Sign the login cookie
        digMod = hashlib.sha256 # REQUIRED NOW PY3.8
        sig = hmac.new(key, digestmod=digMod)
        sig.update(cookie)
        sig = sig.digest()

        self.notify.debug('Sending login cookie: ' .format(cookie))
        self.sendUpdate('login', [cookie, sig])

    def acceptLogin(self):
        messenger.send(self.doneEvent, [{'mode': 'success'}])


    # --- AVATARS LIST ---
    def requestAvatars(self):
        self.sendUpdate('requestAvatars')

    def setAvatars(self, avatars):
        avList = []
        for avNum, avName, avDNA, avPosition, nameState in avatars:
            nameOpen = int(nameState == 1)
            names = [avName, '', '', '']
            if nameState == 2: # PENDING
                names[1] = avName
            elif nameState == 3: # APPROVED
                names[2] = avName
            elif nameState == 4: # REJECTED
                names[3] = avName
            avList.append(PotentialAvatar(avNum, names, avDNA, avPosition, nameOpen))

        self.cr.handleAvatarsList(avList)

    # --- AVATAR CREATION/DELETION ---
    def sendCreateAvatar(self, avDNA, _, index):
        self.sendUpdate('createAvatar', [avDNA.makeNetString(), index])

    def createAvatarResp(self, avId):
        messenger.send('nameShopCreateAvatarDone', [avId])

    def sendDeleteAvatar(self, avId):
        self.sendUpdate('deleteAvatar', [avId])

    # No deleteAvatarResp; it just sends a setAvatars when the deed is done.

    # --- AVATAR NAMING ---
    def sendSetNameTyped(self, avId, name, callback):
        self._callback = callback
        self.sendUpdate('setNameTyped', [avId, name])

    def setNameTypedResp(self, avId, status):
        self._callback(avId, status)

    def sendSetNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4, callback):
        self._callback = callback
        self.sendUpdate('setNamePattern', [avId, p1, f1, p2, f2, p3, f3, p4, f4])

    def setNamePatternResp(self, avId, status):
        self._callback(avId, status)

    def sendAcknowledgeAvatarName(self, avId, callback):
        self._callback = callback
        self.sendUpdate('acknowledgeAvatarName', [avId])

    def acknowledgeAvatarNameResp(self):
        self._callback()

    # --- AVATAR CHOICE ---
    def sendChooseAvatar(self, avId):
        self.sendUpdate('chooseAvatar', [avId])

    # No response: instead, an OwnerView is sent or deleted.

    def systemMessage(self, code, params):
        # First, format message:
        msg = OTPLocalizer.CRSystemMessages.get(code)
        if not msg:
            self.notify.warning('Got invalid system-message code: %d' % code)
            return

        try:
            message = msg % tuple(params)
        except TypeError:
            self.notify.warning(
                'Got invalid parameters for system-message %d: %r' % (code, params))
            return

        whisper = WhisperPopup(message, OTPGlobals.getInterfaceFont(), WhisperPopup.WTSystem)
        whisper.manage(base.marginManager)
        if not self.systemMessageSfx:
            self.systemMessageSfx = base.loader.loadSfx('phase_3/audio/sfx/clock03.ogg')
        if self.systemMessageSfx:
            base.playSfx(self.systemMessageSfx)

    def hasReportedPlayer(self, avId):
        return avId in self.avIdsReportedThisSession

    def d_reportPlayer(self, avId, category):
        # Drop-in replacement for Disney's "CentralLogger" reporting object.
        if self.hasReportedPlayer(avId):
            # We've already reported this avId.
            return
        self.avIdsReportedThisSession.append(avId)
        self.sendUpdate('reportPlayer', [avId, category])
