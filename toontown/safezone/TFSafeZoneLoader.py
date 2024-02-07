# Embedded file name: toontown.safezone.TFSafeZoneLoader
from panda3d.core import *
from .SafeZoneLoader import SafeZoneLoader
from . import TFPlayground
from toontown.battle import BattleParticles
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.effects import Bubbles
from toontown.toon import NPCToons
from toontown.election import ElectionGlobals
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from otp.nametag.NametagConstants import *
import math
import random

class TFSafeZoneLoader(SafeZoneLoader):

    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = TFPlayground.TFPlayground
        self.musicFile = 'phase_6/audio/bgm/TF_SZ_1.ogg'
        self.activityMusicFile = 'phase_3.5/audio/bgm/TC_SZ_activity.ogg'
        self.dnaFile = 'phase_6/dna/toonfest_sz.xml'
        self.safeZoneStorageDNAFile = 'phase_6/dna/storage_TF.xml'
        self.restockSfx = loader.loadSfx('phase_9/audio/sfx/CHQ_SOS_pies_restock.ogg')
        self.flippyBlatherSequence = Sequence()
        self.cloudSwitch = 0
        self.clouds = []
        return

    def load(self):
        SafeZoneLoader.load(self)
        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.reparentTo(render)
        self.flippy.setPickable(0)
        self.flippy.setPos(188, -260, 4.597)
        self.flippy.setH(108.411)
        self.flippy.initializeBodyCollisions('toon')
        self.flippy.addActive()
        self.flippy.startBlink()
        self.flippyBlatherSequence = Sequence(Wait(10), Func(self.flippy.setChatAbsolute, 'Welcome Toons, far and wide!', CFSpeech | CFTimeout), Func(self.flippy.play, 'wave'), Func(self.flippy.loop, 'neutral'), Wait(5), Func(self.flippy.setChatAbsolute, "It's been an amazing year at Toontown, and we're glad you could join us!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "Oh, don't mind the little guy back there. That's my new pet, Fluffy.", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, "He's a real rascal, but he already has the Cog-fighting down to a science!", CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Doctor Surlee says he\'s some sort of creature called a "Doodle". Funny name, right?', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Anyway, what are you waiting for?', CFSpeech | CFTimeout), Wait(8), Func(self.flippy.setChatAbsolute, 'Grab some pies, catch some fish, and go for a spin. ToonFest is in full swing!', CFSpeech | CFTimeout))
        self.flippyBlatherSequence.loop()
        self.npctest = NPCToons.createLocalNPC(91000)
        self.npctest.setPickable(0)
        self.npctest.setPos(109, -329, 8.35)
        self.npctest.setH(60)
        self.npctest.reparentTo(render)
        self.npctest.initializeBodyCollisions('toon')
        self.npctest.addActive()
        self.npctest.startBlink()
        self.towerGeom = self.geom.find('**/toonfest_tower_DNARoot')
        self.toonfestDoorsClosed = self.towerGeom.find('**/tf_tower_doors_closed')
        self.toonfestDoorsClosedColl1 = self.towerGeom.find('**/collision_walls_closed_1')
        self.toonfestDoorsClosedColl2 = self.towerGeom.find('**/collision_walls_closed_2')
        self.toonfestDoorsClosed.removeNode()
        self.toonfestDoorsClosedColl1.removeNode()
        self.toonfestDoorsClosedColl2.removeNode()
        try:
            self.base1 = self.towerGeom.find('**/base1')
            self.base2 = self.towerGeom.find('**/base2')
            self.base3 = self.towerGeom.find('**/base3')
        except:
            self.notify.warning('Something messed up loading the tower bases!')
        self.confetti_1 = BattleParticles.loadParticleFile('tf_confetti_1.ptf')
        self.confetti_1.setPos(0, 0, 5)
        self.confetti_2 = BattleParticles.loadParticleFile('tf_confetti_2.ptf')
        self.confetti_2.setPos(0, 0, 5)
        self.confettiRender = self.geom.attachNewNode('confettiRender')
        self.confettiRender.setDepthWrite(0)
        self.confettiRender.setBin('fixed', 1)

    def unload(self):
        SafeZoneLoader.unload(self)
        del self.confetti_1
        del self.confetti_2
        del self.confettiRender
        self.flippyBlatherSequence.finish()
        if self.flippy:
            self.flippy.stopBlink()
            self.flippy.removeActive()
            self.flippy.cleanup()
            self.flippy.removeNode()
        if self.npctest:
            self.npctest.stopBlink()
            self.npctest.removeActive()
            self.npctest.cleanup()
            self.npctest.removeNode()

    def enter(self, requestStatus):
        SafeZoneLoader.enter(self, requestStatus)
        self.confetti_1.start(camera, self.confettiRender)
        self.confetti_2.start(camera, self.confettiRender)

    def exit(self):
        SafeZoneLoader.exit(self)
        self.confetti_1.cleanup()
        self.confetti_2.cleanup()

    def loadClouds(self):
        self.loadCloudPlatforms()
        self.startCloudPlatforms()
        if base.cloudPlatformsEnabled and 0:
            self.setCloudSwitch(1)
        if self.cloudSwitch:
            self.setCloudSwitch(self.cloudSwitch)

    def startCloudPlatforms(self):
        return
        if len(self.clouds):
            self.cloudTrack = self.__cloudTrack()
            self.cloudTrack.loop()

    def stopCloudPlatforms(self):
        if self.cloudTrack:
            self.cloudTrack.pause()
            del self.cloudTrack
            self.cloudTrack = None
        return

    def __cloudTrack(self):
        track = Parallel()
        for cloud in self.clouds:
            axis = cloud[1]
            pos = cloud[0].getPos(render)
            newPos = pos + axis * 30
            reversePos = pos - axis * 30
            track.append(Sequence(LerpPosInterval(cloud[0], 10, newPos), LerpPosInterval(cloud[0], 20, reversePos), LerpPosInterval(cloud[0], 10, pos)))

        return track

    def loadCloud(self, version, radius, zOffset):
        self.notify.debug('loadOnePlatform version=%d' % version)
        cloud = NodePath('cloud-%d%d' % (radius, version))
        cloudModel = loader.loadModel('phase_5.5/models/estate/bumper_cloud')
        cc = cloudModel.copyTo(cloud)
        colCube = cc.find('**/collision')
        colCube.setName('cloudSphere-0')
        dTheta = 2.0 * math.pi / self.numClouds
        cloud.reparentTo(self.cloudOrigin)
        axes = [Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, 1)]
        cloud.setPos(radius * math.cos(version * dTheta), radius * math.sin(version * dTheta), 4 * random.random() + zOffset)
        cloud.setScale(4.0)
        cloud.setTag('number', '%d%d' % (radius, version))
        self.clouds.append([cloud, random.choice(axes)])

    def loadSkyCollision(self):
        plane = CollisionPlane(Plane(Vec3(0, 0, -1), Point3(0, 0, 200)))
        plane.setTangible(0)
        planeNode = CollisionNode('sky_collision')
        planeNode.addSolid(plane)
        self.cloudOrigin.attachNewNode(planeNode)

    def loadCloudPlatforms(self):
        self.cloudOrigin = self.geom.attachNewNode('cloudOrigin')
        #self.cloudOrigin.setZ(30)
        self.cloudOrigin.setPos(221, -61, 60)
        self.loadSkyCollision()
        self.numClouds = 24
        for i in range(self.numClouds):
            self.loadCloud(i, 100, 0)

        for i in range(self.numClouds):
            self.loadCloud(i, 120, 30)

        for i in range(self.numClouds):
            self.loadCloud(i, 100, 60)

        self.cloudOrigin.stash()

    def __cleanupCloudFadeInterval(self):
        if hasattr(self, 'cloudFadeInterval'):
            self.cloudFadeInterval.pause()
            self.cloudFadeInterval = None
        return

    def fadeClouds(self):
        self.__cleanupCloudFadeInterval()
        self.cloudOrigin.setTransparency(1)
        self.cloudFadeInterval = self.cloudOrigin.colorInterval(0.5, Vec4(1, 1, 1, int(self.cloudOrigin.isStashed())), blendType='easeIn')
        if self.cloudOrigin.isStashed():
            self.cloudOrigin.setColor(Vec4(1, 1, 1, 0))
            self.setCloudSwitch(1)
        else:
            self.cloudFadeInterval = Sequence(self.cloudFadeInterval, Func(self.setCloudSwitch, 0), Func(self.cloudOrigin.setTransparency, 0))
        self.cloudFadeInterval.start()

    def setCloudSwitch(self, on):
        self.cloudSwitch = on
        if hasattr(self, 'cloudOrigin'):
            if on:
                self.cloudOrigin.unstash()
            else:
                self.cloudOrigin.stash()
