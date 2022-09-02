from .SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import SpeedChatStaticText
SCStaticTextMsgEvent = 'SCStaticTextMsg'
SCStaticTextThoughtEvent = 'SCStaticTextThought'

def decodeSCStaticTextMsg(textId):
    return SpeedChatStaticText.get(textId, None)


class SCStaticTextTerminal(SCTerminal):

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = SpeedChatStaticText[self.textId]

    def handleSelect(self, event):
        event = str(event)
        SCTerminal.handleSelect(self, event)
        if event.startswith('mouse1'):
            messenger.send(self.getEventName(SCStaticTextMsgEvent), [self.textId])
        elif event.startswith('mouse3'):
            messenger.send(self.getEventName(SCStaticTextThoughtEvent), [self.textId])
