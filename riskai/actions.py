# Framework to encode all abstract actions, provide pruning 
# # techniques and describe their purpose. 
from enum import Enum
from typing import TypeAlias, Set, Optional
from .structures import GameState, Territories


class ActionType(Enum):
    """
    Represents different card types gained after capturing at least 
    one territory during a turn.

    """
    KILLPLAYER = 1 # player terrs
    TAKEBONUS = 2 # bonus terrs
    BREAKBONUS = 3 # bonus terr? 
    EXPANDBORDERS = 6 # expand terrs
    TAKETERRITORIES = 9 # take terrs
    TAKECARD = 10 # card terr
    NOATTACK = 13
    
    
# Going with attack/foritfy territory list underpinning actions. 
# This controls the graph structure of action sequencing. 
actionSequenceDict = {
    ActionType.KILLPLAYER: [act for act in ActionType if act not in {ActionType.TAKECARD, ActionType.NOATTACK}],
    ActionType.TAKEBONUS: [act for act in ActionType if act not in {ActionType.KILLPLAYER, ActionType.TAKECARD, 
                                                                     ActionType.NOATTACK}],
    ActionType.BREAKBONUS: [act for act in ActionType if act not in {ActionType.KILLPLAYER, ActionType.TAKEBONUS,
                                                                     ActionType.TAKECARD, ActionType.NOATTACK}],
    ActionType.EXPANDBORDERS: [ActionType.EXPANDBORDERS, ActionType.TAKETERRITORIES],
    ActionType.TAKETERRITORIES: [ActionType.TAKETERRITORIES],
    ActionType.TAKECARD: [],
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
    """
    def __init__(self, player : int):
        super().__init__(ActionType.KILLPLAYER)
        self.player = player
        # Decide later on whether to keep kill path in this action, 
        # and how to store it. 
        
    def __eq__(self, other):
        if not isinstance(other, KillPlayer):
            return False
        return self.player == other.player
    
    def __hash__(self):
        return hash(self.player)
    

def generateKPSet(player : int, gameState: GameState) -> Set[KillPlayer]:
    """
    Generates all possible KillPlayer actions for each alive player. 
    """
    return {KillPlayer(aliveP) for aliveP in gameState.playersAlive if aliveP != player}


def kpData(gameState : GameState, kp : KillPlayer) -> Optional[Territories]:
    return gameState.playerDict[kp.player]["territories"]


class TakeBonus(Action):
    """
    Take a bonus by taking all territories in the bonus. Could be on 
    "neutral" territory not explicitly owned by any player, or could 
    be an action directly contesting a bonus. 

    Attributes:
        player (int): The ID of the player whose bonus is getting stolen.
        !Should be None neutral territory.
        bonus (str): The bonus to be taken

    """
    def __init__(self, bonus : str, player : int):
        super().__init__(ActionType.TAKEBONUS)
        # Also decide how bonuses should be represented. Currently all 
        # bonuses have a specific enumeration, could I make this 
        # have a central class?
        self.bonus = bonus
        self.player = player

        def __eq__(self, other):
                if not isinstance(other, TakeBonus):
                    return False
                return self.bonus == other.bonus
            
        def __hash__(self):
            return hash((self.player, self.bonus))


def generateTBSet(player : int, gameState: GameState) -> Set[TakeBonus]:
    """
    Generates all possible Take Bonus actions for all bonuses. 
    """
    
    actions = set()
    for bonus in gameState.map.bonuses.keys():
        if bonus not in gameState.playerDict[player]["bonusesHeld"]:
            owningPlayer = None
            for player in gameState.playersAlive:
                if bonus in gameState.playerDict[player]["bonusesHeld"]:
                    owningPlayer = player
                    break
            actions.add(TakeBonus(bonus, owningPlayer))

    return actions

def tbData(gameState : GameState, tb : TakeBonus) -> Optional[Territories]:
    return gameState.map.bonuses[tb.bonus]["territories"]

class BreakBonus(Action):
    """
    Break a bonus owned by a player by taking a territory in that bonus. 
    Should preferrably be the weakest link of defences or done in a 
    way disallowing retaliation. 

    Attributes:
        player (int): The ID of the player whose bonus is getting broken.
        bonus (str): The bonus to be broken

    """
    def __init__(self, player : int, bonus : str):
        super().__init__(ActionType.BREAKBONUS)
        self.player = player
        # Decisions as mentioned above
        self.bonus = bonus
    

    def __eq__(self, other):
        if not isinstance(other, BreakBonus):
            return False
        return self.bonus == other.bonus

    def __hash__(self):
            return hash((self.player, self.bonus))


def generateBBSet(player : int, gameState: GameState) -> Set[BreakBonus]:
    """
    Generates all possible Break Bonus actions for all bonuses. 
    """
    return {
        BreakBonus(aliveP, bonus)
        for aliveP in gameState.playersAlive if aliveP != player
        for bonus in gameState.playerDict[aliveP]["bonusesHeld"]
    }


def bbDataWeakest(gameState : GameState, bb : BreakBonus) -> Optional[Territories]:
    bonusBorders = gameState.map.bonuses[bb.bonus]["territories"] & gameState.map.borderTerr
    
    minTroops = float("inf")
    minTerr = None
    
    for terr in bonusBorders:
        if gameState.map.graph.nodes[terr]["troops"] < minTroops:
            minTroops = gameState.map.graph.nodes[terr]["troops"]
            minTerr = terr
        
    return {minTerr}




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
        
        
def ebData(gameState : GameState, eb : ExpandBorders) -> Optional[Territories]:
    """
    Finds the territory which is a bonus border adjacent to the agent's territories
    with the least troops to capture. 
    """
    borders = set()
    
    for border in gameState.map.borderTerr:
        if gameState.map.graph.nodes[border]["player"] != gameState.agentID:
            if any(neighbour in gameState.playerDict[gameState.agentID]["territories"] for neighbour in gameState.map.graph.neighbors(border)):
                borders.add(border)
                
                
    if len(borders) == 0:
        return None
    
    minTroops = float("inf")
    minTerr = None
    
    for terr in borders:
        if gameState.map.graph.nodes[terr]["troops"] < minTroops:
            minTroops = gameState.map.graph.nodes[terr]["troops"]
            minTerr = terr
        
    return {minTerr}

        
        
# Generateing solo set element because expand borders locations should be chosen on calulation. 
# Not sure whether that should be here or in actual pre-MST calculations?
def generateEBSet() -> Set[ExpandBorders]:
    """
    Generates all possible Expand borders actions set.
    """
    return {ExpandBorders(None)}



# NOTE: Messy mismatch between class definition and practical usage. 
# attack will never be used, essentially a dummy class as ebData is 
# doing all territory work. 
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
    

    def __hash__(self):
        return hash(self.attack)



def generateTCSet() -> Set[TakeCard]:
    """
    Generates singleton take card action set.
    """
    return {TakeCard(None)}


def tcData(gameState : GameState) -> Optional[Territories]:
    """
    Calculates the adjacent territory with the least troops to take attack.
    """
    neighbours = set()
    
    for owned in gameState.playerDict[gameState.agentID]["territories"]:
        for neighbour in gameState.map.graph.neighbors(owned):
            if gameState.map.graph.nodes[neighbour]["player"] != gameState.agentID:
                neighbours.add(neighbour)
    
    
    minTroops = float("inf")
    minTerr = None
    
    for terr in neighbours:
        if gameState.map.graph.nodes[terr]["troops"] < minTroops:
            minTroops = gameState.map.graph.nodes[terr]["troops"]
            minTerr = terr
        
    return {minTerr}


    

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
    
    def __hash__(self):
        return hash(self.territory)
    
    
def generateTTSet() -> Set[TakeTerritories]:
    """
    Generates singleton taketerritories action set.
    """
    return {TakeTerritories(None)}    


def ttData(gameState : GameState, amount : int) -> Optional[Territories]:
    """
    Adds as many territories as possible to take until amount is reached. Adds territories 
    in a breadth first fashion. While loop ensures that the function continues until 
    all territories are added or the correct amount of random territories to take are reached. 
    """
    # Initialises looping vars
    toTake = set()
    addFlag = True
    
    # Halt when no more terrs can be added
    while addFlag:
        addFlag = False  
        # Consider the neighbours of all owned terrs and all terrs planned to attack
        loopTerr = gameState.playerDict[gameState.agentID]["territories"] | toTake
        for owned in loopTerr:
            for neighbour in gameState.map.graph.neighbors(owned):
                # Check that terr to add is new
                if neighbour not in loopTerr:
                    addFlag = True 
                    toTake.add(neighbour)
                    # If amount has been met then return 
                    if len(toTake) == amount:
                        return toTake
                    
    return toTake


class NoAttack(Action):
    """
    Do not attack, or take a card. Perhaps do not fortify.
    """
    def __init__(self, terr):
        super().__init__(ActionType.NOATTACK)
        self.terr = terr
    
    def __hash__(self):
        return hash(self.terr)
        

def generateNASet() -> Set[NoAttack]:
    """
    Generates singleton no attack action set.
    """
    return {NoAttack(None)}    


ActionSet: TypeAlias = Set[Action]