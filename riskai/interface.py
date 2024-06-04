# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click
from .structures import *
from maps.mapStructures import MapType, Map
from typing import Optional
from .drawInterface import drawBoard



# ---------------------------- Setup interface ----------------------------
# First interface functions to be called, helps to initialise the game structures.

def getMapType() -> MapType:
    """
    Asks the user what map the game is being played on.

    """
    mapList = [elem.name.capitalize() for elem in MapType]
    mapInput = click.prompt("Please enter the map to play on", type=click.Choice(mapList, case_sensitive=True))
    return MapType.from_str(mapInput)


# Likely won't implement, leaving in for expansion
def getBlizzardInfo() -> bool:
    """
    Asks the user if the game has blizzards enabled.
    """
    return click.prompt("Does this game have blizzards enabled?", type=bool, prompt_suffix=' ')


# Likely won't implement
def getCapitalsInfo() -> bool:
    """
    Asks the user if the game has the capitals gamemode enabled.
    """
    return click.prompt("Is this game a capitals conquest game?", type=bool, prompt_suffix=' ')


# Dislike that colours are defined here. Consider a different spot fo the constant. 
COLOURS = ["blue", "green", "yellow", "orange", "red", "pink", "black", "white", "purple"]

def getPlayersList() -> list[str]:
    """
    Gets information about how many players there are, order of players, colours associated with players.
    Should update main data structures. 
    """
    numPlayers = click.prompt("Please enter the number of players", type= click.IntRange(min=2))
    
    playersList = []
        
    click.echo("You should now enter the players in the game, denoted by colour and strictly entered in turn order.")
    for _ in range(numPlayers):
        colour = click.prompt("Please enter the players colour", type=click.Choice(COLOURS, case_sensitive=True))
        
        while colour in playersList:
            click.echo(f"The colour {colour} is already taken. Please choose a unique color.")
            colour = click.prompt("Enter the player colours in order", type=click.Choice(COLOURS, case_sensitive=True))
        
        playersList.append(colour)

    return playersList
    


def getAgentID(playersList : list[str]) -> int:
    """
    Gets the number ID of the agent in playing order indexed from 0. 
    """
    agentColour = click.prompt("Please enter which colour player the agent is (if multi agent game choose first)", type=click.Choice(playersList, case_sensitive=True))
    return playersList.index(agentColour)

def getAgentList(playersList : list[str]) -> list[int]:
    """
    Gets all player IDs to be played by AI. 
    """
    agentList = []
    
    repititionFlag = click.prompt("Would you like any agents in the game", type=bool)

    
    # Gets agents until maximum number of agents is reached
    while repititionFlag:
        
        # Gets new agent to be controlled by AI
        currAgentID = getAgentID(playersList)
        
        # Ensures agent chosen is unique
        while currAgentID in agentList:
            click.echo("This agent is already controlled by the AI.")
            currAgentID = getAgentID(playersList)
        
        # Adds agent to list 
        agentList.append(currAgentID)
        
        # If all agents are added no need to ask to add another
        if len(agentList) == len(playersList): 
            break
        
        repititionFlag =  click.prompt("Would you like to add another agent?", type=bool, prompt_suffix=' ')
        
    # List is sorted so it can be looped over if needed    
    agentList.sort()
    return agentList

def getTroopSetup(playersList : list[str], map : Map):
    """
    Gets information the amount of troops on each territory, and the owner of each territory.
    Should update main data structures.
    """
    
    for nodeID in map.graph.nodes:
        agentColour = click.prompt(f"Enter which player colour owns {map.graph.nodes[nodeID]['name']}", type=click.Choice(playersList, case_sensitive=True), show_choices=False)
        map.graph.nodes[nodeID]["player"] = playersList.index(agentColour)
        
        troopsNum = click.prompt(f"Enter the number of troops on territory {map.graph.nodes[nodeID]['name']}", type= click.IntRange(min=1))

        map.graph.nodes[nodeID]["troops"] = troopsNum
        
        
