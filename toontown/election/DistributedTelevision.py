from direct.distributed.DistributedObject import DistributedObject
from panda3d.core import *
from direct.interval.IntervalGlobal import *
from toontown.battle import BattleProps

class DistributedTelevision(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.generate(self)

        # Load the TV, and give it a nice idle animation.
        # This will probably be moved somewhere else once we get it into the scripted sequence
        self.tv = loader.loadModel('phase_4/models/events/election_tv')
        self.tv.reparentTo(render)
        self.tv.setPosHprScale(87.85, -0.25, 22.0, 270.0, 0.0, 0.0, 1.5, 1.5, 1.5)

        self.tvIdle = Sequence(
            self.tv.posInterval(2.5, (87.85, -0.25, 21.0), blendType='easeInOut'),
            self.tv.posInterval(2.5, (87.85, -0.25, 22.0), blendType='easeInOut'),
        )

        self.prop = BattleProps.globalPropPool.getProp('propeller')
        propJoint = self.tv.find('**/topSphere')
        self.prop.reparentTo(propJoint)
        self.prop.loop('propeller', fromFrame=0, toFrame=8)
        self.prop.setPos(0, 1, 2)
        self.prop.setScale(2.0, 1.5, 1.0)

        self.tvIdle.loop()

        #begin the meme
        media_file = Filename('movie.ogv')
        if media_file:
            self.tex = MovieTexture("name")
            success = self.tex.read(media_file)

            self.sound = loader.loadSfx(media_file)
            # Synchronize the video to the sound.
            self.tex.synchronizeTo(self.sound)

            ts = self.tv.find('**/screen').findTextureStage('*')
            self.tv.find('**/screen').setTexture(ts, self.tex, 1)
            #self.tv.find('**/screen').setTexScale(ts, 1.2, 1.2)
            self.tv.find('**/screen').setTexOffset(ts, -0.2, -0.13)
            #self.tv.find('**/screen').setTexHpr(ts, 1, 0, 0)

            self.sound.setLoop(1)
            self.sound.play()

    def unload(self):
        self.tvIdle.finish()
        self.tv.removeNode()
        self.sound.stop()
        self.tex.unsynchronize()
        self.tex.stop()
        del self.tvIdle
        del self.tv
        del self.sound
        del self.tex

    def delete(self):
        self.unload()
        DistributedObject.delete(self)