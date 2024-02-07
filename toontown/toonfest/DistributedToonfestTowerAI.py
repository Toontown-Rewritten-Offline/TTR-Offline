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
import random

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

    def d_updateTower(self, operation, base, avName):
        #self.sendUpdate('updateTower', [operation, base])
        offset = 1.11
        timestamp = 32
        rpm = 5
        self.validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        if operation not in self.validOperations:
            print('DistributedToonfestTower: Operation %s is not a valid operation.' % operation)
        if base < 0 or base > 2:
            print('DistributedToonfestTower: Invalid base ' + str(base))
        print('Made base ' + str(base + 1) + ' ' + operation)
        if operation == 'SpeedUp':
            rpm = rpm + round(random.uniform(1, 3), 3)
            print(rpm)
            self.air.tfb.setSpeed(rpm, offset, timestamp, base, operation, avName)
        if operation == 'SlowDown':
            rpm = rpm - round(random.uniform(1, 3), 3)
            print(rpm)
            self.air.tfb.setSpeed(rpm, offset, timestamp, base, operation, avName)
        if operation == 'Reverse':
            rpm = rpm + round(random.uniform(-6, -8), 3)
            print(rpm)
            self.air.tfb.setSpeed(rpm, offset, timestamp, base, operation, avName)