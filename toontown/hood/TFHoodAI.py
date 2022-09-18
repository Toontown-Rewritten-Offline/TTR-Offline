from panda3d.core import *
from direct.task import Task
from .SZHoodAI import SZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone.DistributedPicnicTableAI import DistributedPicnicTableAI
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.toonfest import DistributedToonfestDayNightAI
from toontown.toonfest import DistributedToonfestTowerAI
from toontown.toonfest import DistributedToonfestTowerBaseAI
from toontown.toonfest import DistributedToonfestVictoryTrampolineActivityAI
from toontown.toonfest import DistributedToonfestCogAI
#from toontown.toonfest import DistributedToonfestCannonActivityAI
#from toontown.toonfest.DistributedToonfestCannonAI import DistributedToonfestCannonAI
#from toontown.toonfest import DistributedToonfestBalloonAI

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
        self.toonfestTower = DistributedToonfestTowerAI.DistributedToonfestTowerAI(self.air)
        self.toonfestTower.generateWithRequired(self.HOOD)
        self.toonfestTowerBase = DistributedToonfestTowerBaseAI.DistributedToonfestTowerBaseAI(self.air)
        self.toonfestTowerBase.generateWithRequired(self.HOOD)
        self.toonfestTramp = DistributedToonfestVictoryTrampolineActivityAI.DistributedToonfestVictoryTrampolineActivityAI(self.air)
        self.toonfestTramp.generateWithRequired(self.HOOD)
        self.toonfestDayNight = DistributedToonfestDayNightAI.DistributedToonfestDayNightAI(self.air)
        self.toonfestDayNight.generateWithRequired(self.HOOD)
        #self.cannonActivity = DistributedToonfestCannonActivityAI.DistributedToonfestCannonActivityAI(self.air)
        #self.cannonActivity.generateWithRequired(self.HOOD)
        #self.act = DistributedToonfestCannonAI(self.air)
        #self.act.generateWithRequired(self.HOOD)
        #self.act.setActivityDoId(self.cannonActivity.doId)
        self.loadToonfestCogs()

    def loadToonfestCogs(self):
        self.cog1 = DistributedToonfestCogAI.DistributedToonfestCogAI(self.air)
        self.cog1.checkClientTask(139, -94, 4.579, 1)
        self.cog1.generateWithRequired(self.HOOD)
        self.cogs.append(self.cog1)

        self.cog2 = DistributedToonfestCogAI.DistributedToonfestCogAI(self.air)
        self.cog2.checkClientTask(130, -94, 4.579, 2)
        #self.cog2.generateWithRequired(self.HOOD)
        self.cogs.append(self.cog2)
