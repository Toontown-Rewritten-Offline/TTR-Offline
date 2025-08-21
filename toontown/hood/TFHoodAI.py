from panda3d.core import *
from direct.task import Task
from .SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.toonfest.DistributedToonfestDayNightAI import DistributedToonfestDayNightAI
from toontown.toonfest.DistributedToonfestTowerAI import DistributedToonfestTowerAI
from toontown.toonfest.DistributedToonfestTowerBaseAI import DistributedToonfestTowerBaseAI
from toontown.toonfest.DistributedToonfestVictoryTrampolineActivityAI import DistributedToonfestVictoryTrampolineActivityAI
from toontown.toonfest.DistributedToonfestCogAI import DistributedToonfestCogAI
#from toontown.toonfest.DistributedToonfestCannonActivityAI import DistributedToonfestCannonActivityAI

class TFHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.ToonFest

    def createZone(self):
        SZHoodAI.createZone(self, False)
        self.spawnObjects()
        self.cogs = []
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.toonfestTower = DistributedToonfestTowerAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
        self.toonfestTowerBase = DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTowerBase.generateWithRequired(self.HOOD)
        self.toonfestTramp = DistributedToonfestVictoryTrampolineActivityAI(self.air)
        self.toonfestTramp.generateWithRequired(self.HOOD)
        #self.toonfestDayNight = DistributedToonfestDayNightAI(self.air)
        #self.toonfestDayNight.generateWithRequired(self.HOOD)
        #self.cannonActivity = DistributedToonfestCannonActivityAI(self.air)
        #self.cannonActivity.generateWithRequired(self.HOOD)
        self.loadActivities()

    def loadActivities(self):
        self.cog1 = DistributedToonfestCogAI(self.air)
        self.cog1.position = (139, -94, 4.579)
        self.cog1.cogid = 1
        self.cog1.generateWithRequired(self.HOOD)
        self.cogs.append(self.cog1)

        #self.cog2 = DistributedToonfestCogAI(self.air)
        #self.cog2.position = (130, -94, 4.579)
        #self.cog2.cogid = 1
        #self.cog2.generateWithRequired(self.HOOD)
        #self.cogs.append(self.cog2)

