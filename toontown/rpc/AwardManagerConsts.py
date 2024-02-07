from enum import Enum
#GiveAwardErrors = Enum('Success, WrongGender, NotGiftable, FullMailbox, FullAwardMailbox, AlreadyInMailbox, AlreadyInGiftQueue, AlreadyInOrderedQueue, AlreadyInCloset, AlreadyBeingWorn, AlreadyInAwardMailbox, AlreadyInThirtyMinuteQueue, AlreadyInMyPhrases, AlreadyKnowDoodleTraining, AlreadyRented, GenericAlreadyHaveError, UnknownError, UnknownToon, NonToon,')
class GiveAwardErrors(Enum):
    Success = 1
    WrongGender = 2
    NotGiftable = 3
    FullMailbox = 4
    FullAwardMailbox = 5
    AlreadyInMailbox = 6
    AlreadyInGiftQueue = 7
    AlreadyInOrderedQueue = 8
    AlreadyInCloset = 9
    AlreadyBeingWorn = 10
    AlreadyInAwardMailbox = 11
    AlreadyInThirtyMinuteQueue = 12
    AlreadyInMyPhrases = 13
    AlreadyKnowDoodleTraining = 14
    AlreadyRented = 15
    GenericAlreadyHaveError = 16
    UnknownError = 17
    UnknownToon = 18
    NonToon = 19
GiveAwardErrorStrings = {GiveAwardErrors.Success: 'success',
 GiveAwardErrors.WrongGender: 'wrong gender',
 GiveAwardErrors.NotGiftable: 'item is not giftable',
 GiveAwardErrors.FullMailbox: 'mailbox is full',
 GiveAwardErrors.FullAwardMailbox: 'award mailbox is full',
 GiveAwardErrors.AlreadyInMailbox: 'award already in mailbox.',
 GiveAwardErrors.AlreadyInGiftQueue: 'award already in gift queue.',
 GiveAwardErrors.AlreadyInOrderedQueue: 'award already in ordered queue.',
 GiveAwardErrors.AlreadyInCloset: 'award already in closet.',
 GiveAwardErrors.AlreadyBeingWorn: 'award already being worn.',
 GiveAwardErrors.AlreadyInAwardMailbox: 'award already in award mailbox',
 GiveAwardErrors.AlreadyInThirtyMinuteQueue: 'award already in 30 minute queue',
 GiveAwardErrors.AlreadyInMyPhrases: 'speed chat award already in my phrases',
 GiveAwardErrors.AlreadyKnowDoodleTraining: 'doodle training award already known',
 GiveAwardErrors.AlreadyRented: 'award is already rented',
 GiveAwardErrors.GenericAlreadyHaveError: 'generic-already-have error',
 GiveAwardErrors.UnknownError: 'unknown error',
 GiveAwardErrors.UnknownToon: 'toon not in database',
 GiveAwardErrors.NonToon: 'this is not a toon'}

