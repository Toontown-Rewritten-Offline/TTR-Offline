# Embedded file name: toontown.safezone.TFPlayground
from panda3d.core import *
from toontown.toonbase import ToontownGlobals
from . import Playground
from toontown.launcher import DownloadForceAcknowledge
from toontown.building import Elevator
from toontown.toontowngui import TTDialog
from toontown.toonbase import TTLocalizer
from toontown.racing import RaceGlobals
from direct.fsm import ClassicFSM, State
from toontown.safezone import PicnicBasket
from direct.task.Task import Task

class TFPlayground(Playground.Playground):

    def __init__(self, loader, parentFSM, doneEvent):
        Playground.Playground.__init__(self, loader, parentFSM, doneEvent)
        self.parentFSM = parentFSM
        self.towerFsm = ClassicFSM.ClassicFSM('Tower', [State.State('off', self.enterOff, self.exitOff, ['OnBase1', 'OnBase2', 'OnBase3']),
         State.State('OnBase1', self.enterOnBase1, self.exitOnBase1, ['off', 'OnBase2', 'OnBase3']),
         State.State('OnBase2', self.enterOnBase2, self.exitOnBase2, ['off', 'OnBase1', 'OnBase3']),
         State.State('OnBase3', self.enterOnBase3, self.exitOnBase3, ['off', 'OnBase2', 'OnBase1'])], 'off', 'off')
        self.towerFsm.enterInitialState()
        

    def load(self):
        Playground.Playground.load(self)

    def unload(self):
        Playground.Playground.unload(self)

    def enter(self, requestStatus):
        Playground.Playground.enter(self, requestStatus)

    def exit(self):
        Playground.Playground.exit(self)

    def doRequestLeave(self, requestStatus):
        self.fsm.request('trialerFA', [requestStatus])

    def enterOnBase1(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerLarge)

    def exitOnBase1(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def enterOnBase2(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerMed)

    def exitOnBase2(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def enterOnBase3(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPToonfestTowerSmall)

    def exitOnBase3(self):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def enterOff(self):
        return None

    def exitOff(self):
        return None

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def enterActivity(self, setAnimState = True):
        print('Entered Activity')
        if setAnimState:
            base.localAvatar.b_setAnimState('neutral', 1)
        base.localAvatar.setTeleportAvailable(False)
        base.localAvatar.laffMeter.start()

    def exitActivity(self):
        base.localAvatar.setTeleportAvailable(True)
        base.localAvatar.laffMeter.stop()

    def detectedPicnicTableSphereCollision(self, picnicBasket):
        self.fsm.request('picnicBasketBlock', [picnicBasket])

    def handleStartingBlockDone(self, doneStatus):
        self.notify.debug('handling StartingBlock done event')
        where = doneStatus['where']
        if where == 'reject':
            self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'racetrack':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleStartingBlockDone')

    def handlePicnicBasketDone(self, doneStatus):
        self.notify.debug('handling picnic basket done event')
        mode = doneStatus['mode']
        if mode == 'reject':
            self.fsm.request('walk')
        elif mode == 'exit':
            self.fsm.request('walk')
        else:
            self.notify.error('Unknown mode: ' + mode + ' in handlePicnicBasketDone')