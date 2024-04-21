# Will contain datatypes and classes to be used in the AI section

import networkx as nx
from enum import Enum
from typing import Optional, Tuple, TypeAlias, TypedDict


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



Trade: TypeAlias = Optional[Tuple[CardType, CardType, CardType]]
"""
Represents whether a trade action is intending to be played. It will be 
None if no trade is occuring, otherwise it will be a tuple of three cards 
to be played in the order given. 
"""


# Should I keep as class or make type alias?
class Draft:
    """
    Represents the draft phase of the player to be taken.

    Attributes:
        trade (Trade): The trade (if it will occur) and the associated cards.
        drafts (list[(int, int)]): A list of locations formatted as (territory ID, amount of troops) to place troops.  
    """
    
    def __init__(self, trade: Trade, drafts : list[(int, int)]):
        self.trade = trade
        self.drafts = drafts


Attack: TypeAlias = list[Tuple[int, int, int, int]]
"""
Represents what attacks user player should make. Each tuple in 
list is one attack. Empty list means no attacks. ints are structured
as (territoryID from, territoryID to, amount of troops to attack with, amount of troops to move).
"""


Fortify: TypeAlias = Optional[Tuple[int, int, int]]
"""
Represents what fortify user player should make. If None, no fortify.
ints in tuple are structured as (territoryID from, territoryID to, amount of troops to move).
"""

# Consider how to be holding the data of the AI player. Could be in here with an added flag, 
# or could be a seperate structure. 
class PlayerDict(TypedDict):
    """
    Holds all neccessary details about each player in the game. Each entry is a player
    with the key being the player ID. 

    Attributes:
        -id (int): The ID number of the player. Note that ID is associated with their position
        in the turn order. ID 1 is first in turn order.
         
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




class GameState:
    """
    Holds all variables needed to represent a game

    Attributes:
        graph (nx.Graph): The graph structure holding all
        drafts (list[(int, int)]): A list of locations formatted as (territory ID, amount of troops) to place troops.  

    Methods:
        __init__(self, graph: nx.Graph, turn : int, playerDict : PlayerDict, playerRelations
        : RelationShipMatrix, cards : Cards)): Initializes a new instance of the GameState class.
    """
    def __init__(self, graph: nx.Graph, turn : int, playerDict : PlayerDict, playerRelations : RelationShipMatrix, cards : Cards):
        self.graph = graph
        self.playerDict = playerDict
        self.playerRelations = playerRelations
        self.cards = cards