from panda3d.core import *
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
        self.clientStarted = False
        self.cogTaskDone = False
        self.state = 'Down'
        self.air = air

    def enterOff(self):
        self.requestDelete()

    def generateRequest(self):
        self.clientStarted = True

    def checkClientTask(self, x, y, z, cogid):
        taskMgr.add(self.loadClientResources, extraArgs=[x, y, z, cogid])

    def loadClientResources(self, x, y, z, cogid):
        if self.clientStarted:
            self.sendUpdate('setCogPosId', [x, y, z, cogid])
            if not self.cogTaskDone:
                self.toggleCogTask()
            print('Cog Done!')
            self.clientStarted = False
            return Task.cont
        else:
            return Task.cont

    #def setCogPosIdTask(self, x, y, z, cogid):
    #    taskMgr.add(self.setCogPosId, extraArgs=[x, y, z, cogid])

    def toggleCogTask(self):
        taskMgr.doMethodLater(10, self.toggleCog, 'toggle-cog', extraArgs=[])
        self.cogTaskDone = True

    def toggleCog(self):
        if self.state == 'Down':
            self.state = 'Up'
            self.enterUp()
        elif self.state == 'Up':
            self.state = 'Down'
            self.enterDown()
        taskMgr.doMethodLater(10, self.toggleCog, 'toggle-cog', extraArgs=[])

    def setCogPosId(self, x, y, z, cogid):
        if self.clientStarted:
            self.sendUpdate('setCogPosId', [x, y, z, cogid])
            self.clientStarted = False
            return Task.cont
        else:
            return Task.cont

    def setCogId(self, cogid):
        self.sendUpdate('setCogId', [cogid])

    def setCogPos(self, x, y, z):
        self.sendUpdate('setCogPos', [x, y, z])

    def enterDown(self):
        self.cogDown = True
        self.sendUpdate('toggleCog', ['Down'])
        print('Cog has gone down.')

    def enterUp(self):
        self.cogUp = True
        self.sendUpdate('toggleCog', ['Up'])
        print('Cog has come up.')

    def updateTower(self, avName):
        base = random.randrange(0, 3)
        validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        for operation in validOperations:
            operation = random.choice(validOperations)
        if not DistributedToonfestTowerAI or not self.air.toonfestTower:
            print('DistributedToonfestCogAI: ERROR! Could not find the ToonFest Tower.')
        else:
            if random.randrange(0, 100) >= 80:
                self.air.toonfestTower.d_updateTower(operation, base, avName)
        print('DistributedToonfestCogAI: Told Tower to ' + operation + ' base number ' + str(base + 1))
