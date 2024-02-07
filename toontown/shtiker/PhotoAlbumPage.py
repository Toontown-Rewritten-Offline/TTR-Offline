from panda3d.core import *
from . import ShtikerPage
from . import ShtikerBook
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from toontown.toonbase import TTLocalizer
import os
import string
from toontown.toonbase import ToontownGlobals
from sys import platform

class PhotoAlbumPage(ShtikerPage.ShtikerPage):

    notify = DirectNotifyGlobal.directNotify.newCategory('PhotoAlbumPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.photos = {}
        self.selectedFileName = None
        self.selectedFilePath = None
        #TODO: Localizer support for screenshot storing and names
        self.installPath = os.getcwd()
        self.photoPath = TTLocalizer.ScreenshotPath
        self.photoIndex = 0
        return

    def load(self):
        if not os.path.exists(self.photoPath):
            os.mkdir(self.photoPath)
            self.notify.info('Made new directory to save screenshots.')
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.PhotoPageTitle, text_scale=0.1, pos=(0, 0, 0.6))
        self.pictureImage = loader.loadModel('phase_3.5/models/gui/photo_frame')
        self.pictureImage.setScale(0.2)
        self.pictureImage.setPos(0.44, 0, 0.25)
        self.pictureImage.reparentTo(self)
        self.pictureFg = self.pictureImage.find('**/fg')
        self.pictureFg.setColor(1, 1, 1, 0.1)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.pictureCaption = DirectLabel(parent=self, relief=None, text=TTLocalizer.PhotoPageAddName, text_scale=0.05, text_wordwrap=10, text_align=TextNode.ACenter, pos=(0.45, 0, -0.22))
        self.renameButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1, 1, 1), pos=(0.40, 0, -0.35), text=TTLocalizer.PhotoPageAddName, text_scale=0.06, text_pos=(0, -0.02), command=self.renameImage, state=DGG.DISABLED)
        self.directoryButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.3, 1, 1), pos=(0.46, 0, -0.50), text=TTLocalizer.PhotoPageDirectory, text_scale=0.06, text_pos=(0, -0.02), command=self.openPhotoDirectory, state=DGG.NORMAL)
        trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui')
        self.deleteButton = DirectButton(parent=self, image=(trashcanGui.find('**/TrashCan_CLSD'), trashcanGui.find('**/TrashCan_OPEN'), trashcanGui.find('**/TrashCan_RLVR')), text=('', TTLocalizer.AvatarChoiceDelete, TTLocalizer.AvatarChoiceDelete), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1), text_scale=0.1, text_pos=(0, -0.1), text_font=ToontownGlobals.getInterfaceFont(), textMayChange=0, relief=None, pos=(0.68, 0, -0.33), scale=0.4, state=DGG.DISABLED, command=self.deleteImage)
        guiButton.removeNode()
        trashcanGui.removeNode()
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.scrollList = DirectScrolledList(parent=self, relief=None, forceHeight=0.07, pos=(-0.5, 0, 0), incButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(1.3, 1.3, -1.3), incButton_pos=(0.08, 0, -0.60), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(1.3, 1.3, 1.3), decButton_pos=(0.08, 0, 0.52), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(-0.237, 0, 0.41), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(-0.05,
         0.66,
         -0.98,
         0.07), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=13, items=[])
        self.renamePanel = DirectFrame(parent=self, relief=None, pos=(0.45, 0, -0.45), image=DGG.getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.0, 1.0, 0.6), text=TTLocalizer.PhotoPageAddNamePanel, text_scale=0.06, text_pos=(0.0, 0.13))
        self.renameEntry = DirectEntry(parent=self.renamePanel, relief=DGG.SUNKEN, scale=0.06, pos=(-0.3, 0, 0), borderWidth=(0.1, 0.1), numLines=1, cursorKeys=1, frameColor=(0.8, 0.8, 0.5, 1), frameSize=(-0.2,
         10,
         -0.4,
         1.1), command=self.renameDialog)
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.bCancel = DirectButton(parent=self.renamePanel, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text=TTLocalizer.PhotoPageCancel, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.renameCancel)
        self.renamePanel.hide()
        self.deletePanel = DirectFrame(parent=self, relief=None, pos=(0.45, 0, -0.45), image=DGG.getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.0, 1.0, 0.6), text='', text_scale=0.06, text_pos=(0.0, 0.13))
        self.dOk = DirectButton(parent=self.deletePanel, image=(buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr')), relief=None, text=TTLocalizer.PhotoPageConfirm, text_scale=0.05, text_pos=(0.0, -0.1), pos=(-0.1, 0.0, -0.1), command=self.deleteConfirm)
        self.dCancel = DirectButton(parent=self.deletePanel, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text=TTLocalizer.PhotoPageCancel, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.1, 0.0, -0.1), command=self.deleteCancel)
        self.deletePanel.hide()
        self.errorPanel = DirectFrame(parent=self, relief=None, pos=(0.45, 0, -0.45), image=DGG.getDefaultDialogGeom(), image_color=ToontownGlobals.GlobalDialogColor, image_scale=(1.0, 1.0, 0.6), text='', text_wordwrap=16, text_scale=0.06, text_pos=(0.0, 0.13))
        self.bClose = DirectButton(parent=self.errorPanel, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), relief=None, text=TTLocalizer.PhotoPageClose, text_scale=0.05, text_pos=(0.0, -0.1), pos=(0.0, 0.0, -0.1), command=self.errorConfirm)       
        self.errorPanel.hide()
        self.scroll = loader.loadModel('phase_3/models/gui/toon_council').find('**/scroll')
        self.scroll.reparentTo(self)
        self.scroll.setPos(0.0, 1.0, 0.2)
        self.scroll.setScale(0.6, 0.6, 0.6)
        self.tip = DirectLabel(parent=self.scroll, relief=None, text=TTLocalizer.PhotoPageTutorial, text_scale=0.13, pos=(0.0, 0.0, 0.1), text_fg=(0.4, 0.3, 0.2, 1), text_wordwrap=18, text_align=TextNode.ACenter)
        self.leftArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), scale=(-1.0, 1.0, 1.0), pos=(0.15, 0, -0.21), command=self.prevPhoto)
        self.rightArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), pos=(0.75, 0, -0.21), command=self.nextPhoto)
        gui.removeNode()
        buttons.removeNode()
        return

    def unload(self):
        del self.title
        del self.scrollList
        del self.pictureImage
        del self.pictureFg
        del self.pictureCaption
        del self.deleteButton
        del self.renameButton
        del self.directoryButton
        del self.renamePanel
        del self.renameEntry
        del self.scroll
        del self.tip
        del self.errorPanel
        del self.bCancel
        del self.bClose
        del self.deletePanel
        del self.dOk
        del self.dCancel
        del self.leftArrow
        del self.rightArrow
        ShtikerPage.ShtikerPage.unload(self)

    def renameDialog(self, str):
        if os.path.isfile(self.photoPath + self.selectedFileName):
            separator = '_'
            validChars = string.letters + string.digits + ' -#&.,'
            str = [s for s in str if s in validChars]
            oldName = self.selectedFileName
            numUnders = oldName.count(separator)
            if numUnders == 0:
                newName = oldName[0:15] + separator + str + separator + oldName[14:]
            elif numUnders == 2:
                sp = oldName.split(separator)
                newName = sp[0] + separator + str + separator + sp[2]
            else:
                self.renameCleanup()
                return 0
            if str.isspace() or str == '':
                self.renameCancel()
            else:
                os.rename(self.photoPath + oldName, self.photoPath + newName)
                self.renameCleanup()
                self.updateScrollList()
                self.chosePhoto(newName)
            return 1
        else:
            self.renameCancel()
            self.errorPanel['text'] = 'Huh. It looks like this snapshot has been deleted or removed.'
            self.errorPanel.show()
            self.updateScrollList()

    def renameCancel(self):
        self.renameCleanup()

    def renameCleanup(self):
        self.renamePanel.hide()
        chatEntry = base.localAvatar.chatMgr.chatInputNormal.chatEntry
        chatEntry['backgroundFocus'] = self.oldFocus

    def renameImage(self):
        self.deleteCleanup()
        if self.getPhotoName(self.selectedFileName) == TTLocalizer.PhotoPageNoName:
            self.renameEntry.set('')
        else:
            self.renameEntry.set(self.getPhotoName(self.selectedFileName))
        self.renamePanel.show()
        chatEntry = base.localAvatar.chatMgr.chatInputNormal.chatEntry
        chatEntry['backgroundFocus'] = 0
        self.renameEntry['focus'] = 1
        self.notify.debug(self.selectedFileName)

    def deleteConfirm(self):
        if os.path.isfile(self.photoPath + self.selectedFileName):        
            os.remove(self.photoPath + self.selectedFileName)
            self.selectedFileName = None
            self.deleteCleanup()
            self.updateScrollList()
            return
        else:
            self.deleteCancel()
            self.errorPanel['text'] = 'Huh. It looks like this snapshot has already been deleted.'
            self.errorPanel.show()
            self.updateScrollList()

    def deleteCancel(self):
        self.deleteCleanup()

    def deleteCleanup(self):
        self.deletePanel.hide()

    def deleteImage(self):
        self.renameCleanup()
        self.deletePanel['text'] = TTLocalizer.PhotoPageDelete + '\n"%s"?' % self.getPhotoName(self.selectedFileName)
        self.deletePanel.show()
    def makePhotoButton(self, fileName):
        return DirectButton(relief=None, text=self.getPhotoName(fileName), text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, command=self.chosePhoto, extraArgs=[fileName])

    def errorConfirm(self):
        self.errorPanel.hide()

    def getPhotoName(self, fileName):
        separator = '_'
        numUnders = fileName.count(separator)
        if numUnders == 0:
            return TTLocalizer.PhotoPageNoName
        elif numUnders == 2:
            return fileName.split(separator)[1]
        else:
            return TTLocalizer.PhotoPageUnknownName

    def chosePhoto(self, fileName):
        if fileName:
            self.selectedFileName = fileName
            self.selectedFilePath = self.photoPath + fileName
            if os.path.isfile(self.photoPath + self.selectedFileName):
                photoTexture = loader.loadTexture(self.selectedFilePath)
                photoName = self.getPhotoName(fileName)
                self.pictureFg.setTexture(photoTexture, 1)
                self.pictureFg.setColor(1, 1, 1, 1)
                self.pictureCaption['text'] = photoName
                self.renameButton['state'] = DGG.NORMAL
                self.deleteButton['state'] = DGG.NORMAL
                self.renameEntry.set(photoName)
            else:
                self.errorPanel['text'] = 'Huh. It looks like this snapshot has been deleted or removed.'
                self.errorPanel.show()
                self.updateScrollList()
        else:
            self.selectedFileName = None
            self.pictureFg.clearTexture()
            self.pictureFg.setColor(1, 1, 1, 0.1)
            self.pictureCaption['text'] = ''
            self.renameButton['state'] = DGG.DISABLED
            self.deleteButton['state'] = DGG.DISABLED
            self.renameEntry.set('')
        return

    def getPhotos(self):
        files = os.listdir(self.photoPath)
        photos = []
        for fileName in files:
            if fileName[0:14] == 'ttr-screenshot' and fileName[-4:] == '.jpg':
                photos.append(fileName)          

        return photos

    def openPhotoDirectory(self):
        if platform == "darwin":
            OSXPhotoDir = self.installPath + '/screenshots'
            os.system('open "%s"' % OSXPhotoDir)
            self.notify.debug(OSXPhotoDir)
        elif platform == "win32":
            PhotoDir = self.installPath + '\\screenshots\\'
            os.startfile(PhotoDir)
            self.notify.debug(PhotoDir)

    def newScreenshot(self, filename):
        self.updateScrollList()

    def updateScrollList(self):
        newPhotos = self.getPhotos()        
        for photo in list(self.photos.keys()):
            if photo not in newPhotos:
                photoButton = self.photos[photo]
                self.scrollList.removeItem(photoButton)
                photoButton.destroy()
                del self.photos[photo]

        for photo in newPhotos:
            if photo not in self.photos:
                photoButton = self.makePhotoButton(photo)
                self.scrollList.addItem(photoButton)
                self.photos[photo] = photoButton

        if list(self.photos.keys()):
            self.chosePhoto(list(self.photos.keys())[0])
            self.scroll.hide()
            self.scrollList.show()
            self.pictureImage.show()
            self.rightArrow.show()
            self.leftArrow.show()
            self.renameButton.show()
            self.deleteButton.show()
            self.scrollList.show()
        else:
            self.chosePhoto(None)
            self.scroll.show()
            self.scrollList.hide()
            self.pictureImage.hide()
            self.rightArrow.hide()
            self.leftArrow.hide()
            self.renameButton.hide()
            self.deleteButton.hide()
        return

    def enter(self):
        self.accept('screenshot', self.newScreenshot)
        self.updateScrollList()
        chatEntry = base.localAvatar.chatMgr.chatInputNormal.chatEntry
        self.oldFocus = chatEntry['backgroundFocus']
        ShtikerPage.ShtikerPage.enter(self)

    def exit(self):
        self.ignore('screenshot')
        self.renameCleanup()
        self.deleteCleanup()
        ShtikerPage.ShtikerPage.exit(self)

    def updateArrows(self):
        pass

    def prevPhoto(self):
        pass

    def nextPhoto(self):
        pass
