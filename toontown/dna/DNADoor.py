from .DNANode import DNANode
from .DNAParser import *
from . import DNAUtil
from panda3d.core import *

class DNADoor(DNANode):
    TAG = 'door'
    PARENTS = ['landmark_building']

    def __init__(self, code):
        DNANode.__init__(self, 'door')

        self.code = code

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0,0,0), (0,0,0), (1,1,1))
        doorNodePath.setColor(color, 0)
        doorFlat = doorNodePath.find('door_*_flat')
        doorFlat.flattenStrong()
        #doorFlat.setDepthOffset(1) # Can cause building shadows to not properly show up on the doors...
        doorFlat.setEffect(DecalEffect.make())

        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.flattenStrong()
        leftHole.setName('doorFrameHoleLeft')
        leftHole.wrtReparentTo(doorFlat, 0)
        leftHole.hide()
        leftHole.setColor((0, 0, 0, 1), 0)

        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.flattenStrong()
        rightHole.setName('doorFrameHoleRight')
        rightHole.wrtReparentTo(doorFlat, 0)
        rightHole.hide()
        rightHole.setColor((0, 0, 0, 1), 0)

        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.flattenStrong()
        leftDoor.setName('leftDoor')
        leftDoor.hide()
        leftDoor.wrtReparentTo(parentNode, 0)
        leftDoor.setColor(color, 0)

        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.flattenStrong()
        rightDoor.setName('rightDoor')
        rightDoor.hide()
        rightDoor.wrtReparentTo(parentNode, 0)
        rightDoor.setColor(color, 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_%s' % block)

        doorNodePath.flattenMedium()

    def _makeNode(self, storage, parent):
        frontNode = parent.find('**/*building*_front')
        if frontNode.isEmpty():
            frontNode = parent.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = storage.findNode(self.code)
        if node == None:
            #raise DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
            #TODO: error message here
            pass
        doorNode = node.copyTo(frontNode, 0)
        origin = parent.find('**/*door_origin')
        origin.node().setPreserveTransform(ModelNode.PTNet)
        self.setupDoor(doorNode, parent, origin, storage,
          DNAUtil.getBlockFromName(parent.getName()), self.getColor())
        return doorNode

registerElement(DNADoor)
