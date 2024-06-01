# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click
from structures import *
from maps.mapStructures import MapType, Map
from typing import Optional



# ---------------------------- Setup interface ----------------------------
# First interface functions to be called, helps to initialise the game structures.

def getMapType() -> MapType:
    """
    Asks the user what map the game is being played on.

    """
    mapList = [elem.name.capitalize() for elem in MapType]
    mapInput = click.prompt("Please enter the map to play on:", type=click.Choice(mapList, case_sensitive=True))
    return MapType.from_str(mapInput)
    
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


# Dislike that colours are defined here. Consider a different spot fo the constant. 
COLOURS = ["blue", "green", "yellow", "orange", "red", "pink", "black", "white", "purple"]

def getPlayersList() -> list[str]:
    """
    Gets information about how many players there are, order of players, colours associated with players.
    Should update main data structures. 
    """
    numPlayers = click.prompt("Please enter the number of players:", type= click.IntRange(min=2))
    
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



def getTroopSetup(playersList : list[str], map : Map):
    """
    Gets information the amount of troops on each territory, and the owner of each territory.
    Should update main data structures.
    """
    
    for nodeID in map.graph.nodes:
        agentColour = click.prompt(f"Enter which player colour owns {map.graph.nodes[nodeID]["name"]}:", type=click.Choice(playersList, case_sensitive=True))
        map.graph.nodes[nodeID]["player"] = playersList.index(agentColour)
        
        troopsNum = click.prompt(f"Enter the number of troops on territory {map.graph.nodes[nodeID]["name"]}:", type= click.IntRange(min=1))

        map.graph.nodes[nodeID]["troops"] = troopsNum
        
        
def setupGame() -> GameState:
    newGameState = GameState()
            

