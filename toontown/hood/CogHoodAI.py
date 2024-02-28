from toontown.toonbase import ToontownGlobals
from .HoodAI import HoodAI
from toontown.suit.DistributedSuitPlannerAI import DistributedSuitPlannerAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.coghq import DistributedCogKartAI
from toontown.coghq.LobbyManagerAI import LobbyManagerAI
from toontown.building import DistributedBoardingPartyAI

class CogHoodAI(HoodAI):
    """
    This class is an AI-sided representation of a single cog
    neighborhood in Toontown.

    A sub-class of this class exists for each of the 4 types
    of cog neighborhoods. CogHoodAIs are responsible for
    spawning the Cog Elevators, Cog Doors and the SuitPlanners.
    """

    def __init__(self, air):
        HoodAI.__init__(self, air)
        self.doors = []
        self.elevators = []
        self.suitPlanners = []
        self.lobbyMgr = None

    def createElevator(self, dclass, mgr, extZone, intZone, index=0, minLaff=0, boss=False):
        if boss:
            elevator = dclass(self.air, mgr, intZone, antiShuffle=self.air.config.GetInt('want-anti-shuffle', 0), minLaff=minLaff)
        else:
            elevator = dclass(self.air, mgr, intZone, index, antiShuffle=self.air.config.GetInt('want-anti-shuffle', 0), minLaff=minLaff)
        elevator.generateWithRequired(extZone)
        self.elevators.append(elevator)
        return elevator

    def createDoor(self):
        # Overridable by sub-class.
        pass

    def createBoardingGroup(self, air, elevators, zone, maxSize=4):
        if config.GetBool('want-boarding-groups', True):
            boardingGroup = DistributedBoardingPartyAI.DistributedBoardingPartyAI(air, elevators, maxSize)
            boardingGroup.generateWithRequired(zone)

    def createSuitPlanner(self, zone):
        sp = DistributedSuitPlannerAI(self.air, zone)
        sp.generateWithRequired(zone)
        sp.d_setZoneId(zone)
        sp.initTasks()
        self.air.suitPlanners[zone] = sp
        self.suitPlanners.append(sp)

    def createLobbyManager(self, boss, zone):
        self.lobbyMgr = LobbyManagerAI(self.air, boss)
        self.lobbyMgr.generateWithRequired(zone)
