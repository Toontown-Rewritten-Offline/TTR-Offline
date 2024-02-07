from . import Quests
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownBattleGlobals
import random

class QuestManagerAI:
    notify = directNotify.newCategory('QuestManagerAI')
    def __init__(self, air):
        self.air = air

    def __testPercentage(self, percentage):
        """
        Generate a random number and test it against the percentage chance specified.

        Returns TRUE or FALSE, depending on if the generated number is within the
        percentage specified.
        """
        return random.randint(1, 100) <= percentage

    def __incrementQuestProgress(self, quest):
        """
        Increment the supplied quest's progress by 1.
        """
        quest[4] += 1

    def __toonQuestsList2Quests(self, quests):
        return [Quests.getQuest(x[0]) for x in quests]

    def removeBetaQuest(self, toon, rpcmethod):
        toon.b_setWantBetaKeyQuest(0)
        dg = self.air.dclassesByName['AccountAI'].aiFormatUpdate(
            'BETA_KEY_QUEST', toon.DISLid, toon.DISLid,
            self.air.ourChannel, 0
        )
        self.air.send(dg)
        self.air.rpc.call(rpcmethod, webAccId=toon.getWebAccountId())

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToons):
        """
        Called in battleExperience to alert the quest system that a toon has
        killed some cogs.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.CogQuest):
                # It's a cog quest!
                for suit in suitsKilled:
                    # N.B.: This will iterate once if True, none if False.
                    # If it's a newbie quest, it will return an integer rather than a
                    # boolean, and will iterate x times.
                    for x in range(quest.doesCogCount(toon.getDoId(), suit, zoneId, activeToons)):
                        # Give us credit for this cog. If this a newbie quest, it will
                        # give us multiple credit(s), depending on how many newbies were
                        # in the battle.
                       self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def recoverItems(self, toon, suitsKilled, zoneId):
        """
        Called in battleExperience to alert the quest system that a toon should
        test for recovered items.

        Returns a tuple of two lists:
            Index 0: a list of recovered items.
            Index 1: a list of unrecovered items.
        """
        recovered, notRecovered = ([] for i in range(2))
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                isComplete = quest.getCompletionStatus(toon, toon.quests[index])
                if isComplete == Quests.COMPLETE:
                    # This quest is complete, skip.
                    continue
                # It's a quest where we need to recover an item!
                if quest.isLocationMatch(zoneId):
                    # We're in the correct area to recover the item, woo!
                    if quest.getHolder() == Quests.Any or quest.getHolderType() in ['type', 'track', 'level']:
                        for suit in suitsKilled:
                            if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                                # Test if the task has already been completed.
                                # If it has, we don't need to iterate through the cogs anymore.
                                break
                            # Here comes the long IF statement...
                            if (quest.getHolder() == Quests.Any) \
                            or (quest.getHolderType() == 'type' and quest.getHolder() == suit['type']) \
                            or (quest.getHolderType() == 'track' and quest.getHolder() == suit['track']) \
                            or (quest.getHolderType() == 'level' and quest.getHolder() <= suit['level']):
                                progress = toon.quests[index][4] & pow(2, 16) - 1 # This seems to be the Disne
                                completion = quest.testRecover(progress)
                                if completion[0]:
                                    # We win! We got the item from the cogs. :)
                                    recovered.append(quest.getItem())
                                    self.__incrementQuestProgress(toon.quests[index])
                                else:
                                    # Tough luck, maybe next time.
                                    notRecovered.append(quest.getItem())
        toon.updateQuests()
        return (recovered, notRecovered)

    def toonKilledBuilding(self, toon, track, difficulty, floors, zoneId, activeToons):
        """
        This method is called whenever a toon defeats a cog building.
        N.B: This is called once for each toon that defeated the building.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.BuildingQuest):
                # This quest is a building quest, time to see if it counts towards
                # our progress!
                if quest.isLocationMatch(zoneId):
                    # We defeated the building in the correct zone, and the building counts!
                    if quest.getBuildingTrack() == Quests.Any or quest.getBuildingTrack() == track:
                        if floors >= quest.getNumFloors():
                            # This building has more (or equal to) the number of floors we need.
                            for x in range(quest.doesBuildingCount(toon.getDoId(), activeToons)):
                                # Works the same as Cog Quests. Increment by one if it's a
                                # normal quest, or by the amount of newbies if it's a
                                # newbie quest.
                                self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def toonKilledCogdo(self, toon, difficulty, floors, zoneId, activeToons):
        pass

    def toonRecoveredCogSuitPart(self, toon, zoneId, toonList):
        pass

    def toonDefeatedFactory(self, toon, factoryId, activeToonVictors):
        """
        This method is called whenever a toon defeats a Sellbot HQ factory.
        N.B: This is called once for each toon that defeated the factory.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FactoryQuest):
                # Cool, it's a factory quest! Does it count?
                for x in range(quest.doesFactoryCount(toon.getDoId(), factoryId, activeToonVictors)):
                    # Woo, this counts towards our quest progress!
                    # Increment by the amount of credit we deserve.
                    self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def toonDefeatedMint(self, toon, mintId, activeToonVictors):
        """
        This method is called whenever a toon defeats a Cashbot HQ mint.
        N.B: This is called once for each toon that defeated the mint.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.MintQuest):
                # Oh lookie here, a mint quest! I love me some Polos.
                for x in range(quest.doesMintCount(toon.getDoId(), mintId, activeToonVictors)):
                    # Nom nom nom nom, progress!
                    self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def toonDefeatedStage(self, toon, stageId, activeToonVictors):
        pass

    def toonRodeTrolleyFirstTime(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.TrolleyQuest):
                self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()
        
    def toonCalledClarabelle(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.PhoneQuest):
                self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def completeQuest(self, toon, questId):
        """
        This is called whenever a toon completes a single quest in a toontask.

        So far, this currently toons them up and removes the quest from their
        quest list, although it may be needed for more in the future.
        """
        toon.toonUp(toon.getMaxHp())
        toon.removeQuest(questId)

    def giveReward(self, toon, rewardId):
        """
        This is called when a toon completes a whole toontask.

        This grabs the reward from Quests via rewardId and issues the reward
        to the toon.
        """
        reward = Quests.getReward(rewardId)
        if reward:
            reward.sendRewardAI(toon)

    def npcGiveQuest(self, npc, toon, questId, rewardId, toNpcId, storeReward=False):
        """
        This is called when an NPC wants to assign a quest to the toon.
        """
        rewardId = Quests.transformReward(rewardId, toon)
        # If non-zero, this indicates this is the first quest in the whole ToonTask.
        # This means we want to store the reward in the toons setRewardHistory.
        finalReward = rewardId if storeReward else 0
        progress = 0
        toon.addQuest((questId, npc.getDoId(), toNpcId, rewardId, progress), finalReward)
        # Tell the NPC that we assigned this quest to the given toon.
        npc.assignQuest(toon.getDoId(), questId, rewardId, toNpcId)

    def requestInteract(self, toonId, npc):
        toon = self.air.doId2do.get(toonId)
        if not toon:
            # TODO: Flag suspicious. They shouldn't have got this far.
            return

        # Check if the toon has any quests to turn in.
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = toon.quests[index]
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete != Quests.COMPLETE:
                # This quest isn't complete, skip.
                continue
            # If we're in the Toontorial, move to the next step.
            if toonId in list(self.air.tutorialManager.avId2fsm.keys()):
                self.air.tutorialManager.avId2fsm[toonId].demand('Tunnel')
            # Take away gags if it's a DeliverGagQuest.
            if isinstance(quest, Quests.DeliverGagQuest):
                track, level = quest.getGagType()
                toon.inventory.setItem(track, level, toon.inventory.numItem(track, level) - quest.getNumGags())
                toon.b_setInventory(toon.inventory.makeNetString())
            # Check if the ToonTask has more quests to complete.
            nextQuest = Quests.getNextQuest(questId, npc, toon)
            if nextQuest == (Quests.NA, Quests.NA):
                # No more quests in the current ToonTask!
                if isinstance(quest, Quests.TrackChoiceQuest):
                    # TrackTrainingRewards are a little different, as we now
                    # have to display the gag track selection menu.
                    npc.presentTrackChoice(toonId, questId, quest.getChoices())
                    return
                # This function is pretty weird... not sure why it's even here...
                # But I'll include it just in case... (TMS says: "idk about this
                # one, maybe a single quest can have different rewards?")
                rewardId = Quests.getAvatarRewardId(toon, questId)
                npc.completeQuest(toonId, questId, rewardId)
                self.completeQuest(toon, questId)
                self.giveReward(toon, rewardId)
                return
            else:
                # We have another quest to go, sigh.
                self.completeQuest(toon, questId)
                nextQuestId = nextQuest[0]
                nextRewardId = Quests.getFinalRewardId(questId, 1)
                nextToNpcId = nextQuest[1]
                self.npcGiveQuest(npc, toon, nextQuestId, nextRewardId, nextToNpcId)
                return

        # We had no quests to hand in, maybe they want to take out a new ToonTask?
        if len(self.__toonQuestsList2Quests(toon.quests)) >= toon.getQuestCarryLimit():
            # Nope, they already have the maximum amount of concurring quests they
            # can carry. Reject them.
            self.notify.debug("Rejecting toonId %d because their quest inventory is full." % toonId)
            npc.rejectAvatar(toonId)
            return

        # Are we in the Toontorial?
        if toonId in list(self.air.tutorialManager.avId2fsm.keys()):
            # Are we speaking to Tom?
            if toon.getRewardHistory()[0] == 0:
                self.npcGiveQuest(npc, toon, 101, Quests.findFinalRewardId(101)[0], Quests.getQuestToNpcId(101), storeReward=True) # FIXME please, i have no idea if this is correct
                self.air.tutorialManager.avId2fsm[toonId].demand('Battle')
                return

        # Are they eligible for a tier upgrade?
        tier = toon.getRewardHistory()[0]
        if Quests.avatarHasAllRequiredRewards(toon, tier):
            # They have all the rewards needed for the next tier.
            if not Quests.avatarWorkingOnRequiredRewards(toon):
                # Check to make sure they are not on the LOOPING_FINAL_TIER
                if tier != Quests.LOOPING_FINAL_TIER:
                    tier += 1

                # Set the tier
                toon.b_setRewardHistory(tier, [])
            else:
                # They're eligible for a tier upgrade, but haven't finished all
                # of their required ToonTasks yet.
                self.notify.debug("Rejecting toonId %d because they are still working on their current tier." % toonId)
                npc.rejectAvatarTierNotDone(toonId)
                return

        # Time to give them a list of "suitable" tasks!
        suitableQuests = Quests.chooseBestQuests(tier, npc, toon)
        if not suitableQuests:
            # Uh oh! There's no suitable quests for them at the moment... reject.
            self.notify.debug("Rejecting toonId %d because there are no quests available!" % toonId)
            npc.rejectAvatar(toonId)
            return

        # Tell the NPC to select some quests from the generated list.
        npc.presentQuestChoice(toonId, suitableQuests)
        return

    def avatarCancelled(self, toonId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon decided to cancel the interaction.
        """
        # SECURITY TODO: Implement this!
        pass

    def avatarChoseQuest(self, toonId, npc, questId, rewardId, toNpcId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon has chosen a quest from the list supplied.
        """
        toon = self.air.doId2do.get(toonId)
        if not toon:
            # TODO: Flag suspicious. They shouldn't have got this far.
            return
        self.notify.debug("toonId %d chose quest %d with rewardId %d to hand to npcId %d." % (toonId, questId, rewardId, toNpcId))
        if rewardId == 5000:
            # If they take out the quest, we need to tell the web server that they took it
            # out and also tell the CSMUD not to issue any other toons with the quest for
            # the current session (via the Account object's BETA_KEY_QUEST field).
            self.removeBetaQuest(toon, 'lockBetaKey')
        self.npcGiveQuest(npc, toon, questId, rewardId, toNpcId, storeReward=True)

    def avatarChoseTrack(self, toonId, npc, questId, trackId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon has decided on the new track that they want to train for.

        This is a special moment for any toon, as it determines how they
        will play the game for the rest of their time at TTR. :D
        """
        toon = self.air.doId2do.get(toonId)
        if not toon:
            # TODO: Flag suspicious. They shouldn't have got this far.
            return
        self.notify.debug("toonId %d chose trackId %d to train." % (toonId, trackId))
        if trackId in [ToontownBattleGlobals.THROW_TRACK, ToontownBattleGlobals.SQUIRT_TRACK]:
            # Better stop hackers, or our own stupidity.
            self.notify.warning("toonId %s attempted to select trackId %d, which is a default track!" % (toonId, trackId))
            # Yes this is suspicious, because it should be impossible.
            self.air.writeServerEvent('suspicious', avId=toonId, issue='QMAI.avatarChoseTrack Attempted to train trackId %d, which is a default track!' % trackId)
            return
        rewardId = 401 + trackId
        npc.completeQuest(toonId, questId, rewardId)
        self.completeQuest(toon, questId)
        self.giveReward(toon, rewardId)

    def toonMadeFriend(self, toon, otherToon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FriendQuest):
                self.__incrementQuestProgress(toon.quests[index])
        toon.updateQuests()

    def toonFished(self, toon, zoneId):
        """
        This method is called by the FishManagerAI whenever a toon catches
        a fish. This checks for any "fishing" quests that are in progress,
        and determines if they caught any items.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                # Well, this is a quest where we have to recover an item...
                if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                    # Task is already complete. Check if we have any other
                    # quests that we need to fish for.
                    continue
                if quest.isLocationMatch(zoneId):
                    # Well we're in the right zone!
                    if quest.getHolder() == Quests.AnyFish:
                        # Bazinga! This is a fishing quest!
                        progress = toon.quests[index][4] & pow(2, 16) - 1 # This seems to be the Disney way
                        completion = quest.testRecover(progress)
                        if completion[0]:
                            # We got lucky, dave! We caught the item!
                            self.__incrementQuestProgress(toon.quests[index])
                            toon.updateQuests()
                            # Since we caught an item already, there's no
                            # point in checking the other quests as we can
                            # only catch one item at a time via fishing.
                            return quest.getItem()
        # Nope, no fishing quests, or we're out of luck. Too bad.
        return 0

    def hasTailorClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                return True

        return False

    def removeClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = toon.quests[index]
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                toon.removeQuest(questId)
                return True

        return False
