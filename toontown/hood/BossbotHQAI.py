from .CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedBossbotBossAI import DistributedBossbotBossAI
from toontown.building.DistributedBBElevatorAI import DistributedBBElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.coghq.DistributedCogKartAI import DistributedCogKartAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes

class BossbotHQAI(CogHoodAI):
    HOOD = ToontownGlobals.BossbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.karts = []
        self.createZone()
        
    def createDoor(self):
        # CEO Battle
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD, doorIndex=0)
        exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.BossbotLobby, doorIndex=0, lockValue=FADoorCodes.BB_DISGUISE_INCOMPLETE)
        exteriorDoor.setOtherDoor(interiorDoor)
        exteriorDoor.zoneId = self.HOOD
        exteriorDoor.generateWithRequired(self.HOOD)
        exteriorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(exteriorDoor)

        interiorDoor.setOtherDoor(exteriorDoor)
        interiorDoor.zoneId = ToontownGlobals.BossbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.BossbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor) 

        # Executive Office
        executiveDoor = DistributedCogHQDoorAI(self.air, 1, DoorTypes.EXT_COGHQ, ToontownGlobals.BossbotLobby, doorIndex=1, lockValue=FADoorCodes.UNKNOWN_COG_AREA)
        executiveDoor.setOtherDoor(interiorDoor)
        executiveDoor.zoneId = self.HOOD
        executiveDoor.generateWithRequired(self.HOOD)
        executiveDoor.sendUpdate('setDoorIndex', [1])
        
    def createKart(self, index, x, y, z, h, p, r, min):
        kart = DistributedCogKartAI(self.air, index, x, y, z, h, p, r, self.air.countryClubMgr, min)
        kart.generateWithRequired(self.HOOD)
        self.karts.append(kart)
        return kart
    
    def createZone(self):
        CogHoodAI.createZone(self)
        
        # Create lobby manager...
        self.createLobbyManager(DistributedBossbotBossAI, ToontownGlobals.BossbotLobby)
        
        # Create CEO elevator.
        self.ceoElevator = self.createElevator(DistributedBBElevatorAI, self.lobbyMgr, ToontownGlobals.BossbotLobby, ToontownGlobals.BossbotLobby, boss=True)
        
        # Make our doors.
        self.createDoor()
        
        # Create Suit Planners in the cog playground and factory waiting area.
        self.createSuitPlanner(self.HOOD)
        
        # Create Cog Golf Courses.
        kartPos = ((-26.5658, 237.459, 0), (132.197, 227.845, 0), (-28.725, -235.706, 0))
        hprList = ((-159, 0, 0), (172, 0, 0), (-21, 0, 0))

        mins = ToontownGlobals.FactoryLaffMinimums[3]
        for i in range(3):
            x, y, z = kartPos[i]
            h, p, r = hprList[i]
            self.createKart(i, x, y, z, h, p, r, mins[i])

        # Create boarding groups
        # CEO Boarding Group
        self.createBoardingGroup(self.air, [self.ceoElevator.doId], ToontownGlobals.BossbotLobby, 8)

        # Cog Golf Boarding Group's
        kartIds = [kart.getDoId() for kart in self.karts]
        self.createBoardingGroup(self.air, kartIds, ToontownGlobals.BossbotHQ)
