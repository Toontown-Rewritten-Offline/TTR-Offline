# Embedded file name: toontown.election.DistributedToonfestCogAI
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM
from otp.ai.MagicWordGlobal import *
from toontown.election.DistributedHotAirBalloonAI import DistributedHotAirBalloonAI
from toontown.election.DistributedElectionCameraManagerAI import DistributedElectionCameraManagerAI
from toontown.election.DistributedSafezoneInvasionAI import DistributedSafezoneInvasionAI
from toontown.election.DistributedInvasionSuitAI import DistributedInvasionSuitAI
from toontown.election.InvasionMasterAI import InvasionMasterAI
from toontown.toonbase import ToontownGlobals
import toontown.election.SafezoneInvasionGlobals
import toontown.election.ElectionGlobals
from toontown.toonfest import DistributedToonfestTowerAI
import random
from otp.distributed.OtpDoGlobals import *
from direct.task import Task
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedToonfestCogAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerAI')

    def __init__(self, air, operation = 'SpeedUp'):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'ToonfestCogFSM')
        self.air = air

    def enterOff(self):
        self.requestDelete()

    def setPos(self, x, y, z):
        self.sendUpdate('setPosThroughAI', [x, y, z])

    def setId(self, cogid):
        self.sendUpdate('setIdThroughAI', [cogid])

    def enterDown(self):
        pass

    def enterUp(self):
        pass

    def updateTower(self):
        base = random.randrange(0, 3)
        validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        for operation in validOperations:
            operation = random.choice(validOperations)
        if not DistributedToonfestTowerAI or not self.air.toonfestTower:
            print('DistributedToonfestCogAI: ERROR! Could not find the ToonFest Tower.')
        else:
            self.air.toonfestTower.d_updateTower(operation, base)
        print('DistributedToonfestCogAI: Told Tower to ' + operation + ' base number ' + str(base + 1))
