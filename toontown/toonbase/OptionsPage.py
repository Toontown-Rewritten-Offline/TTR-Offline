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

        self.OptionsGUIButtonBox = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_box')
        self.OptionsGUISquareButton = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_squareButton')
        self.DynamicBox = self.OptionsGUISquareButton.attachNewNode('dynamicBox')
        self.OptionsGUIButtonBox.reparentTo(self.DynamicBox)
        self.OptionsGUISquareButton.find('**/ttr_t_gui_gen_buttons_box').setScale(1, 1, 1)

        self.OptionsGUITabButton = self.OptionsGUI.find('**/ttr_t_gui_sbk_settingsPanel_tabInactive')

        self.OptionsGUIScrollBar = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_lineSkinny')
        self.OptionsGUIScrollThumb = self.OptionsGUIImages.find('**/ttr_t_gui_gen_buttons_slider1')
        self.OptionsGUIScrollBar.setR(90)

        self.setupGUI()
        self.initialiseoptions(DirectFrame)

    def setupGUI(self):
        '''Global Values'''
        # Pages
        self.PagePos = (0, 0, 0.11)
        self.PageImageScale = 0.15
        self.PageGeomScale = 0.15

        self.buttonXoffset = 0.406

        # Scroll Frame
        self.ScrollFramePos = (0, 0, -0.25)
        self.ScrollFrameSize = (-0.8, 0.8, -0.45, 0.5075)
        self.ScrollFrameCanvasSize = (-0.75, 0.75, -2, 2)
        self.ScrollBarWidth = 0.04
        self.ScrollBarFrameSize = (-self.ScrollBarWidth / 2.0, self.ScrollBarWidth / 2.0, -0.41, 0.41)
        self.ScrollBarPos = (0.82, 0, -0.21)
        self.ScrollBarGeom = self.OptionsGUIScrollBar
        self.ScrollBarGeomScale = (0.225, 0, 0.15)
        self.ScrollBarThumbGeom = self.OptionsGUIScrollThumb
        self.ScrollBarThumbGeomScale = 0.09
        self.ScrollBarResizeThumb = False

        # Scroll Wheel
        self.frame = DirectFrame(parent=self, geom=self.OptionsGUIPanel, geom_pos=(0.0, 0.0, 0.0), geom_scale=0.15, relief=None)
        SCROLL_UP = PGButton.getReleasePrefix() + MouseButton.wheelUp().getName() + "-"
        SCROLL_DOWN = PGButton.getReleasePrefix() + MouseButton.wheelDown().getName() + "-"
        def mouseScrollValue(scrollBar, direction, value):
            scrollBar.setValue(scrollBar.getValue() + direction*scrollBar["pageSize"])

        # Title Text
        self.TitleTextPos = (0, 0.3025, 0)
        self.TitleTextScale = 0.15
        self.TitleTextColor = (0.232, 0.671, 0.961, 1)
        self.TitleTextFont = ToontownGlobals.getMickeyFontMaximum()

        # Section Text
        self.SectionTextXOffset = -0.71375
        self.SectionTextScale = 0.09
        self.SectionTextFont = ToontownGlobals.getMinnieFont()

        # Option Text
        self.OptionTextXOffset = -0.71375
        self.OptionTextScale = 0.06

        # Option Button
        self.OptionButtonXOffset = 0.5
        self.OptionButtonScale = (0.1, 0.1, 0.1)

        '''Options Button'''
        # Options Icon
        self.OptionsButton = DirectButton(parent=base.a2dBottomRight, relief=None, geom=(self.OptionsIconUp,
         self.OptionsIconDown,
         self.OptionsIconHover), pos=(-0.158, 0, 0.5), geom_scale=(0.05, 0.05, 0.05), command=self.show)

        # Options Exit
        self.OptionsButtonX = DirectButton(parent=self, relief=None, image=(self.OptionsX),
                                           pos=(0.865, 0, 0.6), image_scale=(0.105), command=self.hide)
        hover = self.OptionsButtonX.stateNodePath[0].attachNewNode('main', 1)
        self.OptionsButtonX.stateNodePath[0] = hover
        hover.setScale(0.8)
        self.OptionsButtonX.updateFrameStyle()

        '''Page Frames'''
        # Gameplay
        self.OptionsPageGameplay = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageGameplay, image_scale=self.PageImageScale,
                                               geom=self.OptionsGUIGameplayActive, geom_scale=self.PageImageScale, geom_pos=(-0.6075, 0, 0.58125), pos=self.PagePos)

        self.GameplayTitle = OnscreenText(parent=self.OptionsPageGameplay, font=self.TitleTextFont, text=TTLocalizer.NewOptionsTabGameplayTitle,
                                                     fg=self.TitleTextColor, pos=self.TitleTextPos, scale=self.TitleTextScale)

        self.GameplayScrollFrame = DirectFrame(parent=self.OptionsPageGameplay, state=DGG.NORMAL, relief=None, pos=self.ScrollFramePos, frameSize=self.ScrollFrameSize, pgFunc=PGScrollFrame)
        self.GameplayScrollFrameCanvas = NodePath(self.GameplayScrollFrame.guiItem.getCanvasNode())
        self.GameplayScrollFrame.guiItem.setVirtualFrame(self.ScrollFrameCanvasSize)

        self.GameplayScrollBar = DirectScrollBar(parent=self.OptionsPageGameplay, orientation=DGG.VERTICAL, relief=None, thumb_relief=None)
        self.GameplayScrollFrame.guiItem.setVerticalSlider(self.GameplayScrollBar.guiItem)
        self.GameplayScrollBar.setPos(self.ScrollBarPos)
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
        self.GameplayToonPreferencesText = OnscreenText(parent=self.GameplayScrollFrameCanvas, align=TextNode.ALeft, text=TTLocalizer.NewOptionsTabGameplayToon, font=self.SectionTextFont, scale=self.SectionTextScale, pos=(self.SectionTextXOffset, 1.85))


        # Controls
        self.OptionsPageControls = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageControls, image_scale=(0.15),
        geom=self.OptionsGUIControlsActive, geom_scale=(0.15), geom_pos=(-0.20125, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageControls.hide()

        self.ControlsTitle = OnscreenText(parent=self.OptionsPageControls, font=self.TitleTextFont, text=TTLocalizer.NewOptionsTabControlsTitle,
                                                     fg=self.TitleTextColor, pos=self.TitleTextPos, scale=self.TitleTextScale)

        self.ControlsScrollFrame = DirectFrame(parent=self.OptionsPageControls, relief=None, state=DGG.NORMAL, pos=self.ScrollFramePos, frameSize=self.ScrollFrameSize, pgFunc=PGScrollFrame)
        self.ControlsScrollFrameCanvas = NodePath(self.ControlsScrollFrame.guiItem.getCanvasNode())
        self.ControlsScrollFrame.guiItem.setVirtualFrame(self.ScrollFrameCanvasSize)

        self.ControlsScrollBar = DirectScrollBar(parent=self.OptionsPageControls, orientation=DGG.VERTICAL, relief=None, thumb_relief=None)
        self.ControlsScrollFrame.guiItem.setVerticalSlider(self.ControlsScrollBar.guiItem)
        self.ControlsScrollBar.setPos(self.ScrollBarPos)
        self.ControlsScrollBar['frameSize'] = self.ScrollBarFrameSize
        self.ControlsScrollBar['geom'] = self.ScrollBarGeom
        self.ControlsScrollBar['geom_scale'] = self.ScrollBarGeomScale
        self.ControlsScrollBar['thumb_geom'] = self.ScrollBarThumbGeom
        self.ControlsScrollBar['thumb_geom_scale'] = self.ScrollBarThumbGeomScale
        self.ControlsScrollBar['resizeThumb'] = self.ScrollBarResizeThumb
        self.ControlsScrollBar.incButton.destroy()
        self.ControlsScrollBar.decButton.destroy()
        self.ControlsScrollFrame.bind(SCROLL_UP, mouseScrollValue, [self.ControlsScrollBar, -0.325])
        self.ControlsScrollFrame.bind(SCROLL_DOWN, mouseScrollValue, [self.ControlsScrollBar, 0.325])

        # Controls Components
        self.ControlsMovementText = OnscreenText(parent=self.ControlsScrollFrameCanvas, align=TextNode.ALeft, text=TTLocalizer.NewOptionsTabControlsMovement, font=self.SectionTextFont, scale=self.SectionTextScale, pos=(self.SectionTextXOffset, 1.85))

        self.ControlsMovementForwardText = OnscreenText(parent=self.ControlsScrollFrameCanvas, align=TextNode.ALeft, text=TTLocalizer.NewOptionsTabControlsForward, scale=self.OptionTextScale, pos=(self.OptionTextXOffset, 1.73))
        self.ControlsMovementForwardButton = DirectButton(parent=self.ControlsScrollFrame, relief=None, geom=self.OptionsGUISquareButton, text='', scale=self.OptionButtonScale, pos=(self.OptionButtonXOffset, 0, 0.25))


        # Audio
        self.OptionsPageAudio = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageAudio, image_scale=(0.15),
        geom=self.OptionsGUIAudioActive, geom_scale=(0.15), geom_pos=(0.205, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageAudio.hide()

        self.ControlsTitle = OnscreenText(parent=self.OptionsPageAudio, font=self.TitleTextFont, text=TTLocalizer.NewOptionsTabAudioTitle,
                                                     fg=self.TitleTextColor, pos=self.TitleTextPos, scale=self.TitleTextScale)

        self.AudioScrollFrame = DirectFrame(parent=self.OptionsPageAudio, state=DGG.NORMAL, pos=self.ScrollFramePos, frameSize=self.ScrollFrameSize, pgFunc=PGScrollFrame)
        self.AudioScrollFrameCanvas = NodePath(self.AudioScrollFrame.guiItem.getCanvasNode())
        self.AudioScrollFrame.guiItem.setVirtualFrame(self.ScrollFrameCanvasSize)

        self.AudioScrollBar = DirectScrollBar(parent=self.OptionsPageAudio, orientation=DGG.VERTICAL, relief=None, thumb_relief=None)
        self.AudioScrollFrame.guiItem.setVerticalSlider(self.AudioScrollBar.guiItem)
        self.AudioScrollBar.setPos(self.ScrollBarPos)
        self.AudioScrollBar['frameSize'] = self.ScrollBarFrameSize
        self.AudioScrollBar['geom'] = self.ScrollBarGeom
        self.AudioScrollBar['geom_scale'] = self.ScrollBarGeomScale
        self.AudioScrollBar['thumb_geom'] = self.ScrollBarThumbGeom
        self.AudioScrollBar['thumb_geom_scale'] = self.ScrollBarThumbGeomScale
        self.AudioScrollBar['resizeThumb'] = self.ScrollBarResizeThumb
        self.AudioScrollBar.incButton.destroy()
        self.AudioScrollBar.decButton.destroy()
        self.AudioScrollFrame.bind(SCROLL_UP, mouseScrollValue, [self.AudioScrollBar, -0.325])
        self.AudioScrollFrame.bind(SCROLL_DOWN, mouseScrollValue, [self.AudioScrollBar, 0.325])

        # Audio Components
        self.AudioMusicText = OnscreenText(parent=self.AudioScrollFrameCanvas, align=TextNode.ALeft, text=TTLocalizer.NewOptionsTabAudioMusicTitle, font=self.SectionTextFont, scale=self.SectionTextScale, pos=(self.SectionTextXOffset, 1.85))

        # Video
        self.OptionsPageVideo = DirectFrame(parent=self, relief=None, image=self.OptionsGUIPageVideo, image_scale=(0.15),
        geom=self.OptionsGUIVideoActive, geom_scale=(0.15), geom_pos=(0.61, 0, 0.58125), pos=(0, 0, 0.11))
        self.OptionsPageVideo.hide()

        self.ControlsTitle = OnscreenText(parent=self.OptionsPageVideo, font=self.TitleTextFont, text=TTLocalizer.NewOptionsTabVideoTitle,
                                                     fg=self.TitleTextColor, pos=self.TitleTextPos, scale=self.TitleTextScale)

        self.VideoScrollFrame = DirectFrame(parent=self.OptionsPageVideo, state=DGG.NORMAL, pos=self.ScrollFramePos, frameSize=self.ScrollFrameSize, pgFunc=PGScrollFrame)
        self.VideoScrollFrameCanvas = NodePath(self.VideoScrollFrame.guiItem.getCanvasNode())
        self.VideoScrollFrame.guiItem.setVirtualFrame(self.ScrollFrameCanvasSize)

        self.VideoScrollBar = DirectScrollBar(parent=self.OptionsPageVideo, orientation=DGG.VERTICAL, relief=None, thumb_relief=None)
        self.VideoScrollFrame.guiItem.setVerticalSlider(self.VideoScrollBar.guiItem)
        self.VideoScrollBar.setPos(self.ScrollBarPos)
        self.VideoScrollBar['frameSize'] = self.ScrollBarFrameSize
        self.VideoScrollBar['geom'] = self.ScrollBarGeom
        self.VideoScrollBar['geom_scale'] = self.ScrollBarGeomScale
        self.VideoScrollBar['thumb_geom'] = self.ScrollBarThumbGeom
        self.VideoScrollBar['thumb_geom_scale'] = self.ScrollBarThumbGeomScale
        self.VideoScrollBar['resizeThumb'] = self.ScrollBarResizeThumb
        self.VideoScrollBar.incButton.destroy()
        self.VideoScrollBar.decButton.destroy()
        self.VideoScrollFrame.bind(SCROLL_UP, mouseScrollValue, [self.VideoScrollBar, -0.325])
        self.VideoScrollFrame.bind(SCROLL_DOWN, mouseScrollValue, [self.VideoScrollBar, 0.325])

        # Controls Components
        self.VideoDisplayText = OnscreenText(parent=self.VideoScrollFrameCanvas, align=TextNode.ALeft, text=TTLocalizer.NewOptionsTabDisplayTitle, font=self.SectionTextFont, scale=self.SectionTextScale, pos=(self.SectionTextXOffset, 1.85))


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