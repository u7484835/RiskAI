# Framework to encode all abstract actions, provide pruning 
# # techniques and describe their purpose. 
from enum import Enum


class ActionType(Enum):
    """
    Represents different card types gained after capturing at least 
    one territory during a turn.

    """
    KILLPLAYER = 1
    TAKEBONUS = 2
    BREAKBONUS = 3
    HITSTACK = 4
    CHIPPLAYER = 5
    EXPANDBORDERS = 6
    CREATEPOSITION = 7
    DEFENDBORDERS = 8
    TAKECARD = 9
    MIGRATE = 10
    TAKETERRITORIES = 11
    FLEE = 12
    NOATTACK = 13
    
    

class Action:
    """
    Big class inherited by all action implementations.

    Attributes:
        map (Map): The graph structure holding all territories, connections, and owners grouped


    Methods:
        heuristic() : Calculates how favourable the current GameState is. 
    """
    def __init__(self, action: ActionType):
        self.action = action



# !These are all a very rough draft of the action implementations. Some might be 
# entirely removed or combined, and the parameters to most will be significantly changed. 
class KillPlayer(Action):
    """
    Kill a player by taking all their territories.

    Attributes:
        player (int): The player ID of the player to be killed.
        path (list[int]): The attack moves needed to take the kill
    """
    def __init__(self, player : int, path : list[int]):
        self.player = player
        # Decide later on whether to keep kill path in this action, 
        # and how to store it. 
        self.path = path
    pass



class TakeBonus(Action):
    """
    Take a bonus by taking all territories in the bonus. Could be on 
    "neutral" territory not explicitly owned by any player, or could 
    be an action directly contesting a bonus. 

    Attributes:
        player (int): The ID of the player whose bonus is getting stolen.
        !Should be None or 0 if neutral territory.
        bonus (str): The bonus to be taken
        path (list[int]): The attack moves needed to take the bonus

    """
    def __init__(self, player : int, bonus : str, path : list[int]):
        self.player = player
        # Decide later on whether to keep the path in this action, 
        # and how to store it. 
        self.path = path
        # Also decide how bonuses should be represented. Currently all 
        # bonuses have a specific enumeration, could I make this 
        # have a central class?
        self.bonus = bonus
    pass


class BreakBonus(Action):
    """
    Break a bonus owned by a player by taking a territory in that bonus. 
    Should preferrably be the weakest link of defences or done in a 
    way disallowing retaliation. 

    Attributes:
        player (int): The ID of the player whose bonus is getting broken.
        bonus (str): The bonus to be broken
        path (list[int]): The attack moves needed to break the bonus

    """
    def __init__(self, player : int, bonus : str, path : list[int]):
        self.player = player
        # Decisions as mentioned above
        self.path = path
        # Decisions as mentioned above
        self.bonus = bonus
    pass



class HitStack(Action):
    """
    Attack a player by taking a territory which has a very high 
    concentration of their troops.

    Attributes:
        player (int): The ID of the player to attack
        territory (int): The territory ID to hit
        path (list[int]): The attack moves needed to attack it

    """
    def __init__(self, player : int, territory : int, path : list[int]):
        self.player = player
        self.path = path
        # Might be unnecessary as path should terminate at said territory. 
        # That said, it is useful for action generation rather than calculation. 
        self.territory = territory
    pass

class ChipPlayer(Action):
    """
    Attack a player's (likely smaller) territories to weaken them.

    Attributes:
        player (int): The ID of the player to attack
        territories (int): The territory IDs to hit
        path (list[int]): The attack moves needed to attack it

    """
    def __init__(self, player : int, territories : list[int], path : list[int]):
        self.player = player
        self.path = path
        self.territories = territories
    pass


class ExpandBorders(Action):
    """
    Increase territory control by taking more territories. This should usually 
    be to find strong choke points for defending borders, or gearing up to 
    take a bonus.

    Attributes:
        territories (int): The territory IDs to expand to
        path (list[int]): The attack moves needed to expand

    """
    def __init__(self, territories : list[int], path : list[int]):
        self.territories = territories
        self.path = path
    pass


class CreatePosition(Action):
    """
    Migrate some troops to an unconstested region for survivablility.
    
    Attributes:
        territory (int): The end goal territory ID
        path (list[int]): The attack moves needed to own that territory

    """
    def __init__(self, territories : int, path : list[int]):
        self.territories = territories
        self.path = path
    pass


class DefendBorders(Action):
    """
    Add troops to borders of territory clusters or bonuses to make 
    them less likely to be attacked.

    Attributes:
        borders (list[int]): The border territories to strengthen
    """
    def __init__(self, borders : list[int]):
        self.borders = borders
    pass

class TakeCard(Action):
    """
    Attack a single territory that has low troops to ensure a card is taken.
    Preferrably should be an attack with perfect dice

    Attributes:
        attack (int): The territory ID to take a card in
    """
    def __init__(self, attack : int):
        self.attack = attack
    pass


# Could be combined with flee by implementing a more robust location 
# selecting algorithm
class Migrate(Action):
    """
    Migrate dense stacks of troops from one region of the map to another, 
    usually for capturing bonuses.

    Attributes:
        territory (int): The end goal territory ID
        path (list[int]): The attack moves needed to own that territory

    """
    def __init__(self, territories : int, path : list[int]):
        self.territories = territories
        self.path = path
    pass

# !Could be implemented with the iterative deepening search that on depth 1 
# calculates only taking territories 1 step away etc.
class TakeTerritories(Action):
    """
    Simply attack close territories, intended to be a "catch all" to
    encapsulate all other possible behaviours. 

    Attributes:
        territories (list[int]): The territories to attack

    """
    def __init__(self, territories : list[int]):
        self.territories = territories
    pass


# Fortify action not included here but should be? Or would it be calculated 
# by simply also fortifying to desired location
class Flee(Action):
    """
    Migrate majority of troops away from dangerous players for survival.

    Attributes:
        territory (int): The end goal territory ID
        path (list[int]): The attack moves needed to own that territory

    """
    def __init__(self, territories : int, path : list[int]):
        self.territories = territories
        self.path = path
    pass

class NoAttack(Action):
    """
    Do not attack, or take a card. Perhaps do not fortify.
    """
    pass