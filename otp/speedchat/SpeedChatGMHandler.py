from panda3d.core import *
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer

class SpeedChatGMHandler(DirectObject.DirectObject):
    scStructure = None
    scList = {}

    def __init__(self):
        if SpeedChatGMHandler.scStructure == None:
            self.generateSCStructure()
        return

    def generateSCStructure(self):
        SpeedChatGMHandler.scStructure = [OTPLocalizer.PSCMenuGM]
        phraseCount = 0
        numGMCategories = config.ConfigVariableInt('num-gm-categories', 0).getValue()
        for i in range(0, numGMCategories):
            categoryName = config.ConfigVariableString('gm-category-%d' % i, '').getValue()
            if categoryName == '':
                continue
            categoryStructure = [categoryName]
            numCategoryPhrases = config.ConfigVariableInt('gm-category-%d-phrases' % i, 0).getValue()
            for j in range(0, numCategoryPhrases):
                phrase = config.ConfigVariableString('gm-category-%d-phrase-%d' % (i, j), '')
                if phrase != '':
                    idx = 'gm%d' % phraseCount
                    SpeedChatGMHandler.scList[idx] = phrase
                    categoryStructure.append(idx)
                    phraseCount += 1

            SpeedChatGMHandler.scStructure.append(categoryStructure)

        numGMPhrases = config.ConfigVariableInt('num-gm-phrases', 0).getValue()
        for i in range(0, numGMPhrases):
            phrase = config.ConfigVariableString('gm-phrase-%d' % i, '').getValue()
            if phrase != '':
                idx = 'gm%d' % phraseCount
                SpeedChatGMHandler.scList[idx] = phrase
                SpeedChatGMHandler.scStructure.append(idx)
                phraseCount += 1

    def getStructure(self):
        return SpeedChatGMHandler.scStructure

    def getPhrase(self, id):
        return SpeedChatGMHandler.scList[id]
