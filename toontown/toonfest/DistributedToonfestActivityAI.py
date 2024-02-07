from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.parties import PartyGlobals, PartyUtils # Still relying on PartyGlobals, soon to be changed
"""
dclass DistributedPartyActivity : DistributedObject {
  setX(int16/10) broadcast required;
  setY(int16/10) broadcast required;
  setH(uint16%360/100) broadcast required;
  setPartyDoId(uint32) broadcast required;
  toonJoinRequest() airecv clsend;
  toonExitRequest() airecv clsend;
  toonExitDemand() airecv clsend;
  toonReady() airecv clsend;
  joinRequestDenied(uint8);
  exitRequestDenied(uint8);
  setToonsPlaying(uint32 []) broadcast ram;
  setState(string, int16) broadcast ram;
  showJellybeanReward(uint32, uint8, string);
};
"""
class DistributedToonfestActivityAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonfestActivityAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.toonsPlaying = []

    def updateToonsPlaying(self):
        self.sendUpdate('setToonsPlaying', [self.toonsPlaying])

    def toonJoinRequest(self):
        print('toon join request')
        avId = self.air.getAvatarIdFromSender()
        #todo hackyfun i should FSM
        self.toonsPlaying.append(avId)
        self.updateToonsPlaying()

    def toonExitRequest(self):
        print('toon exit request')

    def toonExitDemand(self):
        print('toon exit demand')
        avId = self.air.getAvatarIdFromSender()
        self.toonsPlaying.remove(avId)
        self.updateToonsPlaying()

    def toonReady(self):
        print('toon ready')

    def joinRequestDenied(self, todo0):
        pass

    def exitRequestDenied(self, todo0):
        pass

    def setToonsPlaying(self, todo0):
        pass

    def setState(self, todo0, todo1):
        pass

    def showJellybeanReward(self, todo0, todo1, todo2):
        pass

