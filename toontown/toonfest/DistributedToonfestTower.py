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
from direct.gui.DirectGui import OnscreenText
from direct.directnotify import DirectNotifyGlobal
import random
from otp.speedchat import SpeedChatGlobals

class DistributedToonfestTower(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTower')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestTowerFSM')

    def delete(self):
        self.demand('Off')
        #self.towerGeom.removeNode()
        DistributedObject.delete(self)

    def updateTower(self, operation, base):
        print('Tower changing!')