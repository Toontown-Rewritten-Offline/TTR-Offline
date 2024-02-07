from enum import Enum
DefaultDbName = 'tt_code_redemption'
#RedeemErrors = Enum('Success, CodeDoesntExist, CodeIsInactive, CodeAlreadyRedeemed, AwardCouldntBeGiven, TooManyAttempts, SystemUnavailable, ')
class RedeemErrors(Enum):
    Success = 1
    CodeDoesntExist = 2
    CodeIsInactive = 3
    CodeAlreadyRedeemed = 4
    AwardCouldntBeGiven = 5
    TooManyAttempts = 6
    SystemUnavailable = 7
RedeemErrorStrings = {RedeemErrors.Success: 'Success',
 RedeemErrors.CodeDoesntExist: 'Invalid code',
 RedeemErrors.CodeIsInactive: 'Code is inactive',
 RedeemErrors.CodeAlreadyRedeemed: 'Code has already been redeemed',
 RedeemErrors.AwardCouldntBeGiven: 'Award could not be given',
 RedeemErrors.TooManyAttempts: 'Too many attempts, code ignored',
 RedeemErrors.SystemUnavailable: 'Code redemption is currently unavailable'}
MaxCustomCodeLen = config.ConfigVariableInt('tt-max-custom-code-len', 16).getValue()
