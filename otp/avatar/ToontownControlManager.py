from direct.controls import ControlManager
from direct.showbase.InputStateGlobal import inputState

# This is the new class for Toontown's ControlManager

class ToontownControlManager(ControlManager.ControlManager):
    # Instead of checking config.prc, get wantWASD from ToonBase
    wantWASD = base.wantCustomControls

    def __init__(self, enable=True, passMessagesThrough=True):
        self.passMessagesThrough = passMessagesThrough
        self.inputStateTokens = []
        self.WASDTurnTokens = []
        self.controls = {}
        self.currentControls = None
        self.currentControlsName = None
        self.isEnabled = 0
        self.forceAvJumpToken = None
        self.inputToDisable = []
        self.forceTokens = None
        self.istWASD = []
        self.istNormal = []
        if enable:
            self.enable()

    def enable(self):
        if self.isEnabled:
            return

        self.isEnabled = 1
        keymap = settings.get('keymap', {})
        # Keep track of what we do on the inputState so we can undo it later on
        self.inputStateTokens.extend((
            inputState.watch('run', 'runningEvent', 'running-on', 'running-off'),
            inputState.watch('forward', 'force-forward', 'force-forward-stop'),
        ))

        if self.wantWASD:
            self.istWASD.extend((
                inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'),
                inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'),
                inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'),
                inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop'),
                inputState.watchWithModifiers('forward', keymap.get('MOVE_UP', base.MOVE_UP), inputSource=inputState.WASD),
                inputState.watchWithModifiers('reverse', keymap.get('MOVE_DOWN', base.MOVE_DOWN), inputSource=inputState.WASD),
                inputState.watchWithModifiers('jump', keymap.get('JUMP', base.JUMP))
            ))

            self.setWASDTurn(True)

        else:
            self.istNormal.extend((
                inputState.watchWithModifiers('forward', base.MOVE_UP, inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('reverse', base.MOVE_DOWN, inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('turnLeft', base.MOVE_LEFT, inputSource=inputState.ArrowKeys),
                inputState.watchWithModifiers('turnRight', base.MOVE_RIGHT, inputSource=inputState.ArrowKeys),
                inputState.watch('jump', base.JUMP, base.JUMP + '-up')
            ))
            
            self.istNormal.extend((
                inputState.watch('turnLeft', 'mouse-look_left', 'mouse-look_left-done'),
                inputState.watch('turnLeft', 'force-turnLeft', 'force-turnLeft-stop'),
                inputState.watch('turnRight', 'mouse-look_right', 'mouse-look_right-done'),
                inputState.watch('turnRight', 'force-turnRight', 'force-turnRight-stop')
            ))
            

        if self.currentControls:
            self.currentControls.enableAvatarControls()

    def setWASDTurn(self, turn):
        # This probably needs to be cleaned up, I don't think Toontown uses slide anywhere
        self.__WASDTurn = turn

        if not self.isEnabled:
            return
        
        keymap = settings.get('keymap', {})
        
        turnLeftWASDSet = inputState.isSet("turnLeft", inputSource=inputState.WASD)
        turnRightWASDSet = inputState.isSet("turnRight", inputSource=inputState.WASD)
        slideLeftWASDSet = inputState.isSet("slideLeft", inputSource=inputState.WASD)
        slideRightWASDSet = inputState.isSet("slideRight", inputSource=inputState.WASD)

        for token in self.WASDTurnTokens:
            token.release()

        if turn:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("turnLeft", keymap.get('MOVE_LEFT', base.MOVE_LEFT), inputSource=inputState.WASD),
                inputState.watchWithModifiers("turnRight", keymap.get('MOVE_RIGHT', base.MOVE_RIGHT), inputSource=inputState.WASD),
                )

            inputState.set("turnLeft", slideLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("turnRight", slideRightWASDSet, inputSource=inputState.WASD)

            inputState.set("slideLeft", False, inputSource=inputState.WASD)
            inputState.set("slideRight", False, inputSource=inputState.WASD)

        else:
            self.WASDTurnTokens = (
                inputState.watchWithModifiers("slideLeft", keymap.get('MOVE_LEFT', base.MOVE_LEFT), inputSource=inputState.WASD),
                inputState.watchWithModifiers("slideRight", keymap.get('MOVE_RIGHT', base.MOVE_RIGHT), inputSource=inputState.WASD),
                )

            inputState.set("slideLeft", turnLeftWASDSet, inputSource=inputState.WASD)
            inputState.set("slideRight", turnRightWASDSet, inputSource=inputState.WASD)
                
            inputState.set("turnLeft", False, inputSource=inputState.WASD)
            inputState.set("turnRight", False, inputSource=inputState.WASD)

    def disable(self):
        self.isEnabled = 0

        for token in self.istNormal:
            token.release()
        self.istNormal = []

        for token in self.inputStateTokens:
            token.release()
        self.inputStateTokens = []

        for token in self.istWASD:
            token.release()
        self.istWASD = []

        for token in self.WASDTurnTokens:
            token.release()
        self.WASDTurnTokens = []
        if self.currentControls:
            self.currentControls.disableAvatarControls()
        keymap = settings.get('keymap', {})
        if self.passMessagesThrough:
            if self.wantWASD:
                self.istWASD.append(inputState.watchWithModifiers(
                  'forward', keymap.get('MOVE_UP', base.MOVE_UP), inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers(
                  'reverse', keymap.get('MOVE_DOWN', base.MOVE_DOWN), inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers(
                  'turnLeft', keymap.get('MOVE_LEFT', base.MOVE_LEFT), inputSource=inputState.WASD))
                self.istWASD.append(inputState.watchWithModifiers(
                  'turnRight', keymap.get('MOVE_RIGHT', base.MOVE_RIGHT), inputSource=inputState.WASD))
            else:
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'forward',
                        base.MOVE_UP,
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'reverse',
                        base.MOVE_DOWN,
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'turnLeft',
                        base.MOVE_LEFT,
                        inputSource=inputState.ArrowKeys))
                self.istNormal.append(
                    inputState.watchWithModifiers(
                        'turnRight',
                        base.MOVE_RIGHT,
                        inputSource=inputState.ArrowKeys))

    def disableWASD(self):
        # Disables WASD for when chat is open.
        # Forces all keys to return 0. This won't affect chat input.
        if self.wantWASD:
            self.forceTokens = [
                inputState.force('jump', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('forward', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('turnLeft', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('slideLeft', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('reverse', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('turnRight', 0, 'ToontownControlManager.disableWASD'),
                inputState.force('slideRight', 0, 'ToontownControlManager.disableWASD')
            ]

    def enableWASD(self):
        # Enables WASD after chat is closed.
        # Releases all the forced keys we added earlier.
        if self.wantWASD:
            if self.forceTokens:
                for token in self.forceTokens:
                    token.release()
                self.forceTokens = []


    def disableControls(self):
        # Forces all keys to return 0.
        self.forceTokens = [
            inputState.force('jump', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('forward', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('turnLeft', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('slideLeft', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('reverse', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('turnRight', 0, 'ToontownControlManager.disableWASD'),
            inputState.force('slideRight', 0, 'ToontownControlManager.disableWASD')
        ]

    def enableControls(self):
        # Releases all the forced keys we added earlier.
        if self.forceTokens:
            for token in self.forceTokens:
                token.release()
            self.forceTokens = []
                
    def reload(self):
        # Called to reload the ControlManager ingame
        # Reload wantWASD
        self.wantWASD = base.wantCustomControls
        self.disable()
        self.enable()