def setupGameState() -> GameState:
    mapType = getMapType()
    map = Map(mapType)
    playerList = getPlayersList()
    playersAlive = [i for i in range(len(playerList))]
    agentID = 0 # Dummy value, updated in main
    # agentID = getAgentID(playerList) removed, handling in game setup
    getTroopSetup(playerList, map)
    round = 1
    playerDict = {}
    
    # Initiliases playerDict with player IDs and colours
    for i in range(len(playerList)):
        # Correctly initialise other player data after deciding amounts
        playerDict[i] = {"id": i, "colour": playerList[i], "troops": 0, "territories": set(), "diceAggression": 0, "territoryAggression": 0, "bonusAggression": 0, "bonusesHeld": set(), "prevIncome": 0, "cardsNum": 0, "dangerLevel": 0}
        
    # Initialises all player troop totals correctly    
    for nodeID in map.graph.nodes:
        currPlayer = map.graph.nodes[nodeID]["player"]
        playerDict[currPlayer]["troops"] += map.graph.nodes[nodeID]["troops"]
        playerDict[currPlayer]["territories"].add(nodeID)

        
    
    # Initilaises players relationship matrix with starting friendliness score of 50    
    relationsMatrix = [[0 for _ in range(len(playerList))] for _ in range(len(playerList))]

    # Players have no relationship with themselves, should always be 0
    for i in range(len(playerList)):
        for j in range(len(playerList)):
            if i == j:
                relationsMatrix[i][j] = 0
                
                
    cards = []
    
    return GameState(map, agentID, round, playerDict, playersAlive, relationsMatrix, cards)


            

