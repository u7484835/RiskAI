import networkx as nx
from enum import Enum
from typing import TypedDict

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
    

# Eventually provide a class which helps to enumerator bonuses, make that ID and make there 
# a str name. Then make each bonus have an Enum which denotes NA, SA, AF, EU, AS, AU etc, and then 
# have them in this dict. 
class Bonuses(TypedDict):
    id: str
    bonus: int
    
    
"""
Represents whether a trade action is intending to be played. It will be 
None if no trade is occuring, otherwise it will be a tuple of three cards 
to be played in the order given. 
"""


class Map:
    """
    Represents a map to be played on.

    Attributes:
        nodes (dict): A dictionary of nodes with key as node ID and value as a dictionary with the following keys:
            name (str): The name of the territory.
            troops (int): The amount of troops on the territory.
            player (int): The player ID that owns the territory.
            bonus (str): The bonus the territory belongs to.
        edges (list): A list of edges with each edge as a tuple of two node IDs. 
    """
    def __init__(self, graph : nx.Graph, bonuses : list):
        self.graph = graph
        self.edges = edges