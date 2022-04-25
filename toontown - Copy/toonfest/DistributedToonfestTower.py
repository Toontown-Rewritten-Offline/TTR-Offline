# Embedded file name: toontown.election.DistributedToonfestTower
from panda3d.core import *
import random
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toonfest import DistributedToonfestTowerBase
from toontown.toon import NPCToons
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import toontown.election.ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
import random
from otp.speedchat import SpeedChatGlobals

class DistributedToonfestTower(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTower')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestTowerFSM')
        #self.towerGeom = loader.loadModel('phase_6/models/events/ttr_m_tf_tower')
        #self.towerGeom.reparentTo(render)
        #self.towerGeom.setH(-30)
        #self.towerGeom.setPos(221, -61, 4.5)
        #self.base1 = self.towerGeom.find('**/base1')
        #self.base2 = self.towerGeom.find('**/base2')
        #self.base3 = self.towerGeom.find('**/base3')
        #self.tfb = DistributedToonfestTowerBase.DistributedToonfestTowerBase

    def delete(self):
        self.demand('Off')
        #self.towerGeom.removeNode()
        DistributedObject.delete(self)

    def updateTower(self, operation, base):
        print('Tower changing!')
        offset = 1.11
        timestamp = 32
        self.validOperations = ['SpeedUp', 'SlowDown', 'Reverse']
        if operation not in self.validOperations:
            print('DistributedToonfestTower: Operation %s is not a valid operation.' % operation)
        if base < 0 or base > 2:
            print('DistributedToonfestTower: Invalid base ' + str(base))
        print('Made base ' + str(base + 1) + ' ' + operation)
        if operation == 'SpeedUp':
            rpm = round(random.uniform(6, 7), 3)
            print(rpm)
            self.cr.tfb.setSpeed(rpm, offset, timestamp)
        if operation == 'SlowDown':
            rpm = round(random.uniform(3, 4), 3)
            print(rpm)
            self.cr.tfb.setSpeed(rpm, offset, timestamp)
        if operation == 'Reverse':
            rpm = round(random.uniform(-3, -4), 3)
            print(rpm)
            self.cr.tfb.setSpeed(rpm, offset, timestamp)