# ---------------------------- Input - Game interface ----------------------------
# Interface features to be called when game is running. 


        
# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getTerritory(map : Map, player : Optional[int], aboveOne : bool) -> int:
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """    
    territory = click.prompt(f"Enter the territory", type=click.Choice(map.territoryNames, case_sensitive=True), show_choices=False)
    
    # !Could be dodgy code, does the iterator go in sequence??
    territoryID = map.territoryNames.index(territory) + 1
    
    if player is not None:
        while map.graph.nodes[territoryID]["player"] != player:
            click.echo(f"Territory {territory} not owned by player.")
            territory = click.prompt(f"Enter the territory", type=click.Choice(map.territoryNames, case_sensitive=True), show_choices=False)
            territoryID = map.territoryNames.index(territory) + 1
            
            if aboveOne:
                while map.graph.nodes[territoryID]["troops"] <= 1:
                    click.echo(f"Territory {territory} must have more than one troop.")
                    territory = click.prompt(f"Enter the territory", type=click.Choice(map.territoryNames, case_sensitive=True), show_choices=False)
                    territoryID = map.territoryNames.index(territory) + 1
            
    else: 
        if aboveOne:
            while map.graph.nodes[territoryID]["troops"] <= 1:
                click.echo(f"Territory {territory} must have more than one troop.")
                territory = click.prompt(f"Enter the territory", type=click.Choice(map.territoryNames, case_sensitive=True), show_choices=False)
                territoryID = map.territoryNames.index(territory) + 1
            
    return territoryID




def getTradeOpp(player : int, map : Map, playerDict : PlayerDict):
    """
    For an opponent's move, gets whether they traded in cards, then simply 
    updates card numbers and bonus troops corresponding with cards. Draft 
    function implicitly handles card troops and territory/bonus troops. 
    """
    tradeFlag = False
    
    if playerDict[player]["cardsNum"] >= 5:
        click.echo(f"The {playerDict[player]['colour']} was forced to trade in.")
        tradeFlag = True
        
    elif playerDict[player]["cardsNum"] >= 3:
        tradeFlag = click.prompt(f"Did {playerDict[player]['colour']} trade in cards?", type=bool, prompt_suffix=' ')
    
    
    if tradeFlag:      
        # Currently unneeded as all draft numbers are taken from drafting phase. It's a little inconsistent 
        # and error prone, could add explicit draft number calculations and checks.   
        # troopsNum = click.prompt("Enter the number of troops gained", type =click.Choice([4, 6, 8, 10]), show_choices=False)
        playerDict[player]["cardsNum"] -= 3
        
        # Cards have territory bonuses which can give +2 on fixed owned territories
        bonusFlag = click.prompt(f"Did the trade give bonus troops?", type=bool, prompt_suffix=' ')
        
        if bonusFlag:   
            click.echo(f"Provide the territory for bonus troops.")
            bonusID = getTerritory(map, player, False)
            playerDict[player]["troops"] += 2
            map.graph.nodes[bonusID]["troops"] += 2
        
        if playerDict[player]["cardsNum"] >= 5:
            getTradeOpp(player, map, playerDict)

            



        
def getDraftOpp(player : int, map : Map, playerDict : PlayerDict):
    """
    For an opponent's move, gets which player drafted, how many troops they drafted, 
    where they drafted. Trading cards computed separately.
    """
    repititionFlag = True
    
    click.echo(f"Drafting {playerDict[player]['colour']}'s troops")
    # Checks for trades, 
    getTradeOpp(player, map, playerDict)
    
    while repititionFlag:
        territoryID = getTerritory(map, player, False)
        
        troopsNum = click.prompt("Enter the number of troops deployed", type = click.IntRange(min=1))

        playerDict[player]["troops"] += troopsNum
        map.graph.nodes[territoryID]["troops"] += troopsNum
            
        repititionFlag = click.prompt("Is there another territory drafted to?", type=bool, prompt_suffix=' ')
            
        
# !! Must also be updating opponent assessment info eg. relationship matrix, dice aggression. Must also update bonuses held
# Consider ballooning into other functions which handle this, while the interface just gets the numbers. 
# Could actually call two separate functions which do the gameState updating, one for captured 
# territories and one without.
def getAttackOpp(player : int, map : Map, playerDict : PlayerDict) -> Tuple[bool, Optional[int]]:
    """
    For an opponent's move, gets where which player attacked, what territory was attacked, how many troopes were lost on each side, 
    how many troops were moved to the new terrtory. Apply changes directly to map. If a player is killed, terminates early and 
    returns the ID of the player killed. Otherwise returns None. Also outputs whether a territory was captured for card updates. 
    """
    
    repititionFlag = click.prompt(f"Did {playerDict[player]['colour']} make any attacks?", type=bool, prompt_suffix=' ')    
    # Cards are awarded if a player captures a territory
    captureFlag = False
    
    while repititionFlag:
        
        # Gets territory player is attacking from
        click.echo("Territory attacking. ", nl=False)
        territoryIDAtt = getTerritory(map, player, True)
    
        
        # Gets defending territory
        click.echo("Territory defending. ", nl=False)
        territoryIDDef = getTerritory(map, None, False)
        # Gets ID of player who owns the attacked territory
        attackedPlayer = map.graph.nodes[territoryIDDef]["player"]


        # Gets number of troops lost while defending
        troopsLostDef = click.prompt(f"Enter the number of defending troops lost", type = click.IntRange(min=0, max=map.graph.nodes[territoryIDDef]["troops"]))
        playerDict[attackedPlayer]["troops"] -= troopsLostDef

            
        # Gets number of troops lost while attacking
        troopsLostAtt = click.prompt(f"Enter the number of attacking troops lost", type = click.IntRange(min=0, max=map.graph.nodes[territoryIDAtt]["troops"]))
        map.graph.nodes[territoryIDAtt]["troops"] -= troopsLostAtt
        playerDict[attackedPlayer]["troops"] -= troopsLostAtt


        

        # Checks whether territory was taken
        if troopsLostDef >= map.graph.nodes[territoryIDDef]["troops"]:
            captureFlag = True
            # If territory was taken, gets number of troops moved to attacked territory
            if map.graph.nodes[territoryIDAtt]["troops"] <= 4:
                troopsMoved = map.graph.nodes[territoryIDAtt]["troops"] - 1
            else:
                troopsMoved = click.prompt(f"Enter the number of troops moved to the attacked territory", type=click.IntRange(min=3, max=map.graph.nodes[territoryIDAtt]["troops"]-1))
            
            # Reassigns territory, adds opponents new troops to territory, updates old territory troops
            map.graph.nodes[territoryIDDef]["player"] = player
            map.graph.nodes[territoryIDDef]["troops"] = troopsMoved
            map.graph.nodes[territoryIDAtt]["troops"] -= troopsMoved
            
            # Updates territory counts for attacking and attacked players
            playerDict[player]["territories"].add(territoryIDDef)
            playerDict[attackedPlayer]["territories"].remove(territoryIDDef)
            
            # If all of an opponents territories are taken, they are eliminated, 
            # and their cards are given to the attacker.
            if len(playerDict[attackedPlayer]["territories"]) == 0:
                click.echo(f"The {playerDict[attackedPlayer]['colour']} has been eliminated.")
                return (True, attackedPlayer)
                
        else:
            # If territory was not captured, updates defending troop count
            map.graph.nodes[territoryIDDef]["troops"] -= troopsLostDef
            
        repititionFlag = click.prompt("Was there another territory attacked?", type=bool, prompt_suffix=' ')    
    
    return (captureFlag, None)



def getFortifyOpp(player : int, map : Map, playerDict : PlayerDict):
    """
    Gets which player fortified, where they fortified from, where they fortified to, and how many troops they fortified.
    """
    
    if len(playerDict[player]["territories"]) == 1:
        click.echo(f"{playerDict[player]['colour']} has only one territory and cannot fortify.")
        fortifyFlag = False
    
    else:
        fortifyFlag = click.prompt(f"Did {playerDict[player]['colour']} fortify?", type=bool, prompt_suffix=' ')    
    
    if fortifyFlag:
        # Gets territory player is fortifying from
        click.echo("Territory fortifying from. ", nl=False)
        fortFromID = getTerritory(map, player, True)

        
        # Gets territory player is fortifying to
        click.echo("Territory fortifying to. ", nl=False)
        fortToID = getTerritory(map, player, False)
        
        # Ensures that troops aren't moved from a territory to itelf
        while fortFromID == fortToID:
            click.echo("Territories must be different. Territory fortifying to. ", nl=False)
            fortToID = getTerritory(map, player, False)
            
        # Gets number of troops moved, updates territories on map
        troopsMoved = click.prompt(f"Enter the number of troops moved", type = click.IntRange(min=1, max=map.graph.nodes[fortFromID]["troops"]))
        map.graph.nodes[fortFromID]["troops"] -= troopsMoved
        map.graph.nodes[fortToID]["troops"] += troopsMoved




def getTurn(player : int, gameState: GameState) -> bool:
    """
    Calls draft, attack and fortify functions to execute the interface between the turns played 
    by opponents in game and the internal representation. Outputs a bool to indicate whether the game has concluded.
    """
    drawBoard(gameState)
    getDraftOpp(player, gameState.map, gameState.playerDict)
    # Gets data on whether a player was killed, and if the player captured at least one territory
    drawBoard(gameState)

    
    captureFlag, killedPlayer = getAttackOpp(player, gameState.map, gameState.playerDict)
    drawBoard(gameState)

    
    # If a player was killed, their cards are given to the attacker
    while killedPlayer is not None:
        gameState.playerDict[player]["cardsNum"] += gameState.playerDict[killedPlayer]["cardsNum"]
        gameState.playersAlive.remove(killedPlayer)
        
        # If only one player is left, the game is over so terminate early. 
        if len(gameState.playersAlive) == 1:
            return True
        
        # Allow the player to continue attacking
        _, killedPlayer = getAttackOpp(player, gameState.map, gameState.playerDict)
        drawBoard(gameState)

        
    getFortifyOpp(player, gameState.map, gameState.playerDict)
    drawBoard(gameState)

    
    if captureFlag:
        gameState.playerDict[player]["cardsNum"] += 1
    
    return False



# ---------------------------- Output - Game interface ----------------------------

def tradeText(card : Card, gameState : GameState) -> str:
    """
    Converts a trade action into a string for output. 
    """
    if card.type == CardType.WILD:
        return "the next wildcard"
    else:
        return f"{card.type.name.capitalize()} at {gameState.map.territoryNames[card.territory]}"

def instructTrade(trades : list[Trade], gameState : GameState) :
    """
    Tells user whether to trade cards, what cards to use.
    """
    # empty list indicates not to trade
    if len(trades) == 0:
        click.echo("You should not trade")

    else:
        click.echo("You should trade the following cards:")
        for trade in trades:
            click.echo(f"Trade in the {tradeText(trade[0], gameState)}, the {tradeText(trade[0], gameState)}, and the {tradeText(trade[0], gameState)}.")
        
    
def instructDraft(draft : Draft, gameState : GameState) :
    """
    Tells user where to draft troops, whether to trade cards, what cards to use.
    """
    instructTrade(draft[0], gameState)
    
    click.echo("Draft to the following territories:")
    for singleDraft in draft[1]:
        click.echo(f"Draft {singleDraft[1]} troops to {gameState.map.territoryNames[singleDraft[0]]}")
        

def instructAttack(attacks : Attack, gameState : GameState) -> bool:
    """
    Tells user which territories to attack with, where to attack, how many to attack with, and how many to move. 
    Indicates gameover with boolean.
    """
    
    if len(attacks) == 0:
        click.echo("Do not attack.")
    
    
    # !! Currently no active tracking if attack fails, complete alongside heuristic
    # Attacks do not give perfect dice calculations
    click.echo("Draft to the following territories:")
    for attack in attacks:
        click.echo(f"Attack from {gameState.map.territoryNames[attack[0]]} to {gameState.map.territoryNames[attack[1]]} with {attack[2]} troops, moving {attack[3]} troops.")
        
        
    

def instructFortify(fortify : Fortify, gameState : GameState):
    """
    Tells user whether to fortify, where fortify from, where to fortify to, and how many to fortify with.
    """
    if fortify is None:
        click.echo("Do not fortify.")
        
    else:  
        click.echo(f"Fortify from {gameState.map.territoryNames[fortify[0]]} to {gameState.map.territoryNames[fortify[1]]} with {fortify[2]} troops.")



def executeAgentTurn(move: Move, gameState: GameState):
    """
    Tells user full list of actions to to implement as instructed by the AI agent. 
    """
    drawBoard(gameState)
    instructDraft(move[0], gameState)
    drawBoard(gameState)
    instructAttack(move[1], gameState)
    drawBoard(gameState)
    instructFortify(move[2], gameState)
    drawBoard(gameState)

    
    

def displayGameover(winnerID : int, gameState : GameState):
    """
    Outputs information about the winner of the game and any final information which might be helpful
    for testing.
    """
    click.echo(f"The game is over. The winner is {gameState.playerDict[winnerID]['colour']}!")
    click.echo("The final state of the game is as follows:")
    print(gameState)
    
