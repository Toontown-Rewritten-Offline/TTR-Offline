from panda3d.core import *
from direct.task import Task
from otp.avatar import Avatar
from otp.nametag.NametagConstants import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm.FSM import FSM
from direct.actor import Actor
from direct.task import Task
from toontown.toon import NPCToons
from toontown.suit import DistributedSuitBase, SuitDNA
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.battle import BattleProps
from otp.margins.WhisperPopup import *
import toontown.election.ElectionGlobals
from direct.directnotify import DirectNotifyGlobal
from random import choice
from .ToonfestCog import ToonfestCog
from toontown.battle.BattleProps import globalPropPool
from toontown.battle.BattleSounds import globalBattleSoundCache
from toontown.parties import *
from otp.speedchat import SpeedChatGlobals

class DistributedToonfestCog(DistributedObject, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedToonfestCog')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.__init__(self, 'ToonfestCogFSM')
        taskMgr.add(self.d_generateRequest, 'GenerateRequest')
        taskMgr.add(self.load, 'LoadCogs')
        self.root = NodePath('ToonfestCog')
        self.parentNode = NodePath('Parent')
        self.requestSent = False
        self.state = 'Down'
        self.cogid = 0
        self.accept('localPieSplat', self.__localPieSplat)
        self.targetDistance = 0.0
        self.targetFacing = 0.0
        self.currentT = 0.0
        self.timestamp = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(), bits=32)
        self.toon = base.localAvatar
        self.avName = self.toon.getName()
        self.position = self.toon.getPos()
        self.netTimeSentToStartByHit = 0
        self.currentFacing = 0.0

    def d_generateRequest(self, task):
        if self.isGenerated():
            self.sendUpdate('generateRequest', [])
            self.requestSent = True
            return Task.done
        else:
            return Task.cont

    def load(self, task):
        if self.requestSent:
            self.setCogProperties()
            return Task.done
        else:
            return Task.cont

    def setCogProperties(self):
        self.parentNode.reparentTo(render)
        self.root.reparentTo(render)
        path = 'phase_13/models/parties/cogPinata_'
        self.actor = Actor.Actor(path + 'actor', {'idle': path + 'idle_anim',
         'down': path + 'down_anim',
         'up': path + 'up_anim',
         'bodyHitBack': path + 'bodyHitBack_anim',
         'bodyHitFront': path + 'bodyHitFront_anim',
         'headHitBack': path + 'headHitBack_anim',
         'headHitFront': path + 'headHitFront_anim'})
        self.actor.setBlend(ConfigVariableBool('smoothanimations', False))
        self.actor.reparentTo(self.root)
        self.temp_transform = Mat4()
        self.head_locator = self.actor.attachNewNode('temphead')
        self.bodyColl = CollisionTube(0, 0, 1, 0, 0, 5.75, 0.75)
        self.bodyColl.setTangible(1)
        self.bodyCollNode = CollisionNode('ToonfestCog-Body-Collision')
        self.bodyCollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.bodyCollNode.addSolid(self.bodyColl)
        self.bodyCollNode.setTag('pieCode', str(ToontownGlobals.PieCodeToonfestCog))
        self.bodyCollNodePath = self.root.attachNewNode(self.bodyCollNode)
        self.headColl = CollisionTube(0, 0, 3, 0, 0, 3.0, 1.5)
        self.headColl.setTangible(1)
        self.headCollNode = CollisionNode('ToonfestCog-Head-Collision')
        self.headCollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.headCollNode.addSolid(self.headColl)
        self.headCollNode.setTag('pieCode', str(ToontownGlobals.PieCodeToonfestCog))
        self.headCollNodePath = self.root.attachNewNode(self.headCollNode)
        self.arm1Coll = CollisionSphere(1.65, 0, 3.95, 1.0)
        self.arm1Coll.setTangible(1)
        self.arm1CollNode = CollisionNode('ToonfestCog-Arm1-Collision')
        self.arm1CollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.arm1CollNode.addSolid(self.arm1Coll)
        self.arm1CollNode.setTag('pieCode', str(ToontownGlobals.PieCodeToonfestCog))
        self.arm1CollNodePath = self.root.attachNewNode(self.arm1CollNode)
        self.arm2Coll = CollisionSphere(-1.65, 0, 3.45, 1.0)
        self.arm2Coll.setTangible(1)
        self.arm2CollNode = CollisionNode('ToonfestCog-Arm2-Collision')
        self.arm2CollNode.setCollideMask(ToontownGlobals.PieBitmask)
        self.arm2CollNode.addSolid(self.arm2Coll)
        self.arm2CollNode.setTag('pieCode', str(ToontownGlobals.PieCodeToonfestCog))
        self.arm2CollNodePath = self.root.attachNewNode(self.arm2CollNode)
        splatName = 'splat-creampie'
        self.splat = globalPropPool.getProp(splatName)
        self.splat.setBillboardPointEye()
        self.splatType = globalPropPool.getPropType(splatName)
        self.pieHitSound = globalBattleSoundCache.getSound('AA_wholepie_only.ogg')
        self.upSound = globalBattleSoundCache.getSound('AV_jump_to_side.ogg')
        self.hole = loader.loadModel('phase_13/models/parties/cogPinataHole')
        self.hole.setTransparency(True)
        self.hole.setP(-90.0)
        self.hole.setScale(3)
        self.hole.setBin('ground', 3)
        self.hole.reparentTo(self.parentNode)
        #taskMgr.doMethodLater(10, self.toggleCog, 'toggle-cog', extraArgs=[])
        self.kaboomTrack = None
        self.hitInterval = None
        self.resetRollIval = None

    def setCogPosId(self, x, y, z, cogid):
        self.root.setPos(x, y, z)
        self.parentNode.setPos(x, y, z)
        self.cogid = cogid
        print('Position set!')

    def setCogPos(self, x, y, z):
        self.root.setPos(x, y, z)
        self.parentNode.setPos(x, y, z)

    def setCogId(self, cogid):
        self.cogid = cogid

    def toggleCog(self, state):
        if state == 'Down':
            self.state = 'Up'
            self.request('Up')
        elif state == 'Up':
            self.state = 'Down'
            self.request('Down')

    def unload(self):
        taskMgr.remove('GenerateRequest')
        taskMgr.remove('toggle-cog')
        taskMgr.remove('LoadCogs')
        self.request('Off')
        self.clearHitInterval()
        if self.hole != None:
            self.hole.removeNode()
            self.hole = None
        if self.actor != None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None
        if self.root != None:
            self.root.removeNode()
            self.root = None
        if self.kaboomTrack != None and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.kaboomTrack = None
        if self.resetRollIval != None and self.resetRollIval.isPlaying():
            self.resetRollIval.finish()
        self.resetRollIval = None
        if self.hitInterval != None and self.hitInterval.isPlaying():
            self.hitInterval.finish()
        self.hitInterval = None
        del self.upSound
        del self.pieHitSound
        return

    def delete(self):
        self.unload()
        DistributedObject.delete(self)

    def enterDown(self):
        if self.oldState == 'Off':
            downAnimControl = self.actor.getAnimControl('down')
            self.actor.pose('down', downAnimControl.getNumFrames() - 1)
            return
        self.clearHitInterval()
        startScale = self.hole.getScale()
        endScale = Point3(5, 5, 5)
        self.hitInterval = Sequence(LerpScaleInterval(self.hole, duration=0.175, scale=endScale, startScale=startScale, blendType='easeIn'), Parallel(SoundInterval(self.upSound, volume=0.6, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), ActorInterval(self.actor, 'down', loop=0)), LerpScaleInterval(self.hole, duration=0.175, scale=Point3(3, 3, 3), startScale=endScale, blendType='easeOut'))
        self.hitInterval.start()

    def enterUp(self):
        self.root.setR(0.0)
        self.root.setH(0.0)
        self.targetDistance = 0.0
        self.targetFacing = 0.0
        self.currentT = 0.0
        try:
            self.clearHitInterval()
        except AttributeError:
            print('Done')
        startScale = self.hole.getScale()
        endScale = Point3(5, 5, 5)
        self.hitInterval = Sequence(LerpScaleInterval(self.hole, duration=0.175, scale=endScale, startScale=startScale, blendType='easeIn'), Parallel(SoundInterval(self.upSound, volume=0.6, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), ActorInterval(self.actor, 'up', loop=0)), Func(self.actor.loop, 'idle'), LerpScaleInterval(self.hole, duration=0.175, scale=Point3(3, 3, 3), startScale=endScale, blendType='easeOut'))
        self.hitInterval.start()

    def __localPieSplat(self, pieCode, entry):
        if self.state == 'Up':
            if pieCode == ToontownGlobals.PieCodeToonfestCog:
                self.respondToPieHit(self.timestamp, self.position)

    def respondToPieHit(self, timestamp, position, hot = False, direction = 1.0):
        if self.netTimeSentToStartByHit < timestamp:
            self.__showSplat(position, direction, hot)
            avName = base.localAvatar.name
            self.sendUpdate('updateTower', [avName])
        else:
            print('respondToPieHit self.netTimeSentToStartByHit = %s' % self.netTimeSentToStartByHit)

    def clearHitInterval(self):
        if self.hitInterval != None and self.hitInterval.isPlaying():
            self.hitInterval.clearToInitial()
        return

    def __showSplat(self, position, direction, hot = False):
        if self.kaboomTrack != None and self.kaboomTrack.isPlaying():
            self.kaboomTrack.finish()
        self.clearHitInterval()
        if not direction == 1.0:
            if self.currentFacing > 0.0:
                facing = 'HitFront'
            else:
                facing = 'HitBack'
        else:
            if self.currentFacing > 0.0:
                facing = 'HitBack'
            else:
                facing = 'HitFront'
        if hot:
            targetscale = 0.75
            part = 'head'
        else:
            targetscale = 0.5
            part = 'body'

        self.hitInterval = Sequence(ActorInterval(self.actor, part + facing, loop=0), Func(self.actor.loop, 'idle'))
        self.hitInterval.start()
        self.kaboomTrack = Parallel(SoundInterval(self.pieHitSound, volume=1.0, node=self.actor, cutOff=PartyGlobals.PARTY_COG_CUTOFF), Sequence(Func(self.splat.showThrough), Parallel(Sequence(LerpScaleInterval(self.splat, duration=0.175, scale=targetscale, startScale=Point3(0.1, 0.1, 0.1), blendType='easeOut'), Wait(0.175)), Sequence(Wait(0.1)))))
        self.kaboomTrack.start()
        return