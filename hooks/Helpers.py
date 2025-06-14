from typing import Optional
from BaseClasses import MultiWorld
from .. import Helpers
from ..Locations import ManualLocation
from ..Items import ManualItem


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if category_name == "Separated" or "Progressive":
        selection = Helpers.get_option_value(multiworld, player, "key_preference")
        if category_name == "Separated":
            if selection == 0:
                return True
            elif selection == 1:
                return False
        if category_name == "Progressive":
            if selection == 1:
                return True
            elif selection == 0:
                return False
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    return None
