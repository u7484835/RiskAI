from enum import Enum



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
