# Framework to encode all abstract actions, provide pruning 
# # techniques and describe their purpose. 
from enum import Enum
from typing import TypeAlias, Set
from .structures import GameState


class ActionType(Enum):
    """
    Represents different card types gained after capturing at least 
    one territory during a turn.

    """
    KILLPLAYER = 1
    TAKEBONUS = 2
    BREAKBONUS = 3
    EXPANDBORDERS = 6 
    MIGRATE = 8
    TAKETERRITORIES = 9
    TAKECARD = 10
    DEFENDBORDERS = 11
    NOATTACK = 13
    
    
# Going with attack/foritfy territory list underpinning actions. 
# This controls the graph structure of action sequencing. 
actionSequenceDict = {
    ActionType.KILLPLAYER: [act for act in ActionType if act not in {ActionType.TAKECARD, ActionType.DEFENDBORDERS, 
                                                                     ActionType.NOATTACK}],
    ActionType.TAKEBONUS: [act for act in ActionType if act not in {ActionType.KILLPLAYER, ActionType.TAKECARD, 
                                                                    ActionType.DEFENDBORDERS, ActionType.NOATTACK}],
    ActionType.BREAKBONUS: [act for act in ActionType if act not in {ActionType.KILLPLAYER, ActionType.TAKEBONUS,
                                                                     ActionType.TAKECARD, ActionType.DEFENDBORDERS, 
                                                                     ActionType.NOATTACK}],
    ActionType.EXPANDBORDERS: [ActionType.EXPANDBORDERS, ActionType.TAKETERRITORIES],
    ActionType.MIGRATE: [ActionType.TAKETERRITORIES],
    ActionType.TAKETERRITORIES: [ActionType.TAKETERRITORIES],
    ActionType.TAKECARD: [ActionType.DEFENDBORDERS],
    ActionType.DEFENDBORDERS: [],
    ActionType.NOATTACK: []
}


    

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
        
    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return self.action == other.action

    def __hash__(self):
        return hash(self.action)



# !These are all a very rough draft of the action implementations. Some might be 
# entirely removed or combined, and the parameters to most will be significantly changed. 

# !NOTE: All action classes will have a prune method which will take the gamestate 
# and output a boolean for the pruning discussed in pruneActionNodes().
class KillPlayer(Action):
    """
    Kill a player by taking all their territories.

    Attributes:
        player (int): The player ID of the player to be killed.
        territories (Set[int]): The territories needed to capture to achieve this
    """
    def __init__(self, player : int, territories : Set[int]):
        super().__init__(ActionType.KILLPLAYER)
        self.player = player
        # Decide later on whether to keep kill path in this action, 
        # and how to store it. 
        self.territories = territories
        
    def __eq__(self, other):
        if not isinstance(other, KillPlayer):
            return False
        return self.player == other.player
    
    def __hash__(self):
        return hash((self.player, self.territories))
    

def generateKPSet(player : int, gameState: GameState) -> Set[KillPlayer]:
    """
    Generates all possible KillPlayer actions for each alive player. 
    """
    actions = set()
    for aliveP in gameState.playersAlive:
        if aliveP != player:
            actions.add(KillPlayer(aliveP, gameState.playerDict[aliveP]["territories"]))
    return actions



class TakeBonus(Action):
    """
    Take a bonus by taking all territories in the bonus. Could be on 
    "neutral" territory not explicitly owned by any player, or could 
    be an action directly contesting a bonus. 

    Attributes:
        player (int): The ID of the player whose bonus is getting stolen.
        !Should be None or 0 if neutral territory.
        bonus (str): The bonus to be taken
        territories (Set[int]): The territories needed to capture to achieve this

    """
    def __init__(self, player : int, bonus : str, territories : Set[int]):
        super().__init__(ActionType.TAKEBONUS)
        self.player = player
        # Decide later on whether to keep the path in this action, 
        # and how to store it. 
        self.territories = territories
        # Also decide how bonuses should be represented. Currently all 
        # bonuses have a specific enumeration, could I make this 
        # have a central class?
        self.bonus = bonus
    

        def __eq__(self, other):
                if not isinstance(other, TakeBonus):
                    return False
                return self.bonus == other.bonus
            
        def __hash__(self):
            return hash((self.player, self.territories, self.bonus))


class BreakBonus(Action):
    """
    Break a bonus owned by a player by taking a territory in that bonus. 
    Should preferrably be the weakest link of defences or done in a 
    way disallowing retaliation. 

    Attributes:
        player (int): The ID of the player whose bonus is getting broken.
        bonus (str): The bonus to be broken
        territory (int): The territories needed to capture to achieve this

    """
    def __init__(self, player : int, bonus : str, territory : int):
        super().__init__(ActionType.BREAKBONUS)
        self.player = player
        # Decisions as mentioned above
        self.territory = territory
        # Decisions as mentioned above
        self.bonus = bonus
    

    def __eq__(self, other):
        if not isinstance(other, BreakBonus):
            return False
        return self.bonus == other.bonus

    def __hash__(self):
            return hash((self.player, self.territory, self.bonus))




class ExpandBorders(Action):
    """
    Increase territory control by taking more territories. This should usually 
    be to find strong choke points for defending borders, or gearing up to 
    take a bonus.

    Attributes:
        territories (int): The territory IDs to expand to

    """
    def __init__(self, territories : Set[int]):
        super().__init__(ActionType.EXPANDBORDERS)
        self.territories = territories
    

    def __eq__(self, other):
        if not isinstance(other, ExpandBorders):
            return False
        return self.territories == other.territories
    
    def __hash__(self):
            return hash(self.territories)



class DefendBorders(Action):
    """
    Add troops to borders of territory clusters or bonuses to make 
    them less likely to be attacked.

    Attributes:
        borders (Set[int]): The border territories to strengthen
    """
    def __init__(self, borders : Set[int]):
        super().__init__(ActionType.DEFENDBORDERS)
        self.borders = borders
    

    def __eq__(self, other):
        return isinstance(other, DefendBorders)


class TakeCard(Action):
    """
    Attack a single territory that has low troops to ensure a card is taken.
    Preferrably should be an attack with perfect dice

    Attributes:
        attack (int): The territory ID to take a card in
    """
    def __init__(self, attack : int):
        super().__init__(ActionType.TAKECARD)
        self.attack = attack
    

    def __eq__(self, other):
        return isinstance(other, TakeCard)


# Could be combined with flee by implementing a more robust location 
# selecting algorithm
class Migrate(Action):
    """
    Migrate dense stacks of troops from one region of the map to another, 
    usually for capturing bonuses.

    Attributes:
        territory (int): The end goal territory ID
    """
    def __init__(self, territory : int):
        super().__init__(ActionType.MIGRATE)
        self.territory = territory
    
    def __eq__(self, other):
        return isinstance(other, Migrate)

# !Could be implemented with the iterative deepening search that on depth 1 
# calculates only taking territories 1 step away etc.
class TakeTerritories(Action):
    """
    Simply attack a territory, intended to be a "catch all" to
    encapsulate all other possible behaviours. 

    Attributes:
        territory (int): The end goal territory ID

    """
    def __init__(self, territory : int):
        super().__init__(ActionType.TAKETERRITORIES)
        self.territory = territory
    

    def __eq__(self, other):
        if not isinstance(other, TakeTerritories):
            return False
        return self.territory == other.territory


class NoAttack(Action):
    """
    Do not attack, or take a card. Perhaps do not fortify.
    """
    def __init__(self):
        super().__init__(ActionType.NOATTACK)


ActionSeq: TypeAlias = Set[Action]