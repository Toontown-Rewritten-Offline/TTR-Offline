import os
import sys
import time
import atexit
import subprocess

from direct.task.Task import Task
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer

ASTRON_EXCEPTION_MSG = ':AstronInternalRepository(warning): INTERNAL-EXCEPTION: '
ASTRON_DONE_MSG = 'Event Logger: Opened new log.'
UBERDOG_DONE_MSG = ':AstronInternalRepository: Done.'
AI_DONE_MSG = ':AstronInternalRepository: District is now ready.'
PYTHON_TRACEBACK_MSG = 'Traceback (most recent call last):'


class DedicatedServer:
    notify = DirectNotifyGlobal.directNotify.newCategory('DedicatedServer')

    def __init__(self, localServer=False):
        self.notify.info('Starting DedicatedServer.')
        self.localServer = localServer

        self.mongoProcess = None
        self.astronProcess = None
        self.uberDogProcess = None
        self.aiProcess = None

        self.mongoLog = None
        self.astronLog = None
        self.uberDogLog = None
        self.aiLog = None

        self.uberDogInternalExceptions = []
        self.aiInternalExceptions = []

        self.notify.setInfo(True)

    def start(self):
        # Register self.killProcesses with atexit in the event of a hard exit,
        # so that the server processes are killed if they're running.
        atexit.register(self.killProcesses)

        if self.localServer:
            self.notify.info('Starting local server...')
        else:
            self.notify.info('Starting dedicated server...')

        if config.ConfigVariableBool('auto-start-server', True).getValue() and not self.localServer:
            self.notify.error("You are trying to start the server manually, but auto-start-server is enabled!\n"
                                "You do not need to run this file offline, the server will start for you.")

        if config.ConfigVariableBool('want-mongo-client', False).getValue():
            taskMgr.add(self.startAstronMongo, 'startAstronMongo')
        else:
            taskMgr.add(self.startAstronYAML, 'startAstronYAML')

    def openAstronProcess(self, astronConfig):
        if sys.platform == 'win32':
            self.astronProcess = subprocess.Popen('astron/astrond.exe --loglevel info %s' % astronConfig,
                                                  stdin=self.astronLog, stdout=self.astronLog, stderr=self.astronLog)
        elif sys.platform == 'darwin':
            self.astronProcess = subprocess.Popen('astron/astrondmac --loglevel info %s' % astronConfig,
                                                  stdin=self.astronLog, stdout=self.astronLog, stderr=self.astronLog, shell=True)
        elif sys.platform in ['linux', 'linux2']:
            self.astronProcess = subprocess.Popen('astron/astrondlinux --loglevel info %s' % astronConfig,
                                                  stdin=self.astronLog, stdout=self.astronLog, stderr=self.astronLog)

    def startAstronYAML(self, task):
        self.notify.info('Starting Astron with YAML...')

        # Create and open the log file to use for Astron.
        astronLogFile = self.generateLog('astron')
        self.astronLog = open(astronLogFile, 'a')
        self.notify.info('Opened new Astron log: %s' % astronLogFile)

        # Use the Astron config file based on the database.
        astronConfig = config.ConfigVariableString('astron-config-path', 'astron/config/astrond-yaml.yml').getValue()

        # Start Astron process.
        self.openAstronProcess(astronConfig)
        # Setup a Task to start the UberDOG process when Astron is done.
        taskMgr.add(self.startUberDog, 'startUberDog')

    def startAstronMongo(self, task):
        self.notify.info('Starting Astron with MongoDB...')

        # Start MongoDB Process.
        if sys.platform == 'win32':
            self.mongoProcess = subprocess.Popen('astron\\mongo\\Server\\5.0\\bin\\mongod.exe --dbpath astron\\mongo\\astrondb --logpath astron\\mongo\\logs\\mongodb.log --logappend --storageEngine wiredTiger')
        else:
            # Other os
            self.mongoProcess = subprocess.Popen('./astron/mongo/Server/5.0/bin/mongod --dbpath astron/mongo/astrondb --logpath astron/mongo/logs/mongodb.log --logappend --storageEngine wiredTiger')
        # Create and open the log file to use for Astron.
        astronLogFile = self.generateLog('astron')
        self.astronLog = open(astronLogFile, 'a')
        self.notify.info('Opened new Astron log: %s' % astronLogFile)

        if config.ConfigVariableBool('auto-start-server', True).getValue():
            gameServicesDialog['text'] = OTPLocalizer.CRLoadingGameServices + '\n\n' + OTPLocalizer.CRLoadingGameServicesAstron

        # Use the Astron config file based on the database.
        astronConfig = config.ConfigVariableString('astron-config-path', 'astron/config/astrond-mongo.yml').getValue()

        # Start Astron process.
        self.openAstronProcess(astronConfig)
        # Setup a Task to start the UberDOG process when Astron is done.
        taskMgr.add(self.startUberDog, 'startUberDog')

    def startUberDog(self, task):
        # Check if Astron is ready through the log.
        astronLogFile = self.astronLog.name
        astronLog = open(astronLogFile)
        astronLogData = astronLog.read()
        astronLog.close()
        if ASTRON_DONE_MSG not in astronLogData:
            # Astron has not started yet. Rerun the task.
            return task.again

        # Astron has started
        if config.ConfigVariableBool('want-mongo-client', False).getValue():
            self.notify.info('MongoDB started successfully!')
        self.notify.info('Astron started successfully!')

        ''' UberDOG '''
        self.notify.info('Starting UberDOG server...')

        # Create and open the log file to use for UberDOG.
        uberDogLogFile = self.generateLog('uberdog')
        self.uberDogLog = open(uberDogLogFile, 'a')
        self.notify.info('Opened new UberDOG log: %s' % uberDogLogFile)

        # Setup UberDOG arguments.
        if __debug__:
            if sys.platform == 'win32':
                uberDogArguments = '%s -m toontown.uberdog.ServiceStartUD' % open('PPYTHON_PATH').read()
            else:
                uberDogArguments = 'python3 -m toontown.uberdog.ServiceStartUD'

        else:
            if sys.platform == 'win32':
                uberDogArguments = 'TTRPEngine.exe --uberdog'
            else:
                uberDogArguments = 'TTRPEngine --uberdog'

        if config.ConfigVariableBool('auto-start-server', True).getValue():
            gameServicesDialog['text'] = OTPLocalizer.CRLoadingGameServices + '\n\n' + OTPLocalizer.CRLoadingGameServicesUberdog

        # Start UberDOG process.
        if sys.platform == 'win32':
            self.uberDogProcess = subprocess.Popen(uberDogArguments, stdin=self.uberDogLog, stdout=self.uberDogLog, stderr=self.uberDogLog)
        else:
            self.uberDogProcess = subprocess.Popen(uberDogArguments, stdin=self.uberDogLog, stdout=self.uberDogLog, stderr=self.uberDogLog, shell=True)
        # Start the AI process when UberDOG is done.
        taskMgr.add(self.startAI, 'startAI')

        # Once started, we can end this task.
        return task.done

    def startAI(self, task):
        # Check if UberDOG is ready through the log.
        uberDogLogFile = self.uberDogLog.name
        uberDogLog = open(uberDogLogFile)
        uberDogLogData = uberDogLog.read()
        uberDogLog.close()
        if UBERDOG_DONE_MSG not in uberDogLogData:
            # UberDOG has not started yet. Rerun the task.
            return task.again

        # UberDOG has started
        self.notify.info('UberDOG started successfully!')

        ''' AI '''
        self.notify.info('Starting AI server...')

        # Create and open the log file to use for AI.
        aiLogFile = self.generateLog('ai')
        self.aiLog = open(aiLogFile, 'a')
        self.notify.info('Opened new AI log: %s' % aiLogFile)

        # Setup AI arguments.
        if __debug__:
            if sys.platform == 'win32':
                aiArguments = '%s -m toontown.ai.ServiceStartAI' % open('PPYTHON_PATH').read()
            else:
                aiArguments = 'python3 -m toontown.ai.ServiceStartAI'
        else:
            if sys.platform == 'win32':
                aiArguments = 'TTRPEngine.exe --ai'
            else:
                aiArguments = 'TTRPEngine --ai'

        if config.ConfigVariableBool('auto-start-server', True).getValue():
            gameServicesDialog['text'] = OTPLocalizer.CRLoadingGameServices + '\n\n' + OTPLocalizer.CRLoadingGameServicesAI

        # Start AI process.
        if sys.platform == 'win32':
            self.aiProcess = subprocess.Popen(aiArguments, stdin=self.aiLog, stdout=self.aiLog, stderr=self.aiLog)
        else:
            self.aiProcess = subprocess.Popen(aiArguments, stdin=self.aiLog, stdout=self.aiLog, stderr=self.aiLog, shell=True)
        # Send a message to note the server has started.
        taskMgr.add(self.serverStarted, 'serverStarted')

        # Once started, we can end this task.
        return task.done

    def serverStarted(self, task):
        # Check if the AI is ready through the log.
        aiLogFile = self.aiLog.name
        aiLog = open(aiLogFile)
        aiLogData = aiLog.read()
        aiLog.close()
        if AI_DONE_MSG not in aiLogData:
            # AI has not started yet. Rerun the task.
            return task.again

        # AI has started
        self.notify.info('AI started successfully!')

        # Every aspect of the server has started. Let's finish with the done message.
        self.notify.info('Server now ready. Have fun on Toontown Rewritten Private!')
        if self.localServer:
            messenger.send('localServerReady')

        # Setup a Task to check if the server has crashed.
        taskMgr.add(self.checkForCrashes, 'checkForCrashes')

        # Otherwise, we can end this task.
        return task.done

    def checkForCrashes(self, task):
        # Check if the UberDOG server has crashed.
        uberDogLogFile = self.uberDogLog.name
        uberDogLog = open(uberDogLogFile)
        uberDogLogData = uberDogLog.read().split('\n')
        uberDogLog.close()
        for i in range(len(uberDogLogData)):
            lineNum = (len(uberDogLogData) - 1) - i
            line = uberDogLogData[lineNum]
            if PYTHON_TRACEBACK_MSG in line:
                prevLineNum = (len(uberDogLogData) - 1) - (i + 1)
                prevLine = uberDogLogData[prevLineNum]
                if ASTRON_EXCEPTION_MSG in prevLine:
                    if prevLineNum not in self.uberDogInternalExceptions:
                        self.uberDogInternalExceptions.append(prevLineNum)
                        self.notify.warning('An internal exception has occurred in the UberDOG server: %s' % line[len(
                            ASTRON_EXCEPTION_MSG):])
                else:
                    # The UberDOG server has crashed!
                    self.killProcesses()
                    self.notify.error("The UberDOG server has crashed, you will need to restart your server."
                                      "\n\nIf this problem persists, please report the bug and provide "
                                      "them with your most recent log from the \"logs/uberdog\" folder.")
            elif ASTRON_EXCEPTION_MSG in line:
                if lineNum not in self.uberDogInternalExceptions:
                    self.uberDogInternalExceptions.append(lineNum)
                    self.notify.warning('An internal exception has occurred in the UberDOG server: %s' % line[
                                                                                         len(ASTRON_EXCEPTION_MSG):])

        # Check if the AI server has crashed.
        aiLogFile = self.aiLog.name
        aiLog = open(aiLogFile)
        aiLogData = aiLog.read().split('\n')
        aiLog.close()
        for i in range(len(aiLogData)):
            lineNum = (len(aiLogData) - 1) - i
            line = aiLogData[lineNum]
            if PYTHON_TRACEBACK_MSG in line:
                prevLineNum = (len(aiLogData) - 1) - (i + 1)
                prevLine = aiLogData[prevLineNum]
                if ASTRON_EXCEPTION_MSG in prevLine:
                    if prevLineNum not in self.aiInternalExceptions:
                        self.aiInternalExceptions.append(prevLineNum)
                        self.notify.warning('An internal exception has occurred in the AI server: %s' % line[
                                                                                        len(ASTRON_EXCEPTION_MSG):])
                else:
                    # The AI server has crashed!
                    self.killProcesses()
                    self.notify.error("The AI server has crashed, you will need to restart your server."
                                      "\n\nIf this problem persists, please report the bug and provide "
                                      "them with your most recent log from the \"logs/ai\" folder.")
            elif ASTRON_EXCEPTION_MSG in line:
                if lineNum not in self.aiInternalExceptions:
                    self.aiInternalExceptions.append(lineNum)
                    self.notify.warning('An internal exception has occurred in the AI server: %s' % line[len(ASTRON_EXCEPTION_MSG):])

        # Keep running this Task if the server has not crashed.
        return task.again

    def killProcesses(self):
        # Terminate server processes in reverse order of how they were started, starting with the AI.
        if self.aiProcess:
            self.aiProcess.terminate()

        # Next is UberDOG.
        if self.uberDogProcess:
            self.uberDogProcess.terminate()

        # Next is Astron.
        if self.astronProcess:
            self.astronProcess.terminate()

        # And lastly, MongoDB
        if config.ConfigVariableBool('want-mongo-client', False).getValue():
            if self.mongoProcess:
                self.astronProcess.terminate()

    @staticmethod
    def generateLog(logPrefix):
        ltime = 1 and time.localtime()
        logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000, ltime[1], ltime[2],
                                                   ltime[3], ltime[4], ltime[5])

        if not os.path.exists('logs/'):
            os.mkdir('logs/')

        if not os.path.exists('logs/%s/' % logPrefix):
            os.mkdir('logs/%s/' % logPrefix)

        logFile = 'logs/%s/%s-%s.log' % (logPrefix, logPrefix, logSuffix)

        return logFile
