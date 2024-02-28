from . import SuitDNA
from otp.ai.MagicWordGlobal import *
from direct.task import Task
from toontown.toonbase import ToontownGlobals
from random import random, randint, choice
import datetime
from direct.directnotify import DirectNotifyGlobal

# TODO: NewsManagerAI to properly announce invasions starting, invasions
# ending, and invasions currently in progress.
# All numbers/values in here are hard-coded. Maybe we should move them to
# ToontownGlobals or something?

class SuitInvasionManagerAI:
    """
    This is a very basic AI class to handle Suit Invasions in Toontown.
    This class doesn't need to do much, besides telling the suit planners
    when an invasion starts and stops.
    """

    notify = DirectNotifyGlobal.directNotify.newCategory('SuitInvasionManagerAI')

    def __init__(self, air):
        self.air = air
        self.invading = 0
        self.specialSuit = 0
        self.suitName = None
        self.numSuits = 0
        self.spawnedSuits = 0

        if config.GetBool('want-mega-invasions', False): # TODO - config for this
            # Mega invasion configuration.
            self.randomInvasionProbability = config.GetFloat('mega-invasion-probability', 0.4)
            self.megaInvasionCog = config.GetString('mega-invasion-cog-type', '')
            if not self.megaInvasionCog:
                raise AttributeError("No mega invasion cog specified, but mega invasions are on!")
            if self.megaInvasionCog not in SuitDNA.suitHeadTypes:
                raise AttributeError("Invalid cog type specified for mega invasion!")
            # Start ticking.
            taskMgr.doMethodLater(randint(1800, 5400), self.__randomInvasionTick, 'random-invasion-tick')

        elif config.GetBool('want-random-invasions', True):
            # Random invasion configuration.
            self.randomInvasionProbability = config.GetFloat('random-invasion-probability', 0.3)
            # Start ticking.
            taskMgr.doMethodLater(randint(1800, 5400), self.__randomInvasionTick, 'random-invasion-tick')

    def __randomInvasionTick(self, task=None):
        """
        Each hour, have a tick to check if we want to start an invasion in
        the current district. This works by having a random invasion
        probability, and each tick it will generate a random float between
        0 and 1, and then if it's less than or equal to the probablity, it
        will spawn the invasion.

        An invasion will not be started if there is an invasion already
        on-going.
        """
        # Generate a new tick delay.
        task.delayTime = randint(1800, 5400)
        if self.getInvading():
            # We're already running an invasion. Don't start a new one.
            self.notify.debug('Invasion tested but already running invasion!')
            return task.again
        if random() <= self.randomInvasionProbability:
            # We want an invasion!
            self.notify.debug('Invasion probability hit! Starting invasion.')
            # We want to test if we get a mega invasion or a normal invasion.
            # Take the mega invasion probability and test it. If we get lucky
            # a second time, spawn a mega invasion, otherwise spawn a normal
            # invasion.
            if config.GetBool('want-mega-invasions', False) and random() <= self.randomInvasionProbability:
                # N.B.: randomInvasionProbability = mega invasion probability.
                suitName = self.megaInvasionCog
                numSuits = randint(2000, 15000)
                specialSuit = random.choice([0, 0, 0, 1, 2])
            else:
                suitName = choice(SuitDNA.suitHeadTypes)
                numSuits = randint(1500, 5000)
                specialSuit = False
            self.startInvasion(suitName, numSuits, specialSuit)
        return task.again

    def getInvading(self):
        """ Tell the caller if an invasion is currently running. """
        return self.invading

    def stopInvasion(self, task=None):
        """
        Stop an invasion on the current AI. This is called either by
        self.__checkInvasionOver or by magic word.
        """
        if not self.getInvading():
            # We're not currently invading, go away!
            return False
        # TODO: Fix once we have NewsManagerAI working.
        self.air.newsManager.sendUpdate('setInvasionStatus', [
            ToontownGlobals.SuitInvasionEnd, self.suitName,
            self.numSuits, self.specialSuit
        ])
        # Remove the invasion timeout.
        if task is not None:
            task.remove()
        else:
            taskMgr.remove('invasion-timeout')
        self.specialSuit = 0
        self.numSuits = 0
        self.spawnedSuits = 0
        self.invading = 0
        self.suitName = None
        self.__spAllCogsSupaFly()

    def __checkInvasionOver(self):
        """ Test if the current invasion has created all the suits. """
        if self.spawnedSuits >= self.numSuits:
            self.stopInvasion()

    def getInvadingCog(self):
        """ Tell the caller the current cog type invading and if they are a skelecog or v2.0 """
        self.spawnedSuits += 1
        self.__checkInvasionOver()
        return (self.suitName, self.specialSuit)

    def __spAllCogsSupaFly(self):
        """ Tell all SuitPlanners to get rid of the current cogs. """
        for sp in list(self.air.suitPlanners.values()):
            sp.flySuits()

    def startInvasion(self, suitName='f', numSuits=1000, specialSuit=0):
        """
        Start an invasion on the current AI. This can be invoked by anything, such
        as a toon summoning an invasion, or an admin manually starting an
        invasion via a magic word.
        """
        if self.getInvading():
            # We're already invading Toontown, go away!
            return False
        self.invading = True
        self.spawnedSuits = 0
        self.suitName = suitName
        self.numSuits = numSuits
        self.specialSuit = specialSuit
        # Tell all the client's that an invasion has started via the NewsManager.
        self.air.newsManager.sendUpdate('setInvasionStatus', [
            ToontownGlobals.SuitInvasionBegin, self.suitName,
            self.numSuits, self.specialSuit
        ])
        # If the cogs aren't defeated in a set amount of time, the invasion will
        # simply timeout. This was calculated by judging that 1000 cogs should
        # take around 20 minutes, becoming 1.2 seconds per cog.
        # We added in a bit of a grace period, making it 1.5 seconds per cog, or 25 minutes.
        timePerCog = config.GetFloat('invasion-time-per-cog', 1.5)
        taskMgr.doMethodLater(timePerCog * numSuits, self.stopInvasion, 'invasion-timeout')
        self.__spAllCogsSupaFly()
        return True

@magicWord(types=[str, str, int, int], category=CATEGORY_OVERRIDE)
def invasion(cmd, name='f', num=1000, specialSuit = 0):
    """ Spawn an invasion on the current AI if one doesn't exist. """
    invMgr = simbase.air.suitInvasionManager
    if cmd == 'start':
        if invMgr.getInvading():
            return "There is already an invasion on the current AI!"
        if not name in SuitDNA.suitHeadTypes:
            return "This cog does not exist!"
        invMgr.startInvasion(name, num, specialSuit)
    elif cmd == 'stop':
        if not invMgr.getInvading():
            return "There is no invasion on the current AI!"
        invMgr.stopInvasion()
    else:
        return "You didn't enter a valid command! Commands are ~invasion start or stop."
