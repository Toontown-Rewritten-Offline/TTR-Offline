from direct.distributed.DistributedObjectAI import DistributedObjectAI
from panda3d.core import *

class DistributedTelevisionAI(DistributedObjectAI):

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)