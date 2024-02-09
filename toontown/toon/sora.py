from otp.avatar import Avatar
from otp.avatar.Avatar import teleportNotify
from . import ToonDNA
from direct.showbase.InputStateGlobal import inputState
from direct.task.Task import Task
from toontown.suit import SuitDNA
from direct.actor import Actor
from .ToonHead import *
from panda3d.core import *
from panda3d.direct import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals
from otp.otpbase import OTPLocalizer
from toontown.toonbase import TTLocalizer
import random
from toontown.effects import Wake
from . import TTEmote
from otp.avatar import Emote
from . import Motion
from toontown.hood import ZoneUtil
from toontown.battle import SuitBattleGlobals
from otp.otpbase import OTPGlobals
from toontown.effects import DustCloud
from direct.showbase.PythonUtil import Functor
from toontown.distributed import DelayDelete
from otp.nametag.NametagConstants import *
from . import AccessoryGlobals
import types
import importlib

soraActor = None

def hideToon():
    global soraActor
    if soraActor:
        originalToon = base.localAvatar.getGeomNode()
        originalToon.hide()

def createSoraActor():
    global soraActor
    if soraActor is None:
        soraActor = Actor.Actor('/Users/ryandemboski/Desktop/GitHub/TTPorkheffley/resources/phase_3/models/char/sora_model.bam',
                                {'idle': '/Users/ryandemboski/Desktop/GitHub/TTPorkheffley/resources/phase_3/models/char/sora-idle.bam',
                                'walk': '/Users/ryandemboski/Desktop/GitHub/TTPorkheffley/resources/phase_3/models/char/sora-walk.bam',
                                'dance': '/Users/ryandemboski/Desktop/GitHub/TTPorkheffley/resources/phase_3/models/char/sora-dance.bam',
                                'swim': '/Users/ryandemboski/Desktop/GitHub/TTPorkheffley/resources/phase_3/models/char/sora-swim.bam'})
        soraActor.setBlend(frameBlend=config.ConfigVariableBool('want-smooth-animations', False).getValue())
        soraActor.setPos(0, 0, 0)
        soraActor.setScale(0.03)
        soraActor.setH(180)

        soraActor.loop('idle')
    return soraActor

def removeSoraActor():
    global soraActor
    if soraActor:
        soraActor.cleanup()
        soraActor.removeNode()
        soraActor = None

def makeSoraSwim():
    global soraActor
    if soraActor:
        soraActor.loop('swim')

def makeSoraStopSwim():
    global soraActor
    if soraActor:
        soraActor.loop('walk')

def makeSoraStopSwimAndIdle():
    global soraActor
    if soraActor:
        soraActor.loop('idle')

def makeSoraDance():
    global soraActor
    if soraActor:
        soraActor.loop('dance')

def makeSoraStopDance():
    global soraActor
    if soraActor:
        soraActor.loop('idle')