# Will contain datatypes and classes to be used in the AI section

import networkx as nx
from enum import Enum
from typing import Optional, Tuple, TypeAlias, TypedDict, List
from maps.mapStructures import Map, MapType
from .interface import *


class CardType(Enum):
    """
    Represents different card types gained after capturing at least 
    one territory during a turn.

    Attributes:
        INFANTRY: Weakest card, 3 give 4 troops.
        CAVALRY: Medium card, 3 give 6 troops.
        ARTILLERY: Strong card, 3 give 8 troops.
        WILD: Strongest card, can act as any of the above cards.
    """
    INFANTRY = 4
    CAVALRY = 6
    ARTILLERY = 8
    WILD = 10

class Card:
    """
    Represents a card that can be gained after capturing at least 
    one territory during a turn.

    Attributes:
        type (CardType): The type of card eg Infantry
        territory (int): The territory ID the card belongs to. 
    """
    def __init__(self, type : CardType, territory : int):
        self.type = type
        self.territory = territory


Cards: TypeAlias = list[Card]
"""
List of cards held by user player
"""

# List of actions carried out by the player or agent, with 
# specific information on the intention

Trade: TypeAlias = Optional[Tuple[CardType, CardType, CardType]]
"""
Represents whether a trade action is intending to be played. It will be 
None if no trade is occuring, otherwise it will be a tuple of three cards 
to be played in the order given. 
"""


DraftPlayer: TypeAlias = Tuple[Trade, list[(int, int)]]
"""
Represents the draft phase of the player to be taken. Holds The trade (if 
it will occur) and the associated cards, and a list of locations formatted 
as (territory ID, amount of troops) to place troops. 
"""


AttackPlayer: TypeAlias = list[Tuple[int, int, int, int]]
"""
Represents what attacks user player should make. Each tuple in 
list is one attack. Empty list means no attacks. ints are structured
as (territoryID from, territoryID to, amount of troops to attack with, amount of troops to move).
"""


FortifyPlayer: TypeAlias = Optional[Tuple[int, int, int]]
"""
Represents what fortify user player should make. If None, no fortify.
ints in tuple are structured as (territoryID from, territoryID to, amount of troops to move).
"""




MovePlayer: TypeAlias = Tuple[DraftPlayer, AttackPlayer, FortifyPlayer]
"""
Represents a full turn which a player should take. Will be the output of the AI agent.
"""



# List of actions played by opponent players, with outcome rather than intent info

TradeOpp: TypeAlias = Optional[Tuple[CardType, CardType, CardType]]
"""
Represents whether a trade action is intending to be played. It will be 
None if no trade is occuring, otherwise it will be a tuple of three cards 
to be played in the order given. 
"""


DraftOpp: TypeAlias = Tuple[Trade, list[(int, int)]]
"""
Represents the drafts an opponent took. Holds The trade (if 
it will occur) and the associated cards, and a list of locations formatted 
as (territory ID, amount of troops) to place troops. 
"""


AttackOpp: TypeAlias = list[Tuple[int, int, int, int, Optional[int]]]
"""
Represents the attacks an opponent took. Each tuple in 
list is one attack. Empty list means no attacks. ints are structured
as (territoryID from, territoryID to, defending troops lost, 
amount of attacking troops lost, amount of troops to move).
"""


FortifyOpp: TypeAlias = Optional[Tuple[int, int, int]]
"""
Represents what fortify user player should make. If None, no fortify.
ints in tuple are structured as (territoryID from, territoryID to, amount of troops to move).
"""




MoveOpp: TypeAlias = Tuple[DraftPlayer, AttackPlayer, FortifyPlayer]
"""
Represents a full turn which a player should take. Will be the output of the AI agent.
"""





Territories: TypeAlias = List[int]
"""
Represents a set of territories on the map. Each int represented the ID of a node. 
"""


