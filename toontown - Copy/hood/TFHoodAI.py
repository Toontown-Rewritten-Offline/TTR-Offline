from .SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
#from toontown.toonfest import DistributedToonfestActivityAI
from toontown.toonfest import DistributedToonfestTowerAI
from toontown.toonfest import DistributedToonfestTowerBaseAI
from toontown.toonfest import DistributedToonfestVictoryTrampolineActivityAI
#from toontown.toonfest import DistributedToonfestCogAI
#from toontown.toonfest import DistributedToonfestCannonActivityAI
#from toontown.toonfest.DistributedToonfestCannonAI import DistributedToonfestCannonAI
#from toontown.toonfest import DistributedToonfestBalloonAI

from direct.fsm.FSM import FSM
from panda3d.core import *

class TFHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.ToonFest

    def createZone(self):
        SZHoodAI.createZone(self, False)
        self.spawnObjects()
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.toonfestTower = DistributedToonfestTowerAI.DistributedToonfestTowerAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
        self.toonfestTowerBase = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTowerBase.generateWithRequired(self.HOOD)
        self.toonfestTramp = DistributedToonfestVictoryTrampolineActivityAI.DistributedToonfestVictoryTrampolineActivityAI(self.air)
        self.toonfestTramp.generateWithRequired(self.HOOD)
        #self.cannonActivity = DistributedToonfestCannonActivityAI.DistributedToonfestCannonActivityAI(self.air)
        #self.cannonActivity.generateWithRequired(self.HOOD)
        #self.act = DistributedToonfestCannonAI(self.air)
        #self.act.generateWithRequired(self.HOOD)
        #self.act.setActivityDoId(self.cannonActivity.doId)
        #act.setPos(156, -146, 4.579)
        #self.toonfestActivities = DistributedToonfestActivityAI.DistributedToonfestActivityAI(self.air)
        #self.toonfestActivities.generateWithRequired(self.HOOD)
        #self.cog = DistributedToonfestCogAI.DistributedToonfestCogAI(self.air)
        #self.cog.generateWithRequired(self.HOOD)
        #self.cog.setPos(139, -94, 4)
        #self.cog.setId(1)
        #self.cogs = []
        #self.cogs.append(self.cog)