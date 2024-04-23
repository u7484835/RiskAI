# Framework to encode all abstract actions, provide pruning 
# # techniques and describe their purpose. 
from enum import Enum


class ActionType(Enum):
    """
    Represents different card types gained after capturing at least 
    one territory during a turn.

    Attributes:
        KILLPLAYER: Kill a player by taking all their territories.
        TAKEBONUS: Take a bonus by taking all territories in the bonus.
        BREAKBONUS: Break a bonus owned by a player by taking a territory in that bonus.
        HITSTACK: Attack a player by taking a territory which has a very 
        high concentration of their troops.
        MIGRATE: Migrate dense stacks of troops from one region of the map to another, 
        usually for capturing bonuses. 
        FLEE: Migrate majority of troops away from dangerous players for survival. 
        CHIPPLAYER: Attack a player's smaller territories to weaken them.
        CREATEPOSITION: Migrate some troops to an unconstested region for survivablility. 
        DEFENDBORDERS: Add troops to borders of territory clusters or bonuses.
        EXPANDBORDERS: Increase territory control by taking more territories. This should 
        usually be to find strong choke points for defending borders, or gearing up to 
        take a bonus.
        TAKECARD: Attack a single territory with low troops to ensure a card is taken.
        TAKETERRITORIES: Simply attack close territories, intended to be a "catch all" to
        encapsulate all other possible behaviours. Could be implemented with the iterative deepening 
        search that on depth 1 calculates only taking territories 1 step away etc.
        NOATTACK: Do not attack, or take a card. Perhaps do not fortify.
    """
    KILLPLAYER = 1
    TAKEBONUS = 2
    BREAKBONUS = 3
    HITSTACK = 4
    MIGRATE = 5
    FLEE = 6
    CHIPPLAYER = 7
    CREATEPOSITION = 8
    DEFENDBORDERS = 9 
    EXPANDBORDERS = 10
    TAKECARD = 11
    TAKETERRITORIES = 12
    NOATTACK = 13
    
    
    """
    List of actions in camelCase for developement, ignore
    
    killPlayer = 1
    takeBonus = 2
    breakBonus = 3
    hitStack = 4
    migrate = 5
    flee = 6
    chipPlayer = 7
    createPosition = 8
    defendBorders = 9 
    expandBorders = 10
    takeCard = 11
    takeTerritories = 12
    noAttack = 13
    """
    

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
