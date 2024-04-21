# Will contain datatypes and classes to be used in the AI section

import networkx as nx
from enum import Enum
from typing import Optional, Tuple, TypeAlias

class MapType(Enum):
    """
    Represents the different maps that can be played on.

    Attributes:
        CLASSIC: Original Risk map in physical board game.
        ASIA: Called "Asia 1800's" in Risk: Global domination. 48 territories, features large indonesia bonus. 
        US: Called "United States" in Risk: Global domination. 42 territories, features uniform blocky bonuses. 
    """
    CLASSIC = 1
    ASIA = 2
    US = 3


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

    Methods:
        __init__(name: str, age: int): Initializes a new instance of the Person class.
        introduce(): Prints an introduction message for the person.
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