# Consider how to be holding the data of the AI player. Could be in here with an added flag, 
# or could be a seperate structure. 
class PlayerDict(TypedDict):
    """
    Holds all neccessary details about each player in the game. Each entry is a player
    with the key being the player ID. 

    Attributes:
        -id (int): The ID number of the player. Note that ID is associated with their position
        in the round order. !ID 0 is first in round order.
         
        -colour (str): The physical colour of the player on the board for representation on nx graphs
        
        -troops (int): The amount of troops the player has. 0 troops means the player is dead.
        
        -diceAggression (int): A measure of how closely the player conforms to optimal balanced blitz play, 
        (eg always taking perfect rolls with 100% and minimal troops.) A higher number should indicate that 
        the player routinely takes risky 75% or less rolls and should guarded against with care. Also should 
        be considered less skillfull. 
        
        -territoryAggression (int): A measure of how likely the player is to take territories (perhaps for the 
        territory holding bonus). Note that this is very important to characterise and counteract the 
        behaviour of bots. 
        
        -bonusAggression (int): A measure of how often the player will go for bonuses, relative to how strong they are.
        This should be used to categorise the potential for a player over-extending, and how receptive they will be
        for you to take a bonus near them. 
        
        bonusesHeld (int): amount of bonuses held by the player.
        
        cardsHeld (int): amount of cards held by the player.
        
        dangerLevel (int): An overall measure of how dangerous the player is to the AI.
    """
    id: int
    colour: str
    troops: int
    territories: int
    diceAggression: int
    territoryAggression: int
    bonusAggression: int
    bonusesHeld: list[str]
    cardsHeld: int
    dangerLevel: int
        
        
        
# Should be num of players ^2 in size, worth enforcing?        
RelationShipMatrix: TypeAlias = list[list[int]]
"""
Represents the friendliness/aggression/vengance between every player in the game and each other.
Value at Matrix[x][y] is how player ID x feels about player ID y. Note that all values where 
x == y are irrelevant and will be 0. 
"""



# !note: Currently the user player is has data stored exactly the same as all other players, 
# with a simple differentiation to decide 
class GameState:
    """
    Main object which holds all variables needed to represent the game of Risk.

    Attributes:
        map (Map): The graph structure holding all territories, connections, and owners grouped
        with the bonuses and their values
        agentID (int) : The number ID of the user player which the AI agent plays as
        round (int): The current round number
        playerDict (PlayerDict): A dictionary holding details of all players for both display and 
        decision making
        relationsMatrix (RelationShipMatrix): A matrix holding the relationships between all players
        cards (Cards): A list of cards held by the user player 
    """
    def __init__(self, mapType: MapType, map: Map, agentID: int, round : int, playerDict : PlayerDict, playersAlive : list[int], relationsMatrix : RelationShipMatrix, cards : Cards):
        self.mapType = mapType
        self.map = map
        self.agentID = agentID
        self.round = round
        self.playerDict = playerDict
        self.playersAlive = playersAlive
        self.relationsMatrix = relationsMatrix
        self.cards = cards
        
        
        
    def __init__(self):
        self.mapType = getMapType()
        self.map = Map(self.mapType)
        self.playerList = getPlayersList()
        self.playersAlive = [i for i in range(len(self.playerList))]
        self.agentID = getAgentID(self.playerList)
        getTroopSetup(self.playerList, self.map)
        self.round = 1
        self.playerDict = {}
        
        # Initiliases playerDict with player IDs and colours
        for i in range(len(self.playerList)):
            # Correctly initialise other player data after deciding amounts
            self.playerDict[i] = {"id": i, "colour": self.playerList[i], "troops": 0, "territories": 0, "diceAggression": 0, "territoryAggression": 0, "bonusAggression": 0, "bonusesHeld": [], "cardsHeld": 0, "dangerLevel": 0}
            
        # Initialises all player troop totals correctly    
        for nodeID in self.map.nodes:
            currPlayer = self.map.nodes[nodeID]["player"]
            self.playerDict[currPlayer]["troops"] += self.map.nodes[nodeID]["troops"]
            self.playerDict[currPlayer]["territories"] += 1

            
        
        # Initilaises players relationship matrix with starting friendliness score of 50    
        self.relationsMatrix = [[0 for _ in range(len(self.playerList))] for _ in range(len(self.playerList))]
    
        # Players have no relationship with themselves, should always be 0
        for i in range(len(self.playerList)):
            for j in range(len(self.playerList)):
                if i == j:
                    self.relationsMatrix[i][j] = 0
                    
                    
        self.cards = []

        
        
        
    # Decide whether to have the heuristic as a method or a function in a separate file. 
    def heuristic(self) -> int:
        pass
    
    # Also decide whether to have functions like incrementing the turn, adding a card
       
