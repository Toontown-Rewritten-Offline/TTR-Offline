import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.rpc.RPCServer import RPCServer
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from .ToontownRPCHandler import *
import urllib

if config.GetBool('want-mongo-client', False):
    import pymongo

class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.notify.setInfo(True)

        if config.GetBool('want-mongo-client', False):
            url = config.GetString('mongodb-url', 'mongodb://localhost')
            replicaset = config.GetString('mongodb-replicaset', '')
            self.notify.info('MongoDB Client is enabled.')
            if replicaset:
                self.mongo = pymongo.MongoClient(url, replicaset=replicaset)
            else:
                self.mongo = pymongo.MongoClient(url)
            db = (urllib.parse.urlparse(url).path)[1:]
            self.mongodb = self.mongo[db]

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', False):
            self.rpcserver = RPCServer(ToontownRPCHandler(self))

        self.createGlobals()
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """
        self.csm = self.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.chatAgent = self.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER, 'ChatAgent')
        self.friendsManager = self.generateGlobalObject(OTP_DO_ID_TTR_FRIENDS_MANAGER, 'TTRFriendsManager')
        if config.GetBool('want-parties', True):
            # want-parties overrides config for want-GlobalPartyManagerUD
            self.globalPartyMgr = self.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        else:
            self.globalPartyMgr = None