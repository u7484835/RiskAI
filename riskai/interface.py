# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click
from structures import *
from maps.mapStructures import MapType, Map



# ---------------------------- Setup interface ----------------------------
# First interface functions to be called, helps to initialise the game structures.

def getMapType() -> MapType:
    """
    Asks the user what map the game is being played on.

    """
    while True:
        mapInput = click.prompt("Please enter the map to play on:", type=str)
        try:
            map_type = MapType.from_str(mapInput)
            return map_type
        except ValueError:
            print("Invalid map name. Please enter a valid map name.")


def getBlizzardInfo() -> bool:
    """
    Asks the user if the game has blizzards enabled.
    """
    return click.prompt("Does this game have blizzards enabled?", type=bool)


# Likely won"t implement
def getCapitalsInfo() -> bool:
    """
    Asks the user if the game has the capitals gamemode enabled.
    """
    return click.prompt("Is this game a capitals conquest game?", type=bool)




# ---------------------------- Input - Game interface ----------------------------
# Interface features to be called when game is running. 


COLOURS = ["blue", "green", "yellow", "orange", "red", "pink", "black", "white", "purple"]

def getPlayersList() -> list[str]:
    """
    Gets information about how many players there are, order of players, colours associated with players.
    Should update main data structures. 
    """
    numPlayers = click.prompt("Please enter the number of players:", type=int)
    
    playersList = []
        
    click.echo("You should now enter the players in the game, denoted by colour and strictly entered in turn order.")
    for _ in range(numPlayers):
        colour = click.prompt("Please enter the players colour:", type=click.Choice(COLOURS, case_sensitive=True))
        
        while colour in playersList:
            click.echo(f"The colour {colour} is already taken. Please choose a unique color.")
            colour = click.prompt("Enter the player colours in order:", type=click.Choice(COLOURS, case_sensitive=True))
        
        playersList.append(colour)

    return playersList
    


def getAgentID(playersList : list[str]) -> int:
    """
    Gets the number ID of the agent in playing order indexed from 0. 
    """
    agentColour = click.prompt("Please enter which colour player the agent is:", type=click.Choice(COLOURS, case_sensitive=True))
    
    while agentColour not in playersList:
            click.echo(f"The colour {agentColour} was not registered as a player.")
            agentColour = click.prompt("Please select the colour of the agent you are playing as:", type=click.Choice(COLOURS, case_sensitive=True))
        
    
    return playersList.index(agentColour)



def getTroopInfo(playersList : list[str], map : Map):
    """
    Gets information the amount of troops on each territory, and the owner of each territory.
    Should update main data structures.
    """
    
    for nodeID in map.graph.nodes:
        agentColour = click.prompt(f"Please enter which player colour owns {map.graph.nodes[nodeID]["name"]}:", type=click.Choice(playersList, case_sensitive=True))
        map.graph.nodes[nodeID]["player"] = playersList.index(agentColour)
        
        troopsNum = click.prompt(f"Please enter the number of troops on territory {map.graph.nodes[nodeID]["name"]}:", type=int)
        
        while troopsNum < 1:
            troopsNum = click.prompt(f"Having {troopsNum} troops on a territory is invalid. Please enter the positive number of troops shown for {map.graph.nodes[nodeID]["name"]}.")
            
        map.graph.nodes[nodeID]["troops"] = troopsNum
        


# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getDraftInfo(player : int, map : Map) -> Draft:
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """
    repititionFlag = True
    
    while repititionFlag:
        territory = click.prompt(f"Please enter which territory is being drafted to:", type=click.Choice(map.territoryNames, case_sensitive=True))
        
        # !Could be dodgy code, does the iterator go in sequence??
        territoryID = map.territoryNames.index(territory) + 1
        
        while map.graph.nodes[territoryID]["player"] != player:
            click.echo(f"Territory {territory} not owned by player.")
            territory = click.prompt(f"Please enter which territory is being drafted to:", type=click.Choice(map.territoryNames, case_sensitive=True))

        troopsNum = click.prompt(f"Please enter the number of troops on deployed to {territory}:", type=int)
            
        while troopsNum < 1:
            troopsNum = click.prompt(f"Having {troopsNum} troops on a territory is invalid. Please enter the positive number of troops shown for {territory}:")
            
        repititionFlag = click.prompt("Did the player trade in cards?", type=bool)
            
        
            
    


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