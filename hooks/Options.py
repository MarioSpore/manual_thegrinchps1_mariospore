# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionList

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class KeyType(Choice):
    """Selects whether you want your access items to be separated or progressive"""
    display_name = "Key Type"
    option_separated = 0
    option_progressive = 1
    default = 0

class StartingArea(Choice):
    """
    Here, you can select which area you'll start the game with. Whichever one you pick is the region you'll have access to at the start of the Multiworld.
    """
    option_whoville = 0
    option_who_forest = 1
    option_who_dump = 2
    option_who_lake = 3
    display_name = "Starting Area"

class Missions(DefaultOnToggle):
    """This allows missions that can be completed to be considered checks. (22 locations)"""
    display_name = "Mission Checks"

class Blueprints(DefaultOnToggle):
    """Every blueprint collected is a check. (67 locations)"""
    display_name = "Blueprint Sanity"

class StoneHearts(DefaultOnToggle):
    """Every time you collect a Heart-Of-Stone, it gives you a check. (4 locations)"""
    display_name = "Heart of Stone Sanity"
    
class Visitsanity(DefaultOnToggle):
    """Everytime you enter a loading zone of a particular area for the first time is a check. (16 locations)"""
    display_name = "VisitSanity"
    
class Supadow(Toggle):
    """Enables completing minigames through the Supadows in Mount Crumpit as checks. (9 locations)"""
    display_name = "Supadow Minigame Checks"
    
class Gifts(Toggle):
    """Missions that require you to squash every present in a level. (4 locations)"""
    display_name = "Gift Collection"

class Max(Toggle):
    """Adds Max the dog to the item pool with his logic built around him. (1 progressive item)"""
    display_name = "Cheats"

class Cheats(Toggle):
    """Throws new items in that allows you to enable cheats through the emulator. (1 useful item)"""
    display_name = "Cheats"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["key_preference"] = KeyType
    options["starting_area"] = StartingArea
    options["missions"] = Missions
    options["blueprintsanity"] = Blueprints
    options["heartsanity"] = StoneHearts
    options["visitsanity"] = Visitsanity
    options["supadow"] = Supadow
    options["sqaush_all_gifts_missions"] = Gifts
    options["randomize_max"] = Max
    options["cheats"] = Cheats
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    return options