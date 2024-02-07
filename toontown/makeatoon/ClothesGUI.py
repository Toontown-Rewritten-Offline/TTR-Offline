from panda3d.core import *
from toontown.toon import ToonDNA
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.makeatoon.MakeAToonGlobals import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.makeatoon import ShuffleButton
import random
CLOTHES_MAKETOON = 0
CLOTHES_TAILOR = 1
CLOTHES_CLOSET = 2

class ClothesGUI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, type, doneEvent, swapEvent = None):
        StateData.StateData.__init__(self, doneEvent)
        self.type = type
        self.toon = None
        self.swapEvent = swapEvent
        self.gender = '?'
        self.girlInShorts = 0
        self.swappedTorso = 0
        return

    def load(self):
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        guiRArrowUp = self.gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowRollover = self.gui.find('**/tt_t_gui_mat_arrowUp')
        guiRArrowDown = self.gui.find('**/tt_t_gui_mat_arrowDown')
        guiRArrowDisabled = self.gui.find('**/tt_t_gui_mat_arrowDisabled')
        shuffleFrame = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleFrame2 = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleFrame2.setColor(0, 100, 30)
        shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = self.gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        self.parentFrame = DirectFrame(relief=DGG.RAISED, pos=(0.98, 0, 0.416), frameColor=(1, 0, 0, 0))

        #Let's use the old GUI for closets.
        if self.type == CLOTHES_CLOSET:
            self.shirtFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.4), hpr=(0, 0, 3), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.ClothesShopShirt, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
            self.topLButton = DirectButton(parent=self.shirtFrame, relief=None, image=(shuffleArrowUp,
             shuffleArrowDown,
             shuffleArrowRollover,
             shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapTop, extraArgs=[-1])
            self.topRButton = DirectButton(parent=self.shirtFrame, relief=None, image=(shuffleArrowUp,
             shuffleArrowDown,
             shuffleArrowRollover,
             shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapTop, extraArgs=[1])
            self.bottomFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.65), hpr=(0, 0, -2), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.ColorShopToon, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
            self.bottomLButton = DirectButton(parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
             shuffleArrowDown,
             shuffleArrowRollover,
             shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapBottom, extraArgs=[-1])
            self.bottomRButton = DirectButton(parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
             shuffleArrowDown,
             shuffleArrowRollover,
             shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapBottom, extraArgs=[1])
            self.parentFrame.hide()
            self.shuffleFetchMsg = 'ClothesShopShuffle'
            self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)
            return   

            
        self.shirtStyleFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame2, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.073), hpr=(0, 0, 3), scale=1.2, frameColor=(1, 1, 1, 1), text=TTLocalizer.ClothesShopShirtsStyle, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.shirtStyleLButton = DirectButton(parent=self.shirtStyleFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapTopStyle, extraArgs=[-1])
        self.shirtStyleRButton = DirectButton(parent=self.shirtStyleFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapTopStyle, extraArgs=[1])         
        
        
        self.shirtFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.3), hpr=(0, 0, 3), scale=0.9, frameColor=(1, 1, 1, 1), text= TTLocalizer.ClothesShopShirtsColor, text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.topLButton = DirectButton(parent=self.shirtFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapTopColor, extraArgs=[-1])
        self.topRButton = DirectButton(parent=self.shirtFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapTopColor, extraArgs=[1]) 
        
        
        self.bottomStyleFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.525), hpr=(0, 0, -2), scale=1.2, frameColor=(1, 1, 1, 1), text='', text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.bottomStyleLButton = DirectButton(parent=self.bottomStyleFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapBottomStyle, extraArgs=[-1])
        self.bottomStyleRButton = DirectButton(parent=self.bottomStyleFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapBottomStyle, extraArgs=[1])
        
        
        self.bottomFrame = DirectFrame(parent=self.parentFrame, image=shuffleFrame, image_scale=halfButtonInvertScale, relief=None, pos=(0, 0, -0.752), hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1), text='', text_scale=0.0575, text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1))
        self.bottomLButton = DirectButton(parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonScale, image1_scale=halfButtonHoverScale, image2_scale=halfButtonHoverScale, pos=(-0.2, 0, 0), command=self.swapBottomColor, extraArgs=[-1])
        self.bottomRButton = DirectButton(parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
         shuffleArrowDown,
         shuffleArrowRollover,
         shuffleArrowDisabled), image_scale=halfButtonInvertScale, image1_scale=halfButtonInvertHoverScale, image2_scale=halfButtonInvertHoverScale, pos=(0.2, 0, 0), command=self.swapBottomColor, extraArgs=[1])
        self.parentFrame.hide()
        self.shuffleFetchMsg = 'ClothesShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)
        return

    def unload(self):
        self.gui.removeNode()
        del self.gui
        self.parentFrame.destroy()
        self.shirtFrame.destroy()
        self.bottomFrame.destroy()
        self.topLButton.destroy()
        self.topRButton.destroy()
        self.bottomLButton.destroy()
        self.bottomRButton.destroy()
        if self.type != CLOTHES_CLOSET:          
            self.shirtStyleFrame.destroy()
            self.shirtStyleLButton.destroy()
            self.shirtStyleRButton.destroy()
            self.bottomStyleFrame.destroy()
            self.bottomStyleLButton.destroy()
            self.bottomStyleRButton.destroy()
            del self.shirtStyleFrame
            del self.shirtStyleLButton
            del self.shirtStyleRButton
            del self.bottomStyleFrame
            del self.bottomStyleLButton
            del self.bottomStyleRButton        
        del self.parentFrame
        del self.shirtFrame
        del self.bottomFrame
        del self.topLButton
        del self.topRButton
        del self.bottomLButton
        del self.bottomRButton
        self.shuffleButton.unload()
        self.ignore('MAT-newToonCreated')

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()

    def enter(self, toon):
        self.notify.debug('enter')
        base.disableMouse()
        self.toon = toon
        self.setupScrollInterface()
        if not self.type == CLOTHES_TAILOR:
            currTop = (self.toon.style.topTex,
             self.toon.style.topTexColor,
             self.toon.style.sleeveTex,
             self.toon.style.sleeveTexColor)
            currTopStyle = (self.toon.style.topTex, self.toon.style.sleeveTex)
            currTopIndex = self.tops.index(currTop)
            self.swapTop(currTopIndex - self.topChoice)
            currBottom = (self.toon.style.botTex, self.toon.style.botTexColor)
            currBottomStyle = (self.toon.style.botTex)
            currBottomIndex = self.bottoms.index(currBottom)
            self.swapBottom(currBottomIndex - self.bottomChoice)
        choicePool = [self.tops, self.bottoms]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeClothes)
        self.acceptOnce('MAT-newToonCreated', self.shuffleButton.cleanHistory)

    def exit(self):
        try:
            del self.toon
        except:
            self.notify.warning('ClothesGUI: toon not found')

        self.hideButtons()
        self.ignore('enter')
        self.ignore('next')
        self.ignore('last')
        self.ignore(self.shuffleFetchMsg)

    def setupButtons(self):
        self.girlInShorts = 0
        if self.gender == 'f':
            if self.type == CLOTHES_CLOSET:            
                if self.bottomChoice == -1:
                    botTex = self.bottoms[0][0]
                else:
                    botTex = self.bottoms[self.bottomChoice][0]
                if ToonDNA.GirlBottoms[botTex][1] == ToonDNA.SHORTS:
                    self.girlInShorts = 1
            else:
                if self.bottomStyleChoice == -1:
                    botTex = self.bottoms[0][0]
                else:
                    botTex = self.bottoms[self.bottomChoice][0]
                if ToonDNA.GirlBottoms[botTex][1] == ToonDNA.SHORTS:
                    self.girlInShorts = 1            
        if self.toon.style.getGender() == 'm':
            if self.type == CLOTHES_CLOSET:
                self.bottomFrame['text'] = TTLocalizer.ClothesShopShorts
            else:
                self.bottomStyleFrame['text'] = TTLocalizer.ClothesShopShortsStyle
                self.bottomFrame['text'] = TTLocalizer.ClothesShopShortsColor
        else:
            if self.type == CLOTHES_CLOSET:
                self.bottomFrame['text'] = TTLocalizer.ClothesShopBottoms
            else:
                self.bottomStyleFrame['text'] = TTLocalizer.ClothesShopBottomsStyle
                self.bottomFrame['text'] = TTLocalizer.ClothesShopBottomsColor
        self.acceptOnce('last', self.__handleBackward)
        self.acceptOnce('next', self.__handleForward)
        return None

    def swapTop(self, offset):
        length = len(self.tops)
        self.topChoice += offset
        if self.topChoice <= 0:
            self.topChoice = 0
        self.updateScrollButtons(self.topChoice, length, 0, self.topLButton, self.topRButton)
        if self.topChoice < 0 or self.topChoice >= len(self.tops) or len(self.tops[self.topChoice]) != 4:
            self.notify.warning('topChoice index is out of range!')
            return None
        self.toon.style.topTex = self.tops[self.topChoice][0]
        self.toon.style.topTexColor = self.tops[self.topChoice][1]
        self.toon.style.sleeveTex = self.tops[self.topChoice][2]
        self.toon.style.sleeveTexColor = self.tops[self.topChoice][3]
        self.toon.generateToonClothes()
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if self.bottomChoice <= 0:
            self.bottomChoice = 0
        self.updateScrollButtons(self.bottomChoice, length, 0, self.bottomLButton, self.bottomRButton)
        if self.bottomChoice < 0 or self.bottomChoice >= len(self.bottoms) or len(self.bottoms[self.bottomChoice]) != 2:
            self.notify.warning('bottomChoice index is out of range!')
            return None
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def swapTopStyle(self, offset):
        length = len(self.topStyles)
        self.topStyleChoice += offset
        if self.topStyleChoice <= 0:
            self.topStyleChoice = 0
        self.updateScrollButtons(self.topStyleChoice, length, 0, self.shirtStyleLButton, self.shirtStyleRButton)
        if self.topStyleChoice < 0 or self.topStyleChoice >= length:
        #if self.topStyleChoice < 0 or self.topStyleChoice >= len(self.topStyles) or len(self.topStyles[self.topStyleChoice]) != 4:
            self.notify.warning('topChoice index is out of range!')
            return None
        self.toon.style.topTex = self.topStyles[self.topStyleChoice][0]
        self.toon.style.sleeveTex = self.topStyles[self.topStyleChoice][1]
        colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        colorLength = len(colors)
        if self.topColorChoice < 0 or self.topColorChoice >= colorLength:
            self.topColorChoice = colorLength - 1
        self.updateScrollButtons(self.topColorChoice, colorLength, 0, self.topLButton, self.topRButton)
        self.toon.style.topTexColor = colors[self.topColorChoice][0]
        self.toon.style.sleeveTexColor = colors[self.topColorChoice][1]
        self.toon.generateToonClothes()
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')        
        
    def swapTopColor(self, offset):
        self.topColorChoice += offset    
        colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        length = len(colors)
        if self.topColorChoice <= 0:
            self.topColorChoice = 0
        self.updateScrollButtons(self.topColorChoice, length, 0, self.topLButton, self.topRButton)
        if self.topColorChoice < 0 or self.topColorChoice >= length:
            self.notify.warning('topChoice index is out of range!')
            self.topColorChoice = len(colors)
            self.updateScrollButtons(self.topColorChoice, length, 0, self.topLButton, self.topRButton)
        self.toon.style.topTexColor = colors[self.topColorChoice][0]
        self.toon.style.sleeveTexColor = colors[self.topColorChoice][1]
        self.toon.generateToonClothes()
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def swapBottomStyle(self, offset):
        length = len(self.bottomStyles)
        self.bottomStyleChoice += offset
        if self.bottomStyleChoice <= 0:
            self.bottomStyleChoice = 0
        self.updateScrollButtons(self.bottomStyleChoice, length, 0, self.bottomStyleLButton, self.bottomStyleRButton)
        if self.bottomStyleChoice < 0 or self.bottomStyleChoice >= length:
        #if self.topStyleChoice < 0 or self.topStyleChoice >= len(self.topStyles) or len(self.topStyles[self.topStyleChoice]) != 4:
            self.notify.warning('bottomChoice index is out of range!')
            return None
        self.toon.style.botTex = self.bottomStyles[self.bottomStyleChoice]
        colors = ToonDNA.getBottomColors(self.gender, self.bottomStyles[self.bottomStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        colorLength = len(colors)
        if self.bottomColorChoice < 0 or self.bottomColorChoice >= colorLength:
            self.bottomColorChoice = colorLength - 1
        self.updateScrollButtons(self.bottomColorChoice, colorLength, 0, self.bottomLButton, self.bottomRButton)
        self.toon.style.botTexColor = colors[self.bottomColorChoice]      
        #colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        #self.toon.style.topTexColor = colors[self.topColorChoice][0]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')
        
    def swapBottomColor(self, offset):
        self.bottomColorChoice += offset    
        colors = ToonDNA.getBottomColors(self.gender, self.bottomStyles[self.bottomStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        length = len(colors)
        if self.bottomColorChoice <= 0:
            self.bottomColorChoice = 0
        self.updateScrollButtons(self.bottomColorChoice, length, 0, self.bottomLButton, self.bottomRButton)
        if self.bottomColorChoice < 0 or self.bottomColorChoice >= length:
            self.notify.warning('bottomColor choice index is out of range!')
            self.bottomColorChoice = len(colors)
            self.updateScrollButtons(self.bottomColorChoice, length, 0, self.bottomLButton, self.bottomRButton)            
        self.toon.style.botTexColor = colors[self.bottomColorChoice]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def updateScrollButtons(self, choice, length, startTex, lButton, rButton):
        if choice >= length - 1:
            rButton['state'] = DGG.DISABLED
        else:
            rButton['state'] = DGG.NORMAL
        if choice <= 0:
            lButton['state'] = DGG.DISABLED
        else:
            lButton['state'] = DGG.NORMAL

    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def resetClothes(self, style):
        if self.toon:
            self.toon.style.makeFromNetString(style.makeNetString())
            if self.swapEvent != None and self.swappedTorso == 1:
                self.toon.swapToonTorso(self.toon.style.torso, genClothes=0)
                self.toon.generateToonClothes()
                self.toon.loop('neutral', 0)
        return

    def changeClothes(self):
        self.notify.debug('Entering changeClothes')
        newChoice = self.shuffleButton.getCurrChoice()
        if newChoice[0] in self.tops:
            newTopIndex = self.tops.index(newChoice[0])
        else:
            newTopIndex = self.topChoice
        if newChoice[1] in self.bottoms:
            newBottomIndex = self.bottoms.index(newChoice[1])
        else:
            newBottomIndex = self.bottomChoice
        oldTopIndex = self.topChoice
        oldBottomIndex = self.bottomChoice
        self.swapTop(newTopIndex - oldTopIndex)
        self.swapBottom(newBottomIndex - oldBottomIndex)

    def getCurrToonSetting(self):
        return [self.tops[self.topChoice], self.bottoms[self.bottomChoice]]