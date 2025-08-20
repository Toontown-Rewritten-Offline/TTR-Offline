from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from . import CogHQLoader
from toontown.toonbase import ToontownGlobals
from direct.gui import DirectGui
from toontown.toonbase import TTLocalizer
from toontown.toon import Toon
from direct.fsm import State
from toontown.coghq import BossbotHQExterior
from toontown.coghq import BossbotHQBossBattle
from toontown.coghq import BossbotOfficeExterior
from toontown.coghq import CountryClubInterior
from toontown.battle import BattleParticles
from panda3d.core import DecalEffect, TextEncoder
from direct.interval.LerpInterval import LerpHprInterval
from direct.interval.IntervalGlobal import *
import random
aspectSF = 0.7227

GEAR_INDEX = range(12)
GEYSER_INDEX = range(1, 5)
ACTIVE_GEYSERS = range(5)

class BossbotCogHQLoader(CogHQLoader.CogHQLoader):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossbotCogHQLoader')

    def __init__(self, hood, parentFSMState, doneEvent):
        CogHQLoader.CogHQLoader.__init__(self, hood, parentFSMState, doneEvent)
        self.fsm.addState(State.State('countryClubInterior', self.enterCountryClubInterior, self.exitCountryClubInterior, ['quietZone', 'cogHQExterior']))
        for stateName in ['start', 'cogHQExterior', 'quietZone']:
            state = self.fsm.getStateNamed(stateName)
            state.addTransition('countryClubInterior')

        self.cogHQExteriorModelPath = 'phase_12/models/bossbotHQ/CogGolfExterior'
        self.cogHQLobbyModelPath = 'phase_12/models/bossbotHQ/CogGolfLobby'
        self.musicFile = random.choice(['phase_12/audio/bgm/Bossbot_Entry_v1.ogg', 'phase_12/audio/bgm/Bossbot_Entry_v2.ogg', 'phase_12/audio/bgm/Bossbot_Entry_v3.ogg'])
        self.geom = None
        self.rain = None 
        self.rainRender = None
        self.rainSound = None
        self.activeGeysers = None
        self.geysers = []
        self.gearLerps = []
        return

    def load(self, zoneId):
        CogHQLoader.CogHQLoader.load(self, zoneId)
        Toon.loadBossbotHQAnims()

    def startRain(self):
        self.rain = BattleParticles.loadParticleFile('raindisk.ptf')
        self.rain.setPos(0, 0, 20)
        self.rainRender = self.geom.attachNewNode('rainRender')
        self.rainRender.setDepthWrite(0)
        self.rainRender.setBin('fixed', 1)
        self.rain.start(camera, self.rainRender)
        self.rainSound = base.loader.loadSfx('phase_12/audio/sfx/CHQ_rain_ambient.ogg')
        base.playSfx(self.rainSound, looping=1, volume=0.25)
        return

    def stopRain(self):
        if self.rain:
            self.rain.cleanup()
            self.rainSound.stop()

    def __fountainDamageTick(self, task):
        base.localAvatar.b_stun(ToontownGlobals.BossbotOilDamage)
        task.delayTime = 5.0
        return task.again

    def startFountainDamage(self, collision):
        taskMgr.add(self.__fountainDamageTick, 'oil-fountain-tick')

    def stopFountainDamage(self, collision):
        taskMgr.remove('oil-fountain-tick')

    def startCollisionDetection(self):
        self.accept('enterFountain_Geom:oil_trigger', self.startFountainDamage)
        self.accept('exitFountain_Geom:oil_trigger', self.stopFountainDamage)

    def stopCollisionDetection(self):
        taskMgr.remove('oil-fountain-tick')
        self.ignore('enterFountain_Geom:oil_trigger')
        self.ignore('exitFountain_Geom:oil_trigger')

    def unload(self):
        del self.rain
        del self.rainRender
        del self.rainSound
        del self.activeGeysers
        Toon.unloadBossbotHQAnims()
        CogHQLoader.CogHQLoader.unload(self)

    def unloadPlaceGeom(self):
        self.destroyGeysers()
        self.stopGearLoop()
        if self.geom:
            self.geom.removeNode()
            self.geom = None
        CogHQLoader.CogHQLoader.unloadPlaceGeom(self)
        return

    def loadPlaceGeom(self, zoneId):
        self.notify.info('loadPlaceGeom: %s' % zoneId)
        zoneId = zoneId - zoneId % 100
        self.notify.debug('zoneId = %d ToontownGlobals.BossbotHQ=%d' % (zoneId, ToontownGlobals.BossbotHQ))
        if zoneId == ToontownGlobals.BossbotHQ:
            self.geom = loader.loadModel(self.cogHQExteriorModelPath)
            gzLinkTunnel = self.geom.find('**/LinkTunnel1')
            gzLinkTunnel.setName('linktunnel_gz_17000_DNARoot')
            self.makeSigns()
            self.startGears()
            trigger = gzLinkTunnel.find('**/tunnel_sphere')
            trigger.setName('tunnel_trigger')
            bigcheeseFountainStatue = self.geom.find('**/Fountain_Geom:Big_Cheese') 
            bigcheeseEOTStatues = self.geom.find('**/ttr_bbhq_EOT:EOT_statues')
            self.makeGeysers()
        elif zoneId == ToontownGlobals.BossbotLobby:
            if config.GetBool('want-qa-regression', 0):
                self.notify.info('QA-REGRESSION: COGHQ: Visit BossbotLobby')
            self.notify.debug('cogHQLobbyModelPath = %s' % self.cogHQLobbyModelPath)
            self.geom = loader.loadModel(self.cogHQLobbyModelPath)
            self.makeGeysers()

        else:
            self.notify.warning('loadPlaceGeom: unclassified zone %s' % zoneId)
        CogHQLoader.CogHQLoader.loadPlaceGeom(self, zoneId) 

    def makeSigns(self):

        def makeSign(topStr, signStr, textId, scale = TTLocalizer.BCHQLsignText):
            top = self.geom.find('**/' + topStr)
            sign = top.find('**/' + signStr)
            locator = top.find('**/sign_origin')
            signText = DirectGui.OnscreenText(text=TextEncoder.upper(TTLocalizer.GlobalStreetNames[textId][-1]), font=ToontownGlobals.getSuitFont(), scale=scale, fg=(0, 0, 0, 1), parent=sign)
            signText.setPosHpr(locator, 0, -0.1, -0.25, 0, 0, 0)
            signText.setDepthWrite(0)

        makeSign('TunnelEntrance', 'Sign_2', 1000)
        makeSign('Gate_2', 'Sign_6', 10700)
        makeSign('Gate_3', 'Sign_3', 10600)
        makeSign('Gate_4', 'Sign_4', 10500)
        makeSign('GateHouse', 'Sign_5', 10200)
        makeSign('GateHouse_2', 'Sign_5', 10300, TTLocalizer.BCHQLofficeText)

    def makeGeysers(self):
        self.activeGeysers = []
        geyser = loader.loadModel('phase_12/models/bossbotHQ/ttr_m_ara_bbhq_geyser')
        for geyserSpot in self.geom.findAllMatches('**/geyser*').getPaths():
            geyser.copyTo(geyserSpot)
            geyser.setScale(0.0)

        for count in ACTIVE_GEYSERS:
            taskMgr.add(self.__makeGeyserIval, 'geyser-task-' + str(count))

        geyser.removeNode()

    def __makeGeyserIval(self, task):
        geyser = random.choice(self.geom.findAllMatches('**/ttr_m_ara_bbhq_geyser*').getPaths())
        while geyser in self.activeGeysers:
            geyser = random.choice(self.geom.findAllMatches('**/ttr_m_ara_bbhq_geyser*').getPaths())

        length = random.randint(5, 15)
        task.delayTime = length + 3
        scale = random.randint(5, 18) / 10

        def geyserIval(node, scale, length):
            count = 0
            length = random.randint(5, 12)
            geyserIval = Sequence()
            while count < length:
                geyserIval.append(node.scaleInterval(1.25, scale + 0.1, blendType='easeInOut'))
                geyserIval.append(node.scaleInterval(1.25, scale, blendType='easeInOut'))
                count += 2.5

            return geyserIval

        geyserSequence = Sequence(Func(self.activeGeysers.append, geyser), geyser.scaleInterval(1.5, scale, blendType='easeOut'), geyserIval(geyser, scale, length), geyser.scaleInterval(1.5, 0.0, blendType='easeIn'), Func(self.activeGeysers.remove, geyser))
        geyserSequence.start()
        return task.again

    def destroyGeysers(self):
        for count in ACTIVE_GEYSERS:
            taskMgr.remove('geyser-task-' + str(count))

        self.activeGeysers = []

    def startGears(self):
        parentId = ToontownGlobals.SPDynamic
        for top in self.geom.findAllMatches('**/Fountain_Geom:Top').getPaths():
            self.gearLerps.append(LerpHprInterval(top, 17, (0, 0, 0), (360, 0, 0)))
            base.cr.parentMgr.registerParent(parentId, top)
            parentId += 1

        for middle in self.geom.findAllMatches('**/Fountain_Geom:Middle').getPaths():
            self.gearLerps.append(LerpHprInterval(middle, 17, (0, 0, 0), (-360, 0, 0)))
            base.cr.parentMgr.registerParent(parentId, middle)
            parentId += 1

        for bottom in self.geom.findAllMatches('**/Fountain_Geom:Bottom').getPaths():
            self.gearLerps.append(LerpHprInterval(bottom, 17, (0, 0, 0), (360, 0, 0)))
            base.cr.parentMgr.registerParent(parentId, bottom)
            parentId += 1

        for lerp in self.gearLerps:
            lerp.loop()

        self.oilGeyser = loader.loadModel('phase_12/models/bossbotHQ/ttr_m_ara_bbhq_geyser')
        for nodeId in GEYSER_INDEX:
            geyserPoint = self.geom.find('**/Fountain_Geom:fountain_geyser' + str(nodeId))
            oilGeyser = self.oilGeyser.copyTo(geyserPoint)
            self.geysers.append(oilGeyser)

        self.startCollisionListener()

    def startCollisionListener(self):
        for colId in GEAR_INDEX:
            self.accept('enterFountain_Geom:gear_floor_coll' + str(colId), self.__handleOnFloor)
            self.accept('exitFountain_Geom:gear_floor_coll' + str(colId), self.__handleOffFloor)

    def stopGearLoop(self):
        if self.gearLerps:
            for lerp in self.gearLerps:
                lerp.finish()

            for geyser in self.geysers:
                geyser.removeNode()

            self.gearLerps = []
            for colId in GEAR_INDEX:
                base.cr.parentMgr.unregisterParent(ToontownGlobals.SPDynamic + colId)

            self.stopCollisionListener()

    def stopCollisionListener(self):
        for colId in GEAR_INDEX:
            self.ignore('enterFountain_Geom:gear_floor_coll' + str(colId))
            self.ignore('exitFountain_Geom:gear_floor_coll' + str(colId))

    def __handleOnFloor(self, collision):
        base.localAvatar.b_setParent(ToontownGlobals.SPDynamic + int(collision.getIntoNode().getName()[29:]))

    def __handleOffFloor(self, collision):
        base.localAvatar.b_setParent(ToontownGlobals.SPRender)

    def getExteriorPlaceClass(self):
        self.notify.debug('getExteriorPlaceClass')
        return BossbotHQExterior.BossbotHQExterior

    def getBossPlaceClass(self):
        self.notify.debug('getBossPlaceClass')
        return BossbotHQBossBattle.BossbotHQBossBattle

    def enterCogHQExterior(self, requestStatus):
        self.placeClass = self.getExteriorPlaceClass()
        self.enterPlace(requestStatus)
        self.hood.spawnTitleText(requestStatus['zoneId'])
        self.startRain()

    def exitCogHQExterior(self):
        self.stopRain()
        taskMgr.remove('titleText')
        self.hood.hideTitleText()
        self.exitPlace()
        self.placeClass = None
        return

    def enterCogHQLobby(self, requestStatus):
        self.hood.setWhiteFog()
        self.hood.startSky()
        CogHQLoader.CogHQLoader.enterCogHQLobby(self, requestStatus)
        self.startRain()

    def exitCogHQLobby(self):
        self.stopRain()
        self.hood.stopSky()
        self.hood.setNoFog()
        CogHQLoader.CogHQLoader.exitCogHQLobby(self)

    def enterCountryClubInterior(self, requestStatus):
        self.placeClass = CountryClubInterior.CountryClubInterior
        self.notify.info('enterCountryClubInterior, requestStatus=%s' % requestStatus)
        self.countryClubId = requestStatus['countryClubId']
        self.enterPlace(requestStatus)

    def exitCountryClubInterior(self):
        self.exitPlace()
        self.placeClass = None
        del self.countryClubId
        return
    
    def enterCogHQBossBattle(self, requestStatus):
        self.notify.debug('BossbotCogHQLoader.enterCogHQBossBattle')
        CogHQLoader.CogHQLoader.enterCogHQBossBattle(self, requestStatus)
        base.cr.forbidCheesyEffects(1)

    def exitCogHQBossBattle(self):
        self.notify.debug('BossbotCogHQLoader.exitCogHQBossBattle')
        CogHQLoader.CogHQLoader.exitCogHQBossBattle(self)
        base.cr.forbidCheesyEffects(0)
