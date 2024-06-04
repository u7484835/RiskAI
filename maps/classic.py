import networkx as nx
from enum import Enum


classicBonusVals = {
    "NA": {
        "bonusVal": 5,
        "territories": {1, 2, 3, 4, 5, 6, 7, 8, 9}
    },
    "EU": {
        "bonusVal": 5,
        "territories": {10, 11, 12, 13, 14, 15, 16}
    },
    "AS": {
        "bonusVal": 7,
        "territories": {17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28}
    },
    "SA": {
        "bonusVal": 2,
        "territories": {29, 30, 31, 32}
    },
    "AF": {
        "bonusVal": 3,
        "territories": {33, 34, 35, 36, 37, 38}
    },
    "AU": {
        "bonusVal": 2,
        "territories": {39, 40, 41, 42}
    },
}


    


# Create an empty graph
Classic = nx.Graph()

# Add territories in North America from left to right, top to bottom
Classic.add_node(1, name = "Alaska", troops = 0, player = 0, bonus = "NA")
Classic.add_node(2, name = "Northwest Territory", troops = 0, player = 0, bonus = "NA")
Classic.add_node(3, name = "Greenland", troops = 0, player = 0, bonus = "NA")
Classic.add_node(4, name = "Alberta", troops = 0, player = 0, bonus = "NA")
Classic.add_node(5, name = "Ontario", troops = 0, player = 0, bonus = "NA")
Classic.add_node(6, name = "Quebec", troops = 0, player = 0, bonus = "NA")
Classic.add_node(7, name = "Western United States", troops = 0, player = 0, bonus = "NA")
Classic.add_node(8, name = "Eastern UNited States", troops = 0, player = 0, bonus = "NA")
Classic.add_node(9, name = "Central America", troops = 0, player = 0, bonus = "NA")

Classic.add_edges_from([(1, 2), (1, 4), 
                        (2, 3), (2, 4), (2, 5), 
                        (3, 5), (3, 6), 
                        (4, 5), (4, 7), 
                        (5, 6), (5, 7), (5, 8), 
                        (6, 8), 
                        (7, 8), (7, 9), 
                        (8, 9)])

# Add Europe territories

Classic.add_node(10, name = "Iceland", troops = 0, player = 0, bonus = "EU")
Classic.add_node(11, name = "Scandinavia", troops = 0, player = 0, bonus = "EU")
Classic.add_node(12, name = "Great Britain", troops = 0, player = 0, bonus = "EU")
Classic.add_node(13, name = "Northern Europe", troops = 0, player = 0, bonus = "EU")
Classic.add_node(14, name = "Ukraine", troops = 0, player = 0, bonus = "EU")
Classic.add_node(15, name = "Western Europe", troops = 0, player = 0, bonus = "EU")
Classic.add_node(16, name = "Southern Europe", troops = 0, player = 0, bonus = "EU")

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
Classic.add_node(17, name = "Ural", troops = 0, player = 0, bonus = "AS")
Classic.add_node(18, name = "Siberia", troops = 0, player = 0, bonus = "AS")
Classic.add_node(19, name = "Yakutsk", troops = 0, player = 0, bonus = "AS")
Classic.add_node(20, name = "Kamchatka", troops = 0, player = 0, bonus = "AS")
Classic.add_node(21, name = "Irkutsk", troops = 0, player = 0, bonus = "AS")
Classic.add_node(22, name = "Mongolia", troops = 0, player = 0, bonus = "AS")
Classic.add_node(23, name = "Japan", troops = 0, player = 0, bonus = "AS")
Classic.add_node(24, name = "Afghanistan", troops = 0, player = 0, bonus = "AS")
Classic.add_node(25, name = "China", troops = 0, player = 0, bonus = "AS")
Classic.add_node(26, name = "Middle East", troops = 0, player = 0, bonus = "AS")
Classic.add_node(27, name = "India", troops = 0, player = 0, bonus = "AS")
Classic.add_node(28, name = "Siam", troops = 0, player = 0, bonus = "AS")

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
Classic.add_node(29, name = "Venezuela", troops = 0, player = 0, bonus = "SA")
Classic.add_node(30, name = "Peru", troops = 0, player = 0, bonus = "SA")
Classic.add_node(31, name = "Brazil", troops = 0, player = 0, bonus = "SA")
Classic.add_node(32, name = "Argentina", troops = 0, player = 0, bonus = "SA")

# Add internal South America edges

Classic.add_edges_from([(29, 30), (29, 31), 
                        (30, 31), (30, 32), 
                        (31, 32)])

# Add external South America edges

Classic.add_edges_from([(9, 29)])


# Add Africa territories

Classic.add_node(33, name = "North Africa", troops = 0, player = 0, bonus = "AF")
Classic.add_node(34, name = "Egypt", troops = 0, player = 0, bonus = "AF")
Classic.add_node(35, name = "Congo", troops = 0, player = 0, bonus = "AF")
Classic.add_node(36, name = "East Africa", troops = 0, player = 0, bonus = "AF")
Classic.add_node(37, name = "South Africa", troops = 0, player = 0, bonus = "AF")
Classic.add_node(38, name = "Madagascar", troops = 0, player = 0, bonus = "AF")

# Add internal Africa edges

Classic.add_edges_from([(33, 34), (33, 35), (33, 36), 
                        (34, 36), 
                        (35, 36), (35, 37), 
                        (36, 37), (36, 38), 
                        (37, 38)])

# Add external Africa edges

