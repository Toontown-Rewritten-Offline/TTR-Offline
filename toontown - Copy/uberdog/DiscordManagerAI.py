from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectAI
import string
import random


class DiscordManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DiscordManagerAI')

    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.districtLimit = self.air.districtLimit
        self.districtId = self.air.districtId
        self.partyId = "69"
        tmp = string.ascii_lowercase + string.ascii_uppercase + string.digits
        for _ in range(30):
            self.partyId += random.choice(tmp)
        self.notify.debug("Party ID set to: {}".format(self.partyId))

    def setDistrictLimit(self, districtLimit):
        self.districtLimit = districtLimit

    def getDistrictLimit(self):
        return self.districtLimit

    def setDistrictId(self, districtId):
        self.districtId = districtId

    def getDistrictId(self):
        return self.districtId

    def getPartyId(self):
        return self.partyId
