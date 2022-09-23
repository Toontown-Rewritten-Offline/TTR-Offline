from enum import Enum
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from otp.otpbase import OTPLocalizer
from direct.interval.IntervalGlobal import *

FurnitureTypes = {
 100: ('phase_3.5/models/props/tart',     # Model
       None,                              # Color
       None,                              # Color Options
       5),                                # Base Price
                                          # Flags
                                          # Scale
 110: ('phase_5/models/props/fruit-pie-slice',
       None,
       None,
       5),
 120: ('phase_5/models/props/cream-pie-slice',
       None,
       None,
       5),
 130: ('phase_5.5/models/estate/birthday-cake-chan',
       None,
       None,
       15),
 140: ('phase_5.5/models/estate/wedding_cake',
       None,
       None,
       50)
}

class PrizeThrowableItem():
    sequenceNumber = 0
    pictureToon = None

    def makeNewItem(self, throwableIndex, loyaltyDays = 0):
        self.throwableIndex = throwableIndex
        self.loyaltyDays = loyaltyDays
#        CatalogItem.CatalogItem.makeNewItem(self)

    def getPurchaseLimit(self):
        return 100

    class getPieTypes(Enum):
        CUPCAKE = 0
        FRUIT_SLICE = 1
        CREAM_SLICE = 2
        CREAM_PIE = 3
        BIRTHDAY_CAKE = 4
        WEDDING_CAKE = 5

    def reachedPurchaseLimit(self, avatar):
        if self in avatar.onOrder or self in avatar.mailboxContents or self in avatar.onGiftOrder or self in avatar.awardMailboxContents or self in avatar.onAwardOrder:
            return 1
        if self.throwableIndex >= len(avatar.emoteAccess):
            return 0
        return avatar.emoteAccess[self.throwableIndex] != 0

    def getAcceptItemErrorText(self, retcode):
        if retcode == ToontownGlobals.P_ItemAvailable:
            return TTLocalizer.CatalogAcceptEmote
        return CatalogItem.CatalogItem.getAcceptItemErrorText(self, retcode)

    def saveHistory(self):
        return 1

    def getTypeName(self):
        return TTLocalizer.ThrowableTypeName

    def getName(self):
        return OTPLocalizer.ThrowableItemList[self.throwableIndex]

    def recordPurchase(self, avatar, pieType, numPies, optional):
        if self.throwableIndex < 0 or self.throwableIndex > len(avatar.emoteAccess):
            self.notify.warning('Invalid throwableItem access: %s for avatar %s' % (self.throwableIndex, avatar.doId))
            return ToontownGlobals.P_InvalidIndex
        #avatar.emoteAccess[self.throwableIndex] = 1
        avatar.b_setPieType(pieType)
        avatar.b_setNumPies(numPies)
        return ToontownGlobals.P_ItemAvailable

    def getPicture(self, avatar):
        model = self.loadModel()
        spin = 1
        flags = self.getFlags()
        if flags & FLRug:
            spin = 0
            model.setP(90)
        elif flags & FLPainting:
            spin = 0
        elif flags & FLBillboard:
            spin = 0
        model.setBin('unsorted', 0, 1)
        self.hasPicture = True
        return self.makeFrameModel(model, spin)

    def changeIval(self, volume):
        from toontown.toon import Toon
        from toontown.toon import ToonHead
        from toontown.toon import TTEmote
        from otp.avatar import Emote
        self.volume = volume
        if not hasattr(self, 'pictureToon'):
            return Sequence()
        track, duration = Emote.globalEmote.doEmote(self.pictureToon, self.throwableIndex, volume=self.volume)
        if duration == None:
            duration = 0
        name = 'emote-item-%s' % self.sequenceNumber
        PrizeThrowableItem.sequenceNumber += 1
        if track != None:
            track = Sequence(Sequence(track, duration=0), Wait(duration + 2), name=name)
        else:
            track = Sequence(Func(Emote.globalEmote.doEmote, toon, self.throwableIndex), Wait(duration + 4), name=name)
        return track

    def cleanupPicture(self):
        self.hasPicture = False
        self.pictureToon.emote.finish()
        self.pictureToon.emote = None
        self.pictureToon.delete()
        self.pictureToon = None
        return

    def output(self, store = -1):
        return 'PrizeThrowableItem(%s%s)' % (self.throwableIndex, self.formatOptionalData(store))

    def compareTo(self, other):
        return self.throwableIndex - other.throwableIndex

    def getHashContents(self):
        return self.throwableIndex

    def getBasePrice(self):
        return 5

    def loadModel(self):
        type = FurnitureTypes[self.furnitureType]
        model = loader.loadModel(type[FTModelName])
        self.applyColor(model, type[FTColor])
        if type[FTColorOptions] != None:
            if self.colorOption == None:
                option = random.choice(list(type[FTColorOptions].values()))
            else:
                option = type[FTColorOptions].get(self.colorOption)
            self.applyColor(model, option)
        if FTScale < len(type):
            scale = type[FTScale]
            if not scale == None:
                model.setScale(scale)
                model.flattenLight()
        return model

    def decodeDatagram(self, di, versionNumber, store):
        CatalogItem.CatalogItem.decodeDatagram(self, di, versionNumber, store)
        self.throwableIndex = di.getUint8()
        if versionNumber >= 6:
            self.loyaltyDays = di.getUint16()
        else:
            self.loyaltyDays = 0
        if self.throwableIndex > len(OTPLocalizer.EmoteList):
            raise ValueError

    def encodeDatagram(self, dg, store):
        CatalogItem.CatalogItem.encodeDatagram(self, dg, store)
        dg.addUint8(self.throwableIndex)
        dg.addUint16(self.loyaltyDays)
