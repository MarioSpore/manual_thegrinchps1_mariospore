# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState
from Options import OptionError

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    if world.options.squash_all_gifts_missions.value == True and world.options.missions.value = False:
        logging.info(f"Force enabling option missions from {player}'s world")
        world.options.missions.value == True
    if world.options.missions.value == False and world.options.blueprintsanity.value == False and world.options.heartsanity.value == False and world.options.supadow.value == False and world.options.sqaush_all_gifts_missions.value == False and world.options.visitsanity.value == False:
        raise OptionError(f"This is MY Christmas! You are attempting to generate a seed with no locations! Make sure you enable at LEAST one option for a playable game. - MarioSpore")
    if world.options.missions.value == False or world.options.blueprintsanity.value == False:
        raise OptionError(f"Ouch! It's unbearable! You are attempting to generate a seed with not enough locations! Please enable both missions or blueprintsanity to ensure the generator is able to place the necessary items into the pool. - MarioSpore")
    if world.options.starting_area.value == 2 and world.options.visitsanity.value == False:
        # world.options.starting_area.value == 0 or world.options.starting_area.value == 1 or world.options.starting_area.value == 3
        raise OptionError(f"Ya Grinched! Currently, Who Dump has no sphere 1 locations due to how the logic is designed at the moment. Please enable visitsanity to guarantee a sphere 1 location. - MarioSpore")
    if world.options.starting_area.value == 1 and world.options.blueprintsanity.value == False and world.options.visitsanity.value == False:
        raise OptionError(f"My plans! My precious plans! Who Forest does not have any starting locations for missions! Please enable either blueprintsanity or visitsanity if you still want to start in this area. - MarioSpore")
    if world.options.starting_area.value == 3 and world.options.blueprintsanity.value == False and world.options.visitsanity.value == False:
        raise OptionError(f"Gotcha! Who Lake does not have any starting locations for missions! Please enable either blueprintsanity or visitsanity if you still want to start in this area. - MarioSpore")
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    if world.options.heartsanity.value == 1:
        itemNamesToRemove = ["Heart of Stone"] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    world.filler_item_name = "Present"
    starting_area = world.options.starting_area.value
    if world.options.starting_area.value == 0:
        starting_items = ["Whoville Access Key"]
    if world.options.starting_area.value == 1:
        starting_items = ["Who Forest Access Key"]
    if world.options.starting_area.value == 2:
        starting_items = ["Who Dump Access Key"]
        # starting_items = ["Who Dump Access Key", "Rotten Egg Launcher", "Rocket Spring"]
    if world.options.starting_area.value == 3:
        starting_items = ["Who Lake Access Key"]
    for itemName in starting_items:
        item = next((i for i in item_pool if i.name == itemName), None)
        if item is None:
           continue
        multiworld.push_precollected(item)
        item_pool.remove(item)
    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
