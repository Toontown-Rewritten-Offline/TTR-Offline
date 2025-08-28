from toontown.toonbase import ToontownGlobals
from . import SellbotScrapFactorySpec
from . import SellbotScrapFactoryCogs
from . import SellbotSteelFactorySpec
from . import SellbotSteelFactoryCogs
from . import LawbotLegFactorySpec
from . import LawbotLegFactoryCogs

def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]


def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]


FactorySpecModules = {ToontownGlobals.SellbotScrapFactoryInt: SellbotScrapFactorySpec,
                      ToontownGlobals.SellbotSteelFactoryInt: SellbotSteelFactorySpec,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec}
CogSpecModules = {ToontownGlobals.SellbotScrapFactoryInt: SellbotScrapFactoryCogs,
                  ToontownGlobals.SellbotSteelFactoryInt: SellbotSteelFactoryCogs,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs}
if __dev__:
    from . import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec
    from . import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
