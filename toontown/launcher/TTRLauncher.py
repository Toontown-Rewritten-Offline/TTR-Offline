from panda3d.core import *
from direct.directnotify import DirectNotifyGlobal
from otp.launcher.LauncherBase import LauncherBase
from direct.task.TaskManagerGlobal import *
from direct.showbase.EventManagerGlobal import *
import os
import sys
import time
import tkinter as tk
from tkinter import Entry, Label, Button

class LogAndOutput:
    def __init__(self, orig, log):
        self.orig = orig
        self.log = log

    def write(self, str):
        self.log.write(str)
        self.log.flush()
        self.orig.write(str)
        self.orig.flush()

    def flush(self):
        self.log.flush()
        self.orig.flush()

class TTRLauncher(LauncherBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('ToontownDummyLauncher')

    def __init__(self):
        self.http = HTTPClient()

        self.logPrefix = 'ttr-'

        ltime = time.localtime()
        logSuffix = '%02d%02d%02d_%02d%02d%02d' % (ltime[0] - 2000,  ltime[1], ltime[2],
                                                   ltime[3], ltime[4], ltime[5])

        
        if not os.path.exists('logs/'):
            os.mkdir('logs/')
            self.notify.info('Made new directory to save logs.')
        
        logfile = os.path.join('logs', self.logPrefix + logSuffix + '.log')

        log = open(logfile, 'a')
        logOut = LogAndOutput(sys.stdout, log)
        logErr = LogAndOutput(sys.stderr, log)
        sys.stdout = logOut
        sys.stderr = logErr

    def getPlayToken(self):
        return self.getValue('TTR_PLAYCOOKIE')

    def getGameServer(self):
        return self.getValue('TTR_GAMESERVER')

    def setPandaErrorCode(self, code):
        pass

    def getGame2Done(self):
        return True

    def getLogFileName(self):
        return 'toontown'

    def getValue(self, key, default = None):
        return os.environ.get(key, default)

    def setValue(self, key, value):
        os.environ[key] = str(value)

    def getVerifyFiles(self):
        return config.ConfigVariableInt('launcher-verify', 0).getValue()

    def getTestServerFlag(self):
        return self.getValue('IS_TEST_SERVER', 0)

    def isDownloadComplete(self):
        return 1

    def isTestServer(self):
        return 0

    def getPhaseComplete(self, phase):
        return 1

    def startGame(self):
        from toontown.toonbase import ToontownStart

    def create_gui(self):
        gui = tk.Tk()
        gui.title("Toontown Porkheffley Launcher")

        playcookie_label = Label(gui, text="Username:")
        playcookie_label.grid(row=0, column=0, padx=10, pady=5)
        self.playcookie_entry = Entry(gui)
        self.playcookie_entry.grid(row=0, column=1, padx=10, pady=5)

        gameserver_label = Label(gui, text="Gameserver:")
        gameserver_label.grid(row=1, column=0, padx=10, pady=5)
        self.gameserver_entry = Entry(gui)
        self.gameserver_entry.grid(row=1, column=1, padx=10, pady=5)

        start_button = Button(gui, text="Start Game", command=self.openLauncher)
        start_button.grid(row=2, column=0, columnspan=2, pady=10)

        gui.mainloop()

    def openLauncher(self):
        playcookie = self.playcookie_entry.get()
        gameserver = self.gameserver_entry.get()

        self.setValue('TTR_PLAYCOOKIE', playcookie)
        self.setValue('TTR_GAMESERVER', gameserver)

        self.startGame()

if __name__ == "__main__":
    launcher = TTRLauncher()
    launcher.create_gui()