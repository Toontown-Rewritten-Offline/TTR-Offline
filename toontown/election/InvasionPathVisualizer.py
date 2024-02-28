# Embedded file name: toontown.election.InvasionPathVisualizer
from panda3d.core import *
from otp.ai.MagicWordGlobal import *
from .InvasionPathDataAI import pathfinder
LINK_HEIGHT = 6

class InvasionPathVisualizer(NodePath):

    def __init__(self, pathfinder):
        NodePath.__init__(self, 'viz')
        self.pathfinder = pathfinder
        self.showVertices()
        self.showBorders()
        self.showEdges()

    def showVertices(self):
        segs = LineSegs('vertices')
        segs.setColor(0, 0, 1)
        for vertex in self.pathfinder.vertices:
            x, y = vertex.pos
            segs.moveTo(x, y, -20)
            segs.drawTo(x, y, 20)

        self.attachNewNode(segs.create())

    def showBorders(self):
        segs = LineSegs('borders')
        segs.setColor(0, 1, 0)
        for border in self.pathfinder.borders:
            x1, y1, x2, y2 = border
            segs.moveTo(x1, y1, LINK_HEIGHT + 0.1)
            segs.drawTo(x2, y2, LINK_HEIGHT + 0.1)

        self.attachNewNode(segs.create())

    def showEdges(self):
        segs = LineSegs('edges')
        segs.setColor(1, 0, 0)
        for vertex in self.pathfinder.vertices:
            x1, y1 = vertex.pos
            for neighbor in vertex.getNeighbors():
                x2, y2 = neighbor.pos
                segs.moveTo(x1, y1, LINK_HEIGHT)
                segs.drawTo(x2, y2, LINK_HEIGHT)

        self.attachNewNode(segs.create())


invasionViz = None

@magicWord()
def showInvasionPaths():
    global invasionViz
    invasionViz = InvasionPathVisualizer(pathfinder)
    invasionViz.reparentTo(render)
    return 'Showing invasion paths.'


@magicWord()
def hideInvasionPaths():
    if invasionViz == None:
        return 'No invasion paths to hide.'
    else:
        invasionViz.removeNode()
        return 'Hiding invasion paths.'


@magicWord()
def planPathFrom():
    base.localAvatar._planPos = base.localAvatar.getPos()
    return 'Set planned path "from".'


@magicWord()
def planPathTo():
    fromPos = getattr(base.localAvatar, '_planPos', None)
    if not fromPos:
        return 'No planFrom point set!'
    else:
        toPos = base.localAvatar.getPos()
        path = pathfinder.planPath((fromPos.getX(), fromPos.getY()), (toPos.getX(), toPos.getY()))
        if path is None:
            return 'Pathfinding failed -- no path exists.'
        segs = LineSegs('plannedPath')
        segs.setColor(1, 1, 0)
        segs.moveTo(fromPos.getX(), fromPos.getY(), LINK_HEIGHT - 0.1)
        for x, y in path:
            segs.drawTo(x, y, LINK_HEIGHT - 0.1)

        for np in render.findAllMatches('**/plannedPath'):
            np.removeNode()

        render.attachNewNode(segs.create())
        return 'Set planned path "to".'