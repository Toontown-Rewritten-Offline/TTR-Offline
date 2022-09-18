from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectAI

class DistributedToonfestDayNightAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedToonfestDayNightAI")
