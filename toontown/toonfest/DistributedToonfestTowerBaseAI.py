from panda3d.core import *
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
ChangeDirectionTime = 1.0

class DistributedToonfestTowerBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestTowerBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.air.tfb = self
        self.spinStartTime = 0.0
        self.rpm = 5.0
        self.degreesPerSecond1 = self.rpm / 60.0 * 360.0
        self.degreesPerSecond2 = self.rpm / 60.0 * 360.0
        self.degreesPerSecond3 = self.rpm / 60.0 * 360.0
        self.offset = 0.0

    def requestSpeedUp(self):
        print('Toon on base')

    def requestChangeDirection(self):
        pass

    def setSpeed(self, rpm, offset, timestamp, base, operation, avName):
        timestamp = globalClockDelta.networkToLocalTime(timestamp)
        if base == 0:
            degreesPerSecond1 = rpm / 60.0 * 360.0
            now = globalClock.getFrameTime()
            oldHeading = self.degreesPerSecond1 * (now - self.spinStartTime) + self.offset
            oldHeading = oldHeading % 360.0
            oldOffset = oldHeading - degreesPerSecond1 * (now - timestamp)
            self.rpm = rpm
            self.degreesPerSecond1 = degreesPerSecond1
            self.sendUpdate('setSpeed', [self.degreesPerSecond1, self.degreesPerSecond2, self.degreesPerSecond3])
            self.sendUpdate('playSfxMessage', [operation, avName])
        if base == 1:
            degreesPerSecond2 = rpm / 60.0 * 360.0
            now = globalClock.getFrameTime()
            oldHeading = self.degreesPerSecond2 * (now - self.spinStartTime) + self.offset
            oldHeading = oldHeading % 360.0
            oldOffset = oldHeading - degreesPerSecond2 * (now - timestamp)
            self.rpm = rpm
            self.degreesPerSecond2 = degreesPerSecond2
            self.sendUpdate('setSpeed', [self.degreesPerSecond1, self.degreesPerSecond2, self.degreesPerSecond3])
            self.sendUpdate('playSfxMessage', [operation, avName])
        if base == 2:
            degreesPerSecond3 = rpm / 60.0 * 360.0
            now = globalClock.getFrameTime()
            oldHeading = self.degreesPerSecond3 * (now - self.spinStartTime) + self.offset
            oldHeading = oldHeading % 360.0
            oldOffset = oldHeading - degreesPerSecond3 * (now - timestamp)
            self.rpm = rpm
            self.degreesPerSecond3 = degreesPerSecond3
            self.sendUpdate('setSpeed', [self.degreesPerSecond1, self.degreesPerSecond2, self.degreesPerSecond3])
            self.sendUpdate('playSfxMessage', [operation, avName])
        self.offset = offset
        self.spinStartTime = timestamp
        while oldOffset - offset < -180.0:
            oldOffset += 360.0

        while oldOffset - offset > 180.0:
            oldOffset -= 360.0

        self.oldOffset = oldOffset
        self.lerpStart = now
        self.lerpFinish = timestamp + ChangeDirectionTime

    def playSfxMessage(self, todo0):
        pass

    def playSpeedUp(self, todo0):
        pass

    def playChangeDirection(self, todo0):
        pass
    