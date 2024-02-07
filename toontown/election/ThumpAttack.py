# Embedded file name: toontown.election.ThumpAttack
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from otp.ai.MagicWordGlobal import *
from toontown.toonbase import ToontownGlobals
from toontown.effects.ShakeCamera import ShakeCamera
from . import SafezoneInvasionGlobals

class ThumpAttack(NodePath, DirectObject):
    SPEED = 10.0
    RANGE = SafezoneInvasionGlobals.MoveShakerRadius
    FADE_TIME = 0.2
    INNER_RADIUS = 0.95
    SHAKE_INTENSITY = 90.0
    cm = CardMaker('thump_geom')
    cm.setFrame(-1, 1, -1, 1)

    def __init__(self, callback):
        NodePath.__init__(self, 'thump')
        DirectObject.__init__(self)
        self.geom = self.attachNewNode(self.cm.generate())
        self.geom.setP(-90)
        self.geom.setTransparency(1)
        self.geom.setDepthWrite(0)
        self.geom.setDepthTest(0)
        self.geom.setBin('shadow', 0)
        self.geom.setTexture(loader.loadTexture('phase_4/maps/shockwave.jpg', 'phase_4/maps/shockwave_a.rgb'))
        self.collisionName = 'thumpCollide-%d' % id(self)
        self.collision = self.attachNewNode(CollisionNode(self.collisionName))
        csphere = CollisionSphere(0, 0, 0, 1)
        csphere.setTangible(0)
        self.collision.node().addSolid(csphere)
        self.collision.node().setIntoCollideMask(ToontownGlobals.WallBitmask)
        self.callback = callback

    def start(self):
        spreadTime = self.RANGE / self.SPEED
        interval = Sequence(Parallel(LerpScaleInterval(self, spreadTime, self.RANGE, startScale=0), Sequence(Wait(spreadTime - self.FADE_TIME), LerpColorScaleInterval(self, self.FADE_TIME, (1, 1, 1, 0)))), Func(self.cleanup))
        offset = base.localAvatar.getPos(render) - self.getPos(render)
        intensity = self.SHAKE_INTENSITY / offset.lengthSquared()
        shake = ShakeCamera(intensity)
        shake.start()
        interval.start()
        self.accept('enter' + self.collisionName, self.__handleCollide)
        self.accept('again' + self.collisionName, self.__handleCollide)

    def __handleCollide(self, ce):
        offset = base.localAvatar.getPos(self) - Point3(0, 0, 0)
        if offset.lengthSquared() < self.INNER_RADIUS * self.INNER_RADIUS:
            return
        if getattr(base.localAvatar.controlManager.currentControls, 'isAirborne', 0):
            return
        self.ignoreAll()
        self.callback()

    def cleanup(self):
        self.ignoreAll()
        self.removeNode()


@magicWord(category=CATEGORY_DEBUG)
def doThump():
    """Plays a 'thump attack' effect in front of your current position."""
    thump = ThumpAttack(lambda : base.localAvatar.setSystemMessage(0, 'Gotcha!'))
    thump.setPos(spellbook.getInvoker(), 0, 5, 0)
    thump.reparentTo(render)
    thump.start()