Classic.add_edges_from([(15, 33), (16, 33), (16, 34), (26, 34), (26, 36), (31, 33)])

# Add Australia territories

Classic.add_node(39, name = "Indonesia", troops = 0, player = 0, bonus = "AU")
Classic.add_node(40, name = "New Guinea", troops = 0, player = 0, bonus = "AU")
Classic.add_node(41, name = "Western Australia", troops = 0, player = 0, bonus = "AU")
Classic.add_node(42, name = "Eastern Australia", troops = 0, player = 0, bonus = "AU")

# Add internal Australia edges

Classic.add_edges_from([(39, 40), (39, 41),
                        (40, 41), (40, 42),
                        (41, 42)])

# Add external Australia edges

Classic.add_edges_from([(28, 39)])



classicPosCoords = {
    1: (278, 117),
    2: (415, 112),
    3: (664, 69),
    4: (376, 180),
    5: (466, 193),
    6: (559, 190),
    7: (335, 274),
    8: (457, 306),
    9: (349, 391),
    10: (763, 144),
    11: (883, 142),
    12: (721, 247),
    13: (856, 261),
    14: (986, 217),
    15: (731, 375),
    16: (875, 330),
    17: (1129, 183),
    18: (1207, 127),
    19: (1304, 84),
    20: (1415, 105),
    21: (1300, 189),
    22: (1333, 276),
    23: (1496, 285),
    24: (1115, 300),
    25: (1277, 351),
    26: (1024, 433),
    27: (1196, 430),
    28: (1328, 466),
    29: (427, 469),
    30: (403, 588),
    31: (530, 555),
    32: (397, 765),
    33: (793, 526),
    34: (907, 472),
    35: (899, 666),
    36: (1006, 612),
    37: (899, 805),
    38: (1076, 793),
    39: (1337, 631),
    40: (1505, 600),
    41: (1426, 796),
    42: (1580, 817),
}


newClassicPosCoords = {
    1: [278, 942], 
    2: [415, 947], 
    3: [664, 990], 
    4: [376, 879], 
    5: [466, 866], 
    6: [559, 869], 
    7: [335, 785], 
    8: [457, 753], 
    9: [349, 668], 
    10: [763, 915], 
    11: [883, 917], 
    12: [721, 812], 
    13: [856, 798], 
    14: [986, 842], 
    15: [731, 684], 
    16: [875, 729], 
    17: [1129, 876], 
    18: [1207, 932], 
    19: [1304, 975], 
    20: [1415, 954], 
    21: [1300, 870], 
    22: [1333, 788], 
    23: [1496, 774], 
    24: [1115, 759], 
    25: [1277, 708], 
    26: [1024, 626], 
    27: [1196, 629], 
    28: [1328, 593], 
    29: [427, 590], 
    30: [403, 471], 
    31: [530, 504], 
    32: [397, 294], 
    33: [793, 533], 
    34: [907, 587], 
    35: [899, 393], 
    36: [1006, 447], 
    37: [899, 254], 
    38: [1076, 266], 
    39: [1337, 428], 
    40: [1505, 459], 
    41: [1426, 263], 
    42: [1580, 242]
 }

new2ClassicPosCoords = { 
    1: [18, 712], 
    2: [155, 717], 
    3: [404, 760], 
    4: [116, 649], 
    5: [206, 636], 
    6: [299, 639], 
    7: [75, 555], 
    8: [197, 523], 
    9: [89, 438], 
    10: [503, 685], 
    11: [623, 687], 
    12: [461, 582], 
    13: [596, 568], 
    14: [726, 612], 
    15: [471, 454], 
    16: [615, 499], 
    17: [869, 646], 
    18: [947, 702], 
    19: [1044, 745], 
    20: [1155, 724], 
    21: [1040, 640], 
    22: [1073, 558], 
    23: [1236, 544], 
    24: [855, 529], 
    25: [1017, 478], 
    26: [764, 396], 
    27: [936, 399], 
    28: [1068, 363], 
    29: [167, 360], 
    30: [143, 241], 
    31: [270, 274], 
    32: [137, 64], 
    33: [533, 303], 
    34: [647, 357], 
    35: [639, 163], 
    36: [746, 217], 
    37: [639, 24], 
    38: [816, 36], 
    39: [1077, 198], 
    40: [1245, 229], 
    41: [1166, 33], 
    42: [1320, 12]
}


new3ClassicPosCoords = {1: [13, 970], 
 2: [150, 975], 
 3: [399, 1018], 
 4: [111, 907], 
 5: [201, 894], 
 6: [294, 897], 
 7: [70, 813], 
 8: [192, 781], 
 9: [84, 696], 
 10: [498, 943], 
 11: [618, 945], 
 12: [456, 840], 
 13: [591, 826], 
 14: [721, 870], 
 15: [466, 712], 
 16: [610, 757], 
 17: [864, 904], 
 18: [942, 960], 
 19: [1039, 1003], 
 20: [1150, 982], 
 21: [1035, 898], 
 22: [1068, 816], 
 23: [1231, 802], 
 24: [850, 787], 
 25: [1012, 736], 
 26: [759, 654], 
 27: [931, 657], 
 28: [1063, 621], 
 29: [162, 618], 
 30: [138, 499], 
 31: [265, 532], 
 32: [132, 322], 
 33: [528, 561], 
 34: [642, 615], 
 35: [634, 421], 
 36: [741, 475], 
 37: [634, 282], 
 38: [811, 294], 
 39: [1072, 456], 
 40: [1240, 487], 
 41: [1161, 291], 
 42: [1315, 270]}