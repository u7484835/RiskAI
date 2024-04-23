# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click
from structures import *
from maps.mapStructures import MapType



# ---------------------------- Setup interface ----------------------------
# First interface functions to be called, helps to initialise the game structures.


def getMapInfo() -> MapType:
    """
    Asks the user what map the game is being played on.

    """
    pass



def getBlizzardInfo() -> bool:
    """
    Asks the user if the game has blizzards enabled.
    """
    pass

# Likely won't implement
def getCapitalsInfo() -> bool:
    """
    Asks the user if the game has the capitals gamemode enabled.
    """
    pass




# ---------------------------- Input - Game interface ----------------------------
# Interface features to be called when game is running. 


def getPlayersInfo():
    """
    Gets information about how many players there are, order of players, colours associated with players.
    Should update main data structures. 
    """
    pass


def getTroopInfo():
    """
    Gets information the amount of troops on each territory, and the owner of each territory.
    Should update main data structures.
    """
    pass


def getSetupInfo():
    """
    Gets information about how many players there are, order of players and which player owns what territories with what amount of troops. 
    Updates main game variables to do this. Should provide checksum values (comparing troops inputted to troop tally provided by game).
    Should update main data structures.
    
    Requires:
        - `getPlayersInfo()`
        - `getTroopInfo()`
    """
    pass



# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getDraftInfo() -> Draft:
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """
    pass


def getAttackInfo() -> Attack:
    """
    Gets where which player attacked, what territory was attacked, how many troopes were lost on each side, 
    how many troops were moved to the new terrtory.
    """
    pass


def getFortifyInfo() -> Fortify:
    """
    Gets which player fortified, where they fortified from, where they fortified to, and how many troops they fortified.
    """
    pass


def getTurn():
    """
    Gets info about the amount of troops a player drafted, where they played the draft,
    whether they traded in cards, what territories they attacked, whether they killed a player (needed or inferred?) 
    what territories they left troops in when attacking, and where they fortified to. 
    
    Should update internal data structures.
    
    
    Requires:
        - `getDraftInfo()`
        - `getAttackInfo()`
        - `getFortifyInfo()`
    """
    pass



# ---------------------------- Output - Game interface ----------------------------


def instructDraft(draft : Draft) :
    """
    Tells user where to draft troops, whether to trade cards, what cards to use.
    """
    pass

def instructAttack(attacks : Attack):
    """
    Tells user which territories to attack with, where to attack, how many to attack with, and how many to move.
    """
    pass

def instructFortify(fortify : Fortify):
    """
    Tells user whether to fortify, where fortify from, where to fortify to, and how many to fortify with.
    """
    pass



def instructTurn(draft : Draft, attacks : Attack, fortify : Fortify):
    """
    Tells user full list of actions to to implement as instructed by the AI agent. 
    
    
    Requires:
        - `instructDraft()`
        - `instructAttack()`
        - `instructFortify()`
    """
    pass

def displayGameover():
    """
    Outputs information about the winner of the game and any final information which might be helpful
    for testing.
    """
    pass