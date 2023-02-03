from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui import DirectGuiGlobals
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from panda3d.core import *
from otp.otpbase.Settings import Settings

PAGE_GAMEPLAY = 1
PAGE_CONTROLS = 2
PAGE_AUDIO = 3
PAGE_VIDEO = 4

class OptionsPage(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('OptionsPage')

    def __init__(self):
        DirectFrame.__init__(self)
        self.reparentTo(aspect2d)
        self.setPos(0, 0, -0.05)
        self.hide()

        self.buttonXoffset = 0.406
        self.TextTitleColor = (0.232, 0.671, 0.961, 1)

        self.OptionsIcon = loader.loadModel('phase_3/models/gui/ttr_m_gui_sbk_settingsIcon')
        self.OptionsIconUp = self.OptionsIcon.find('**/ttr_t_gui_sbk_settingsIcon_up')
        self.OptionsIconHover = self.OptionsIcon.find('**/ttr_t_gui_sbk_settingsIcon_hover')
        self.OptionsIconDown = self.OptionsIcon.find('**/ttr_t_gui_sbk_settingsIcon_down')

        self.OptionsGUI = loader.loadModel('phase_3/models/gui/ttr_m_gui_sbk_settingsPanel')
        self.OptionsGUIPanel = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_panelMain')
        self.OptionsGUIPanel.setBin('fixed', 0)
        self.OptionsGUIPageGameplay = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabActive1')
        self.OptionsGUIPageGameplay.setBin('fixed', 2)
        self.OptionsGUIPageControls = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabActive2')
        self.OptionsGUIPageControls.setBin('fixed', 2)
        self.OptionsGUIPageAudio = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabActive3')
        self.OptionsGUIPageAudio.setBin('fixed', 2)
        self.OptionsGUIPageVideo = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabActive4')
        self.OptionsGUIPageVideo.setBin('fixed', 2)

        self.OptionsGUIImages = loader.loadModel('phase_3/models/gui/ttr_m_gui_gen_buttons')
        self.OptionsX = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_xButton')
        self.OptionsXHover = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_xButton')
        self.OptionsGUIGameplayActive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_playActive')
        self.OptionsGUIGameplayInactive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_playInactive')
        self.OptionsGUIControlsActive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_controlsActive')
        self.OptionsGUIControlsInactive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_controlsInactive')
        self.OptionsGUIAudioActive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_audioActive')
        self.OptionsGUIAudioInactive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_audioInactive')
        self.OptionsGUIVideoActive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_videoActive')
        self.OptionsGUIVideoInactive = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_videoInactive')

        self.OptionsGUITabButton = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabInactive')

        self.OptionsGUIScrollBar = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_lineSkinny')
        self.OptionsGUIScrollThumb = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_slider1')
        self.OptionsGUIScrollBar.setR(90)
        #self.OptionsGUIScrollBar.setPos(0.78, 0, 0.04)

        self.setupGUI()

    def setupGUI(self):
        self.frame = DirectFrame(parent=self, geom=self.OptionsGUIPanel, geom_pos=(0.0, 0.0, 0.0), geom_scale=0.15, relief=None)

        # Scroll Wheel
        SCROLL_UP = PGButton.getReleasePrefix() + MouseButton.wheelUp().getName() + "-"
        SCROLL_DOWN = PGButton.getReleasePrefix() + MouseButton.wheelDown().getName() + "-"
        def mouseScrollValue(scrollBar, direction, value):
            scrollBar.setValue(scrollBar.getValue() + direction*scrollBar["pageSize"])

        '''Global Values'''
        # Section Text Titles
        self.SectionTextXOffset = -0.225
        self.SectionTextScale = 0.09
        self.SectionTextFont = ToontownGlobals.getMinnieFont()

        # Scroll Frame Globals
        self.ScrollBarWidth = 0.04
        self.ScrollBarPos = (0.825, 0, -0.18)
        self.ScrollBarFrameSize = (-self.ScrollBarWidth / 2.0, self.ScrollBarWidth / 2.0, -0.45, 0.45)
        self.ScrollBarGeom = self.OptionsGUIScrollBar
        self.ScrollBarGeomScale = (0.225, 0, 0.15)
        self.ScrollBarThumbGeom = self.OptionsGUIScrollThumb
        self.ScrollBarThumbGeomScale = 0.085
        self.ScrollBarResizeThumb = False

        # Options Icon
        self.OptionsButton = DirectButton(parent=base.a2dBottomRight, relief=None, geom=(self.OptionsIconUp,
         self.OptionsIconDown,
         self.OptionsIconHover), pos=(-0.158, 0, 0.5), geom_scale=(0.05, 0.05, 0.05), command=self.show)

        # Options Exit
        self.OptionsButtonX = DirectButton(parent=self, relief=None, scale=(1), pressEffect=0, image=(self.OptionsX, self.OptionsXHover),
        pos=(0.9, 0, 0.6), image_scale=(0.1), command=self.hide)

        '''Page Frames'''
        # Gameplay
        self.OptionsPageGameplay = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageGameplay, image_scale=(0.15),
                                               geom=self.OptionsGUIGameplayActive, geom_scale=(0.15), geom_pos=(-0.6075, 0, 0.58125), pos=(0, 0, 0.11))

        self.GameplayTitle = OnscreenText(parent=self.OptionsPageGameplay, font=ToontownGlobals.getMickeyFontMaximum(), text=TTLocalizer.NewOptionsTabGameplayTitle,
                                                     fg=self.TextTitleColor, pos=(0, 0.31, 0), scale=(0.15))

        self.GameplayScrollCanvasSize = (-0.75, 0.75, -2, 2)
        self.GameplayScrollFrame = DirectFrame(parent=self.OptionsPageGameplay, state=DGG.NORMAL, pos=(0, 0, -0.25), frameSize=(-0.8, 0.8, -0.45, 0.525), pgFunc=PGScrollFrame)
        self.GameplayScrollCanvas = NodePath(self.GameplayScrollFrame.guiItem.getCanvasNode())
        self.GameplayScrollFrame.guiItem.setVirtualFrame(self.GameplayScrollCanvasSize)

        self.GameplayScrollBar = DirectScrollBar(parent=self.OptionsPageGameplay, orientation=DGG.VERTICAL, relief=None thumb_relief=None)
        self.GameplayScrollFrame.guiItem.setVerticalSlider(self.GameplayScrollBar.guiItem)
        self.GameplayScrollBar['pos'] = self.ScrollBarPos
        self.GameplayScrollBar['frameSize'] = self.ScrollBarFrameSize
        self.GameplayScrollBar['geom'] = self.ScrollBarGeom
        self.GameplayScrollBar['geom_scale'] = self.ScrollBarGeomScale
        self.GameplayScrollBar['thumb_geom'] = self.ScrollBarThumbGeom
        self.GameplayScrollBar['thumb_geom_scale'] = self.ScrollBarThumbGeomScale
        self.GameplayScrollBar['resizeThumb'] = self.ScrollBarResizeThumb
        self.GameplayScrollBar.incButton.destroy()
        self.GameplayScrollBar.decButton.destroy()
        self.GameplayScrollFrame.bind(SCROLL_UP, mouseScrollValue, [self.GameplayScrollBar, -0.325])
        self.GameplayScrollFrame.bind(SCROLL_DOWN, mouseScrollValue, [self.GameplayScrollBar, 0.325])

        # Gameplay Components
        self.GameplayPlacholderText = OnscreenText(parent=self.GameplayScrollCanvas, text=TTLocalizer.NewOptionsTabGameplayToon, font=self.SectionTextFont, scale=self.SectionTextScale, pos=(self.SectionTextXOffset, 1.9))


        # Controls
        self.OptionsPageControls = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageControls, image_scale=(0.15),
        geom=self.OptionsGUIControlsActive, geom_scale=(0.15), geom_pos=(-0.20125, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageControls.hide()


        # Audio
        self.OptionsPageAudio = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageAudio, image_scale=(0.15),
        geom=self.OptionsGUIAudioActive, geom_scale=(0.15), geom_pos=(0.205, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageAudio.hide()


        # Video
        self.OptionsPageVideo = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageVideo, image_scale=(0.15),
        geom=self.OptionsGUIVideoActive, geom_scale=(0.15), geom_pos=(0.61, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageVideo.hide()


        # Page Buttons
        self.OptionsButtonGameplay = DirectButton(parent=self, relief=None, image=self.OptionsGUITabButton,
        image_scale=(0.15), geom=(self.OptionsGUIGameplayInactive), geom_pos=(0, 0, 0.025), geom_scale=(0.15), pos=(-0.6075, 0, 0.665), command=self.setupButtons, extraArgs=[PAGE_GAMEPLAY])
        self.OptionsButtonGameplay.setBin('fixed', 1)

        self.OptionsButtonControls = DirectButton(parent=self, relief=None, image=(self.OptionsGUITabButton),
        image_scale=(0.15), geom=(self.OptionsGUIControlsInactive), geom_pos=(0, 0, 0.025), geom_scale=(0.15), pos=((-0.6075 + self.buttonXoffset), 0, 0.665), command=self.setupButtons, extraArgs=[PAGE_CONTROLS])
        self.OptionsButtonControls.setBin('fixed', 1)

        self.OptionsButtonAudio = DirectButton(parent=self, relief=None, image=(self.OptionsGUITabButton),
        image_scale=(0.15), geom=(self.OptionsGUIAudioInactive), geom_pos=(0, 0, 0.025), geom_scale=(0.15), pos=((-0.6075 + (self.buttonXoffset * 2)), 0, 0.665), command=self.setupButtons, extraArgs=[PAGE_AUDIO])
        self.OptionsButtonAudio.setBin('fixed', 1)

        self.OptionsButtonVideo = DirectButton(parent=self, relief=None, image=(self.OptionsGUITabButton),
        image_scale=(0.15), geom=(self.OptionsGUIVideoInactive), geom_pos=(0, 0, 0.025), geom_scale=(0.15), pos=((-0.6075 + (self.buttonXoffset * 3)), 0, 0.665), command=self.setupButtons, extraArgs=[PAGE_VIDEO])
        self.OptionsButtonVideo.setBin('fixed', 1)

    def setupButtons(self, page):
        if page == PAGE_GAMEPLAY:
            self.OptionsButtonGameplay.hide()
            self.OptionsButtonControls.show()
            self.OptionsButtonAudio.show()
            self.OptionsButtonVideo.show()
            self.OptionsButtonGameplay['state'] = DGG.DISABLED
            self.OptionsButtonControls['state'] = DGG.NORMAL
            self.OptionsButtonAudio['state'] = DGG.NORMAL
            self.OptionsButtonVideo['state'] = DGG.NORMAL
            self.OptionsPageGameplay.show()
            self.OptionsPageControls.hide()
            self.OptionsPageAudio.hide()
            self.OptionsPageVideo.hide()
        if page == PAGE_CONTROLS:
            self.OptionsButtonGameplay.show()
            self.OptionsButtonControls.hide()
            self.OptionsButtonAudio.show()
            self.OptionsButtonVideo.show()
            self.OptionsButtonGameplay['state'] = DGG.NORMAL
            self.OptionsButtonControls['state'] = DGG.DISABLED
            self.OptionsButtonAudio['state'] = DGG.NORMAL
            self.OptionsButtonVideo['state'] = DGG.NORMAL
            self.OptionsPageGameplay.hide()
            self.OptionsPageControls.show()
            self.OptionsPageAudio.hide()
            self.OptionsPageVideo.hide()
        if page == PAGE_AUDIO:
            self.OptionsButtonGameplay.show()
            self.OptionsButtonControls.show()
            self.OptionsButtonAudio.hide()
            self.OptionsButtonVideo.show()
            self.OptionsButtonGameplay['state'] = DGG.NORMAL
            self.OptionsButtonControls['state'] = DGG.NORMAL
            self.OptionsButtonAudio['state'] = DGG.DISABLED
            self.OptionsButtonVideo['state'] = DGG.NORMAL
            self.OptionsPageGameplay.hide()
            self.OptionsPageControls.hide()
            self.OptionsPageAudio.show()
            self.OptionsPageVideo.hide()
        if page == PAGE_VIDEO:
            self.OptionsButtonGameplay.show()
            self.OptionsButtonControls.show()
            self.OptionsButtonAudio.show()
            self.OptionsButtonVideo.hide()
            self.OptionsButtonGameplay['state'] = DGG.NORMAL
            self.OptionsButtonControls['state'] = DGG.NORMAL
            self.OptionsButtonAudio['state'] = DGG.NORMAL
            self.OptionsButtonVideo['state'] = DGG.DISABLED
            self.OptionsPageGameplay.hide()
            self.OptionsPageControls.hide()
            self.OptionsPageAudio.hide()
            self.OptionsPageVideo.show()