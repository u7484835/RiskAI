import networkx as nx
from enum import Enum
from typing import TypedDict
from classic import *

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
    



class Map:
    """
    Represents a map to be played on.

    Attributes:
        graph (nx.Graph): A networkx graph representing the map, with each node representing a territory.
        bonuses (dict): A dictionary corresponding each bonus to the troops awarded if all territories are held. 
    """
    def __init__(self, map : MapType):
        match map:
            case MapType.CLASSIC:
                self.graph = Classic
                self.bonuses = classicBonusVals
            # Currently do not have asia implemented but showing how it would be instantiated.
            case MapType.ASIA:
                self.graph = Classic
                self.bonuses = classicBonusVals # should be AsiaBonusVals
