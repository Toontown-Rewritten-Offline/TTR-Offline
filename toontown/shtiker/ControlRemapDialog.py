from direct.fsm import ClassicFSM, State
from toontown.shtiker.OptionsPageGUI import OptionButton
from toontown.toonbase.TTLocalizer import Controls, RemapPrompt, RemapPopup
from toontown.toonbase.ToontownGlobals import OptionsPageHotkey
from toontown.toontowngui import TTDialog

class ControlRemap:
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    JUMP = 4
    ACTION_BUTTON = 5
    OPTIONS_PAGE_HOTKEY = 6
    CHAT_HOTKEY = 7
    SCREENSHOT_KEY = 8
    INTERACT = 9

    def __init__(self):
        self.dialog = TTDialog.TTGlobalDialog(
            dialogName='ControlRemap', doneEvent='doneRemapping', style=TTDialog.TwoChoice,
            text=RemapPrompt, text_wordwrap=24,
            text_pos=(0, 0, -0.8), suppressKeys = True, suppressMouse = True
        )
        scale = self.dialog.component('image0').getScale()
        scale.setX(((scale[0] * 2.5) / base.getAspectRatio()) * 1.2)
        scale.setZ(scale[2] * 2.5)
        self.dialog.component('image0').setScale(scale)
        button_x = -0.6
        button_y = 0.4
        labelPos = (0, 0, 0.1)

        self.upKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_UP,
            pos=(button_x, 0.0, button_y),
            command=self.enterWaitForKey, extraArgs=[self.UP],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[0])

        self.leftKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_LEFT,
            pos=(button_x + 0.4, 0.0, button_y),
            command=self.enterWaitForKey, extraArgs=[self.LEFT],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[1])

        self.downKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_DOWN,
            pos=(button_x + 0.8, 0.0, button_y),
            command=self.enterWaitForKey, extraArgs=[self.DOWN],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[2])

        self.rightKey = OptionButton(
            parent=self.dialog,
            text=base.MOVE_RIGHT,
            pos=(button_x + 1.2, 0.0, button_y),
            command=self.enterWaitForKey, extraArgs=[self.RIGHT],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[3])

        self.jumpKey = OptionButton(
            parent=self.dialog,
            text=base.JUMP,
            pos=(button_x, 0.0, button_y - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.JUMP],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[4])

        self.actionKey = OptionButton(
            parent=self.dialog,
            text=base.ACTION_BUTTON,
            pos=(button_x + 0.4, 0.0, button_y - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.ACTION_BUTTON],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[5])

        self.optionsKey = OptionButton(
            parent=self.dialog,
            text=OptionsPageHotkey,
            pos=(button_x + 0.8, 0.0, button_y - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.OPTIONS_PAGE_HOTKEY],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[6])
            
        self.chatHotkey = OptionButton(
            parent=self.dialog,
            text=base.CHAT_HOTKEY,
            pos=(button_x + 1.2, 0.0, button_y - 0.3),
            command=self.enterWaitForKey, extraArgs=[self.CHAT_HOTKEY],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[7])

        self.screenshotKey = OptionButton(
            parent=self.dialog,
            text=base.SCREENSHOT_KEY,
            pos=(button_x, 0.0, button_y - 0.6),
            command=self.enterWaitForKey, extraArgs=[self.SCREENSHOT_KEY],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[8])
			
        self.interactKey = OptionButton(
            parent=self.dialog,
            text=base.INTERACT,
            pos=(button_x + 1.2, 0.0, button_y - 0.6),
            command=self.enterWaitForKey, extraArgs=[self.INTERACT],
            wantLabel=True, labelOrientation='top', labelPos=labelPos,
            labelText=Controls[9])
            
        self.controlsToBeSaved = {
            self.UP: base.MOVE_UP,
            self.LEFT: base.MOVE_LEFT,
            self.DOWN: base.MOVE_DOWN,
            self.RIGHT: base.MOVE_RIGHT,
            self.JUMP: base.JUMP,
            self.ACTION_BUTTON: base.ACTION_BUTTON,
            self.OPTIONS_PAGE_HOTKEY: OptionsPageHotkey,
            self.CHAT_HOTKEY: base.CHAT_HOTKEY,
            self.SCREENSHOT_KEY: base.SCREENSHOT_KEY,
            self.INTERACT: base.INTERACT
        }

        self.popupDialog = None
        self.dialog.show()    

        self.fsm = ClassicFSM.ClassicFSM(
            'ControlRemapDialog', [
                State.State('off', self.enterShow, self.exitShow, ['waitForKey']),
                State.State('waitForKey', self.enterWaitForKey, self.exitWaitForKey, ['off'])], 'off', 'off')
        
        self.fsm.enterInitialState()
        self.dialog.accept('doneRemapping', self.exit)
        messenger.send('disable-hotkeys')
        try:
            base.localAvatar.chatMgr.disableBackgroundFocus()
        except:
            pass

    def enterShow(self):
        pass

    def exitShow(self):
        pass

    def enterWaitForKey(self, controlNum):
        base.transitions.fadeScreen(0.9)
        self.dialog.hide()

        if self.popupDialog:
            self.popupDialog.cleanup()
        self.popupDialog = TTDialog.TTDialog(style=TTDialog.NoButtons,
          text=RemapPopup, suppressMouse=True, suppressKeys=True)

        scale = self.popupDialog.component('image0').getScale()
        scale.setX((scale[0] * 3.5) / base.getAspectRatio())
        scale.setZ(scale[2] * 3)
        self.popupDialog.setScale(scale)
        self.popupDialog.show()

        base.buttonThrowers[0].node().setButtonDownEvent('buttonPress-' + str(controlNum))
        self.dialog.accept('buttonPress-' + str(controlNum), self.registerKey, [controlNum])

    def registerKey(self, controlNum, keyName):
        self.popupDialog.cleanup()
        self.controlsToBeSaved[controlNum] = keyName
        if controlNum == self.UP:
            self.upKey['text'] = keyName
        elif controlNum == self.LEFT:
            self.leftKey['text'] = keyName
        elif controlNum == self.DOWN:
            self.downKey['text'] = keyName
        elif controlNum == self.RIGHT:
            self.rightKey['text'] = keyName
        elif controlNum == self.JUMP:
            self.jumpKey['text'] = keyName
        elif controlNum == self.ACTION_BUTTON:
            self.actionKey['text'] = keyName
        elif controlNum == self.OPTIONS_PAGE_HOTKEY:
            self.optionsKey['text'] = keyName
        elif controlNum == self.CHAT_HOTKEY:
            self.chatHotkey['text'] = keyName
        elif controlNum == self.SCREENSHOT_KEY:
            self.screenshotKey['text'] = keyName
        elif controlNum == self.INTERACT:
            self.interactKey['text'] = keyName
        self.dialog.show()    
        self.exitWaitForKey(controlNum, keyName)
        
    def exitWaitForKey(self, controlNum, keyName):
        self.dialog.ignore('buttonPress-' + str(controlNum))

    def exit(self):
        if self.dialog.doneStatus == 'ok':
            self.enterSave()
        else:
            self.enterCancel()

    def enterSave(self):
        keymap = settings.get('keymap', {})
        keymap['MOVE_UP'] = self.controlsToBeSaved[self.UP]
        keymap['MOVE_LEFT'] = self.controlsToBeSaved[self.LEFT]
        keymap['MOVE_DOWN'] = self.controlsToBeSaved[self.DOWN]        
        keymap['MOVE_RIGHT'] = self.controlsToBeSaved[self.RIGHT]
        keymap['JUMP'] = self.controlsToBeSaved[self.JUMP]
        keymap['ACTION_BUTTON'] = self.controlsToBeSaved[self.ACTION_BUTTON]
        keymap['OPTIONS_PAGE_HOTKEY'] = self.controlsToBeSaved[self.OPTIONS_PAGE_HOTKEY]
        keymap['CHAT_HOTKEY'] = self.controlsToBeSaved[self.CHAT_HOTKEY]
        keymap['SCREENSHOT_KEY'] = self.controlsToBeSaved[self.SCREENSHOT_KEY]
        keymap['INTERACT'] = self.controlsToBeSaved[self.INTERACT]
        settings['keymap'] = keymap

        base.reloadControls()
        try:
            base.localAvatar.controlManager.reload()
            base.localAvatar.chatMgr.reloadWASD()
            self.unload()

            base.localAvatar.controlManager.disable()
        except:
            self.unload()

    def exitSave(self):
        pass

    def enterCancel(self):
        self.unload()

    def exitCancel(self):
        pass

    def unload(self):
        if self.popupDialog:
            self.popupDialog.cleanup()
        del self.popupDialog
        self.dialog.cleanup()
        del self.dialog
        messenger.send('enable-hotkeys')