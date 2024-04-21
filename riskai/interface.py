# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click




# ---------------------------- Setup interface ----------------------------
# First interface functions to be called, helps to initialise the game structures.


def getMapInfo():
    """
    Asks the user what map the game is being played on.

    """
    pass



def getBlizzardInfo():
    """
    Asks the user if the game has blizzards enabled.
    """
    pass


def getFogInfo():
    """
    Asks the user if the game has blizzards enabled.
    """
    pass




# ---------------------------- Input - Game interface ----------------------------
# Interface features to be called when game is running. 


def getPlayersInfo():
    """
    Gets information about how many players there are, order of players, colours associated with players.
    """
    pass


def getTroopInfo():
    """
    Gets information the amount of troops on each territory, and the owner of each territory.
    """
    pass


# Gets information about how many players there are, order of players and which player owns what territories with what amount of troops. 
# Updates main game variables to do this. Should provide checksum values (comparing troops inputted to troop tally provided by game)

#Uses getPlayersInfo(), getTroopInfo()
def getSetupInfo():
    """
    Gets information about how many players there are, order of players and which player owns what territories with what amount of troops. 
    Updates main game variables to do this. Should provide checksum values (comparing troops inputted to troop tally provided by game).
    
    Requires:
        - `getPlayersInfo()`
        - `getTroopInfo()`
    """
    pass



# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getDraftInfo():
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """
    pass


def getAttackInfo():
    """
    Gets where which player attacked, what territory was attacked, how many troopes were lost on each side, 
    how many troops were moved to the new terrtory.
    """
    pass


def getFortifyInfo():
    """
    Gets which player fortified, where they fortified from, where they fortified to, and how many troops they fortified.
    """
    pass


def getTurnInfo():
    """
    Gets info about the amount of troops a player drafted, where they played the draft,
    whether they traded in cards, what territories they attacked, whether they killed a player (needed or inferred?) 
    what territories they left troops in when attacking, and where they fortified to. 
    
    
    Requires:
        - `getDraftInfo()`
        - `getAttackInfo()`
        - `getFortifyInfo()`
    """
    pass



# ---------------------------- Output - Game interface ----------------------------

# Tells user where to draft troops, whether to trade cards, what cards to use.
def instructDraft():
    pass

# Tells user which territories to attack with, where to attack, how many to attack with, and how many to move.
def instructAttack():
    pass

# Tells user whether to fortify, where fortify from, where to fortify to, and how many to fortify with.
def instructFortify():
    pass

