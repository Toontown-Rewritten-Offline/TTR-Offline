from panda3d.core import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from toontown.building.ElevatorConstants import *
from toontown.building.ElevatorUtils import *
from toontown.building import DistributedElevatorExt
from toontown.building import DistributedElevator
from toontown.toonbase import ToontownGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from toontown.hood import ZoneUtil
from toontown.suit import Suit
from toontown.toonbase import TTLocalizer

class DistributedFactoryElevatorExt(DistributedElevatorExt.DistributedElevatorExt):

    def __init__(self, cr):
        DistributedElevatorExt.DistributedElevatorExt.__init__(self, cr)

    def generate(self):
        DistributedElevatorExt.DistributedElevatorExt.generate(self)

    def delete(self):
        self.elevatorModel.removeNode()
        del self.elevatorModel
        DistributedElevatorExt.DistributedElevatorExt.delete(self)

    def setEntranceId(self, entranceId):
        self.entranceId = entranceId
        if self.entranceId == 0:
            self.elevatorModel.setPosHpr(62.74, -85.31, 0.0, 2.0, 0.0, 0.0)
            self.cab = self.elevatorModel.find('**/elevator')
            cogIcons = loader.loadModel('phase_3.5/models/props/ttr_m_ara_gen_cogIcons')
            corpIcon = cogIcons.find('**/SalesIcon').copyTo(self.cab)
            corpIcon.setPos(0, 6.79, 6.8)
            corpIcon.setScale(3)
            corpIcon.setColor(Vec4(0.843, 0.745, 0.745, 1.0))
            cogIcons.removeNode()
        elif self.entranceId == 1:
             self.elevatorModel.setPosHpr(-133.455, -12.0889, 0, 0.0, 0.0, 0.0)
             self.cab = self.elevatorModel.find('**/elevator')
             gearIcons = loader.loadModel('phase_3.5/models/props/ttr_m_ara_gen_cogToughIcons')
             gearIcon = gearIcons.find('**/geo_M_ToughSalesIcon_01').copyTo(self.cab)
             gearIcon.setPos(0, 6.79, 6.8)
             gearIcon.setScale(1.2)
             gearIcon.setColor(Vec4(0.843, 0.745, 0.745, 1.0))
             gearIcons.removeNode()
             cogIcons = loader.loadModel('phase_3.5/models/props/ttr_m_ara_gen_cogIcons')
             corpIcon = cogIcons.find('**/SalesIcon').copyTo(self.cab)
             corpIcon.setPos(0, 6.78, 6.8)
             corpIcon.setScale(3)
             corpIcon.setColor(Vec4(0.843, 0.745, 0.745, 1.0))
             cogIcons.removeNode()
        else:
            self.notify.error('Invalid entranceId: %s' % entranceId)

    def setupElevator(self):
        self.elevatorModel = loader.loadModel('phase_9/models/cogHQ/ttr_m_ara_shq_elevatorFactory')
        self.elevatorModel.reparentTo(render)
        self.elevatorModel.setScale(1.05)
        self.leftDoor = self.elevatorModel.find('**/left_door')
        self.rightDoor = self.elevatorModel.find('**/right_door')
        self.elevatorModel.find('**/light_panel').removeNode()
        DistributedElevator.DistributedElevator.setupElevator(self)

    def getElevatorModel(self):
        return self.elevatorModel

    def setBldgDoId(self, bldgDoId):
        self.bldg = None
        self.setupElevator()
        return

    def getZoneId(self):
        return 0

    def __doorsClosed(self, zoneId):
        pass

    def setFactoryInteriorZone(self, zoneId):
        if self.localToonOnBoard:
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {'loader': 'cogHQLoader',
             'where': 'factoryInterior',
             'how': 'teleportIn',
             'zoneId': zoneId,
             'hoodId': hoodId}
            self.cr.playGame.getPlace().elevator.signalDone(doneStatus)

    def setFactoryInteriorZoneForce(self, zoneId):
        place = self.cr.playGame.getPlace()
        if place:
            place.fsm.request('elevator', [self, 1])
            hoodId = self.cr.playGame.hood.hoodId
            doneStatus = {'loader': 'cogHQLoader',
             'where': 'factoryInterior',
             'how': 'teleportIn',
             'zoneId': zoneId,
             'hoodId': hoodId}
            if hasattr(place, 'elevator') and place.elevator:
                place.elevator.signalDone(doneStatus)
            else:
                self.notify.warning("setMintInteriorZoneForce: Couldn't find playGame.getPlace().elevator, zoneId: %s" % zoneId)
        else:
            self.notify.warning("setFactoryInteriorZoneForce: Couldn't find playGame.getPlace(), zoneId: %s" % zoneId)

    def getDestName(self):
        if self.entranceId == 0:
            return TTLocalizer.ElevatorSellBotFactory0
        elif self.entranceId == 1:
            return TTLocalizer.ElevatorSellBotFactory1
