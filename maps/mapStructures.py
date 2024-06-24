import networkx as nx
from enum import Enum
from typing import TypedDict
from .classic import *

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
    
    @classmethod
    def from_str(cls, name: str) -> "MapType":
        """
        Converts a string to a MapType enum.
        """
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"Invalid map name: {name}")
    


class Map:
    """
    Represents a map to be played on.

    Attributes:
        graph (nx.Graph): A networkx graph representing the map, with each node representing a territory.
        bonuses (dict): A dictionary corresponding each bonus to the troops awarded if all territories are held. 
    """
    def __init__(self, mapType : MapType):
        match mapType:
            case MapType.CLASSIC:
                self.mapType = mapType
                self.graph = Classic
                self.bonuses = classicBonusDict
                
            # Currently do not have asia implemented but showing how it would be instantiated.
            case MapType.ASIA:
                self.mapType = mapType
                self.graph = Classic
                self.bonuses = classicBonusDict # should be AsiaBonusVals
                
        # Adds territory names for interface        
        self.territoryNames = [node["name"] for _, node in sorted(self.graph.nodes(data=True), key=lambda x: x[0])]


        # Adds list of border territories for calculations
        self.borderTerr = set()
        # Iterates through all nodes, checking if it has a border with a non-bonus territory
        for node in self.graph.nodes():
            # map.graph.nodes[node]["bonus"] gets bonus of node
            # map.bonuses[bonus]["territories"] gets territories for bonus 
            # Function checks if a node has any neighbours not in the bonus. If so, it is 
            # a border territory.
            if any(neighbour not in self.bonuses[(self.graph.nodes[node]["bonus"])]["territories"] for neighbour in self.graph.neighbors(node)):          
                self.borderTerr.add(node)
