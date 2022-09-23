from . import PrizeInvalidItem
from . import PrizeThrowableItem
INVALID_ITEM = 0
THROWABLE_ITEM = 1
CatalogItemTypes = {PrizeInvalidItem.PrizeInvalidItem: INVALID_ITEM,
 PrizeThrowableItem.PrizeThrowableItem: THROWABLE_ITEM}
CatalogItemType2multipleAllowed = {INVALID_ITEM: False,
 THROWABLE_ITEM: True}
PrizeItemTypeMask = 31
PrizeItemSaleFlag = 128
PrizeItemGiftTag = 64
