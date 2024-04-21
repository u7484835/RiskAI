import networkx as nx
from enum import Enum


class ClassicBonus(Enum):
    """
    Represents different bonuses for the classic map

    Attributes:
        NORTHAMERICA: North America bonus
        EUROPE: Europe bonus
        ASIA: Asia bonus
        SOUTHAMERICA: South America bonus
        AFRICA: Africa bonus
        AUSTRALIA: Australia bonus
    """
    NORTHAMERICA = 1
    EUROPE = 2
    ASIA = 3
    SOUTHAMERICA = 4
    AFRICA = 5
    AUSTRALIA = 6
    

classicBonuses = {
    ClassicBonus.NORTHAMERICA: {
        "name": "NA",
        "bonus": 5
    },
    ClassicBonus.EUROPE: {
        "name": "EU",
        "bonus": 5
    },
    ClassicBonus.ASIA: {
        "name": "EU",
        "bonus": 7
    },
    ClassicBonus.SOUTHAMERICA: {
        "name": "EU",
        "bonus": 2
    },
    ClassicBonus.AFRICA: {
        "name": "EU",
        "bonus": 3
    },
    ClassicBonus.AUSTRALIA: {
        "name": "EU",
        "bonus": 2
    },
}


# Eventually provide a class which helps to enumerator bonuses, make that ID and make there 
# a str name. Then make each bonus have an Enum which denotes NA, SA, AF, EU, AS, AU etc, and then 
# have them in this dict. 
class ClassicBonuses(TypedDict):
    id: ClassicBonus
    name: str
    bonus: int
    


# Create an empty graph
Classic = nx.Graph()

# Add territories in North America from left to right, top to bottom
Classic.add_node(1, name = "Alaska", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(2, name = "Northwest Territory", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(3, name = "Greenland", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(4, name = "Alberta", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(5, name = "Ontario", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(6, name = "Quebec", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(7, name = "Western United States", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(8, name = "Eastern UNited States", troops = 0, player = 0, bonus = 'NA')
Classic.add_node(9, name = "Central America", troops = 0, player = 0, bonus = 'NA')

Classic.add_edges_from([(1, 2), (1, 4), 
                        (2, 3), (2, 4), (2, 5), 
                        (3, 5), (3, 6), 
                        (4, 5), (4, 7), 
                        (5, 6), (5, 7), (5, 8), 
                        (6, 8), 
                        (7, 8), (7, 9), 
                        (8, 9)])

# Add Europe territories

Classic.add_node(10, name = "Iceland", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(11, name = "Scandinavia", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(12, name = "Great Britain", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(13, name = "Northern Europe", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(14, name = "Ukraine", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(15, name = "Western Europe", troops = 0, player = 0, bonus = 'EU')
Classic.add_node(16, name = "Southern Europe", troops = 0, player = 0, bonus = 'EU')

# Add internal Europe edges
Classic.add_edges_from([(10, 11), (10, 12), 
                        (11, 12), (11, 13), (11, 14), 
                        (12, 13), (12, 15), 
                        (13, 14), (13, 15), (13, 16), 
                        (14, 16), 
                        (15, 16)])

# Add external Europe edges
Classic.add_edges_from([(3, 10)])


# Add Asia territories
Classic.add_node(17, name = "Ural", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(18, name = "Siberia", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(19, name = "Yakutsk", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(20, name = "Kamchatka", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(21, name = "Irkutsk", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(22, name = "Mongolia", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(23, name = "Japan", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(24, name = "Afghanistan", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(25, name = "China", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(26, name = "Middle East", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(27, name = "India", troops = 0, player = 0, bonus = 'AS')
Classic.add_node(28, name = "Siam", troops = 0, player = 0, bonus = 'AS')

# Add internal Asia edges
Classic.add_edges_from([(17, 18), (17, 24), (17, 25),
                        (18, 19), (18, 21), (18, 22), (18, 25), 
                        (19, 20), (19, 21), 
                        (20, 21), (20, 22), (20, 23),
                        (21, 22), 
                        (22, 23), (22, 25),
                        (24, 25), (24, 26), (24, 27),
                        (25, 27), (25, 28),  
                        (26, 27), 
                        (27, 28)])

# Add external Asia edges
Classic.add_edges_from([(1, 20), (14, 17), (14, 24), (14, 26), (16, 26)])


# Add South America territories
Classic.add_node(29, name = "Venezuela", troops = 0, player = 0, bonus = 'SA')
Classic.add_node(30, name = "Peru", troops = 0, player = 0, bonus = 'SA')
Classic.add_node(31, name = "Brazil", troops = 0, player = 0, bonus = 'SA')
Classic.add_node(32, name = "Argentina", troops = 0, player = 0, bonus = 'SA')

# Add internal South America edges

Classic.add_edges_from([(29, 30), (29, 31), 
                        (30, 31), (30, 32), 
                        (31, 32)])

# Add external South America edges

Classic.add_edges_from([(9, 29)])


# Add Africa territories

Classic.add_node(33, name = "North Africa", troops = 0, player = 0, bonus = 'AF')
Classic.add_node(34, name = "Egypt", troops = 0, player = 0, bonus = 'AF')
Classic.add_node(35, name = "Congo", troops = 0, player = 0, bonus = 'AF')
Classic.add_node(36, name = "East Africa", troops = 0, player = 0, bonus = 'AF')
Classic.add_node(37, name = "South Africa", troops = 0, player = 0, bonus = 'AF')
Classic.add_node(38, name = "Madagascar", troops = 0, player = 0, bonus = 'AF')

# Add internal Africa edges

Classic.add_edges_from([(33, 34), (33, 35), (33, 36), 
                        (34, 36), 
                        (35, 36), (35, 37), 
                        (36, 37), (36, 38), 
                        (37, 38)])

# Add external Africa edges

Classic.add_edges_from([(15, 33), (16, 33), (16, 34), (26, 34), (26, 36), (31, 33)])

# Add Australia territories

Classic.add_node(39, name = "Indonesia", troops = 0, player = 0, bonus = 'AU')
Classic.add_node(40, name = "New Guinea", troops = 0, player = 0, bonus = 'AU')
Classic.add_node(41, name = "Western Australia", troops = 0, player = 0, bonus = 'AU')
Classic.add_node(42, name = "Eastern Australia", troops = 0, player = 0, bonus = 'AU')

# Add internal Australia edges

Classic.add_edges_from([(39, 40), (39, 41),
                        (40, 41), (40, 42),
                        (41, 42)])

# Add external Australia edges

Classic.add_edges_from([(28, 39)])