# ---------------------------- Input - Game interface ----------------------------
# Interface features to be called when game is running. 


        
# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getTerritory(map : Map, player : Optional[int]) -> int:
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """    
    territory = click.prompt(f"Enter the territory:", type=click.Choice(map.territoryNames, case_sensitive=True))
    
    # !Could be dodgy code, does the iterator go in sequence??
    territoryID = map.territoryNames.index(territory) + 1
    
    if player is not None:
        while map.graph.nodes[territoryID]["player"] != player:
            click.echo(f"Territory {territory} not owned by player.")
            territory = click.prompt(f"Enter the territory:", type=click.Choice(map.territoryNames, case_sensitive=True))
            
    return territoryID


        

# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getDraftOpp(player : int, map : Map, playerDict : PlayerDict):
    """
    For an opponent's move, gets which player drafted, how many troops they drafted, 
    where they drafted, and whether they traded in cards.
    """
    repititionFlag = True
    
    click.echo("Drafting troops:")
    while repititionFlag:
        territoryID = getTerritory(map, player)
        
        troopsNum = click.prompt("Enter the number of troops on deployed:", type = click.IntRange(min=1))

        playerDict[player]["troops"] += troopsNum
        map.graph.nodes[territoryID]["troops"] += troopsNum
            
        repititionFlag = click.prompt("Is there another territory drafted to?", type=bool)
            
        
            
def getAttackOpp(player : int, map : Map, playerDict : PlayerDict) -> Tuple[bool, Optional[int]]:
    """
    For an opponent's move, gets where which player attacked, what territory was attacked, how many troopes were lost on each side, 
    how many troops were moved to the new terrtory. Apply changes directly to map. If a player is killed, terminates early and 
    returns the ID of the player killed. Otherwise returns None. Also outputs whether a territory was captured for card updates. 
    """
    
    repititionFlag = click.prompt("Did the player make any attacks?", type=bool)    
    # Cards are awarded if a player captures a territory
    captureFlag = False
    
    while repititionFlag:
        
        # Gets territory player is attacking from
        click.echo("Territory attacking. ", nl=False)
        territoryIDAtt = getTerritory(map, player)
        
        # Gets defending territory
        click.echo("Territory defending. ", nl=False)
        territoryIDDef = getTerritory(map, None)
        # Gets ID of player who owns the attacked territory
        attackedPlayer = map.graph.nodes[territoryIDDef]["player"]


        # Gets number of troops lost while defending
        troopsLostDef = click.prompt(f"Enter the number of defending troops lost:", type = click.IntRange(min=0, max=map.graph.nodes[territoryIDDef]["troops"]))
        playerDict[attackedPlayer]["troops"] -= troopsLostDef

            
        # Gets number of troops lost while attacking
        troopsLostAtt = click.prompt(f"Enter the number of attacking troops lost:", type = click.IntRange(min=0, max=map.graph.nodes[territoryIDAtt]["troops"]))
        map.graph.nodes[territoryIDAtt]["troops"] -= troopsLostAtt
        playerDict[attackedPlayer]["troops"] -= troopsLostAtt


        

        # Checks whether territory was taken
        if troopsLostDef >= map.graph.nodes[territoryIDDef]["troops"]:
            captureFlag = True
            # If territory was taken, gets number of troops moved to attacked territory
            troopsMoved = click.prompt(f"Enter the number of troops moved to the attacked territory:", type=click.IntRange(min=3, max=map.graph.nodes[territoryIDAtt]["troops"]-1))
            
            # Reassigns territory, adds opponents new troops to territory, updates old territory troops
            map.graph.nodes[territoryIDDef]["player"] = player
            map.graph.nodes[territoryIDDef]["troops"] = troopsMoved
            map.graph.nodes[territoryIDAtt]["troops"] -= troopsMoved
            
            # Updates territory counts for attacking and attacked players
            playerDict[player]["territories"] += 1
            playerDict[attackedPlayer]["territories"] -= 1
            
            # If all of an opponents territories are taken, they are eliminated, 
            # and their cards are given to the attacker.
            if playerDict[attackedPlayer]["territories"] == 0:
                return (True, attackedPlayer)
                
        else:
            # If territory was not captured, updates defending troop count
            map.graph.nodes[territoryIDDef]["troops"] -= troopsLostDef
            
        repititionFlag = click.prompt("Was there another territory attacked?", type=bool)    
    
    return (captureFlag, None)



def getFortifyOpp(player : int, map : Map):
    """
    Gets which player fortified, where they fortified from, where they fortified to, and how many troops they fortified.
    """
    fortifyFlag = click.prompt("Did the player fortify?", type=bool)    
    
    if fortifyFlag:
        # Gets territory player is fortifying from
        click.echo("Territory fortifying from. ", nl=False)
        fortFromID = getTerritory(map, player)
        
        # Gets territory player is fortifying to
        click.echo("Territory fortifying to. ", nl=False)
        fortToID = getTerritory(map, player)
        
        # Ensures that troops aren't moved from a territory to itelf
        while fortFromID == fortToID:
            click.echo("Territories must be different. Territory fortifying to. ", nl=False)
            fortToID = getTerritory(map, player)
            
        # Gets number of troops moved, updates territories on map
        troopsMoved = click.prompt(f"Enter the number of troops moved:", type = click.IntRange(min=1, max=map.graph.nodes[fortFromID]["troops"]))
        map.graph.nodes[fortFromID]["troops"] -= troopsMoved
        map.graph.nodes[fortToID]["troops"] += troopsMoved




def getTurn(player : int, gameState: GameState) -> bool:
    """
    Calls draft, attack and fortify functions to execute the interface between the turns played 
    by opponents in game and the internal representation. Outputs a bool to indicate whether the game has concluded.
    """
    getDraftOpp(player, gameState.map, gameState.playerDict)
    # Gets data on whether a player was killed, and if the player captured at least one territory
    captureFlag, killedPlayer = getAttackOpp(player, gameState.map, gameState.playerDict)
    
    # If a player was killed, their cards are given to the attacker
    while killedPlayer is not None:
        gameState.playerDict[player]["cards"] += gameState.playerDict[killedPlayer]["cards"]
        gameState.playersAlive.remove(killedPlayer)
        
        # If only one player is left, the game is over so terminate early. 
        if len(gameState.playersAlive) == 1:
            return True
        
        # Allow the player to continue attacking
        _, killedPlayer = getAttackOpp(player, gameState.map, gameState.playerDict)
        
    getFortifyOpp(player, gameState.map)
    
    if captureFlag:
        gameState.playerDict[player]["cards"] += 1
    
    return False



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