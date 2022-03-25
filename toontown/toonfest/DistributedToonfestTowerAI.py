# Embedded file name: toontown.election.DistributedToonfestTowerAI
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from toontown.election.DistributedElectionCameraManagerAI import DistributedElectionCameraManagerAI
from toontown.election.DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from toontown.election.DistributedInvasionSuitAI import DistributedInvasionSuitAI
from toontown.election.InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
from toontown.toonfest import DistributedToonfestTowerBaseAI
import toontown.election.SafezoneInvasionGlobals
import toontown.election.ElectionGlobals
from otp.distributed.OtpDoGlobals import *
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedToonfestTowerAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ToonfestTowerFSM')
        self.air = air
        self.air.toonfestTower = self

    def enterOff(self):
        self.requestDelete()
        self.air.toonfestTower = None
        return

    def d_updateTower(self, operation, base):
        self.sendUpdate('updateTower', [operation, base])