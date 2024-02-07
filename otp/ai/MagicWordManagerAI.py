from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from otp.ai.MagicWordGlobal import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("MagicWordManagerAI")

    def sendMagicWord(self, word, targetId, execute):
        invokerId = self.air.getAvatarIdFromSender()

        invoker = self.air.doId2do.get(invokerId)
        if not invoker:
            self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', ['missing invoker'])
            return

        if invoker.getAdminAccess() < MINIMUM_MAGICWORD_ACCESS:
            self.air.writeServerEvent('suspicious', avId=invokerId, issue='Attempted to issue magic word: %s' % word)
            dg = PyDatagram()
            dg.addServerHeader(self.GetPuppetConnectionChannel(invokerId), self.air.ourChannel, CLIENTAGENT_EJECT)
            dg.addUint16(126)
            dg.addString('Magic Words are reserved for administrators only!')
            self.air.send(dg)
            return

        target = self.air.doId2do.get(targetId)
        if not target:
            self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', ['missing target'])
            return
        
        if execute:
            response = spellbook.process(invoker, target, word)
            if response[0]:
                self.sendUpdateToAvatarId(invokerId, 'sendMagicWordResponse', [response[0]])
                print(response)
        else:
            response = ('Client MW executed.',)
            
        from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
        targetAccess = 0 if not isinstance(target, DistributedPlayerAI) else target.getAdminAccess()

        self.air.writeServerEvent('magic-word',
                                  invokerId=invokerId, invokerAccess=invoker.getAdminAccess(),
                                  targetId=targetId, targetAccess=targetAccess,
                                  word=word, response=response[0])
