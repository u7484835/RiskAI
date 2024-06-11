# Will contain components for using click to transition between click input/output and variables to 
# coded objects
import click
from .structures import *
from maps.mapStructures import MapType, Map
from typing import Optional
from .drawInterface import drawBoard
from .riskAI import draftTroopsAmount, ownedTerrConnected



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


# *Dislike that colours are defined here. Consider a different spot fo the constant. 
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
        
    
    # Initialises all player bonuses correctly
    for bonus, vals in map.bonuses.items():
        if vals["territories"].issubset(playerDict[currPlayer]["territories"]):
            playerDict[currPlayer]["bonusesHeld"].add(bonus)

        
    
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




def getTradeOpp(player : int, gameState : GameState):
    """
    For an opponent's move, gets whether they traded in cards, then simply 
    updates card numbers and bonus troops corresponding with cards. Draft 
    function implicitly handles card troops and territory/bonus troops. 
    """
    tradeFlag = False
    
    if gameState.playerDict[player]["cardsNum"] >= 5:
        click.echo(f"The {gameState.playerDict[player]['colour']} was forced to trade in.")
        tradeFlag = True
        
    elif gameState.playerDict[player]["cardsNum"] >= 3:
        tradeFlag = click.prompt(f"Did {gameState.playerDict[player]['colour']} trade in cards?", type=bool, prompt_suffix=' ')
    
    
    if tradeFlag:      
        # Currently unneeded as all draft numbers are taken from drafting phase. It's a little inconsistent 
        # and error prone, could add explicit draft number calculations and checks.   
        # troopsNum = click.prompt("Enter the number of troops gained", type =click.Choice([4, 6, 8, 10]), show_choices=False)
        gameState.playerDict[player]["cardsNum"] -= 3
        
        # Cards have territory bonuses which can give +2 on fixed owned territories
        bonusFlag = click.prompt(f"Did the trade give bonus troops?", type=bool, prompt_suffix=' ')
        
        if bonusFlag:   
            click.echo(f"Provide the territory for bonus troops.")
            bonusID = getTerritory(gameState.map, player, False)
            gameState.playerDict[player]["troops"] += 2
            gameState.map.graph.nodes[bonusID]["troops"] += 2
        
        if gameState.playerDict[player]["cardsNum"] >= 5:
            getTradeOpp(player, gameState)

            



        
def getDraftOpp(player : int, gameState : GameState):
    """
    For an opponent's move, gets which player drafted, how many troops they drafted, 
    where they drafted. Trading cards computed separately.
    """
    repititionFlag = True
    
    draftNum = draftTroopsAmount(gameState, [])
    
    click.echo(f"Drafting {gameState.playerDict[player]['colour']}'s troops. There should be {draftNum} base troops to deploy.")
    # Checks for trades, 
    getTradeOpp(player, gameState)
    
    while repititionFlag:
        territoryID = getTerritory(gameState.map, player, False)
        
        troopsNum = click.prompt("Enter the number of troops deployed", type = click.IntRange(min=1))

        gameState.playerDict[player]["troops"] += troopsNum
        gameState.map.graph.nodes[territoryID]["troops"] += troopsNum
            
        repititionFlag = click.prompt("Is there another territory drafted to?", type=bool, prompt_suffix=' ')
            
        
# !! Must also be updating opponent assessment info eg. relationship matrix, dice aggression. Must also update bonuses held
# Consider ballooning into other functions which handle this, while the interface just gets the numbers. 
# Could actually call two separate functions which do the gameState updating, one for captured 
# territories and one without.
def getAttackOpp(player : int, gameState : GameState) -> Tuple[bool, Optional[int]]:
    """
    For an opponent's move, gets where which player attacked, what territory was attacked, how many troopes were lost on each side, 
    how many troops were moved to the new terrtory. Apply changes directly to map. If a player is killed, terminates early and 
    returns the ID of the player killed. Otherwise returns None. Also outputs whether a territory was captured for card updates. 
    """
    
    repititionFlag = click.prompt(f"Did {gameState.playerDict[player]['colour']} make any attacks?", type=bool, prompt_suffix=' ')    
    # Cards are awarded if a player captures a territory
    captureFlag = False
    
    while repititionFlag:
        
        # Gets territory player is attacking from
        click.echo("Territory attacking. ", nl=False)
        territoryIDAtt = getTerritory(gameState.map, player, True)
    
        
        # Gets defending territory
        click.echo("Territory defending. ", nl=False)
        territoryIDDef = getTerritory(gameState.map, None, False)
        
        # Attacking territory must be adjacent to defending territory, and must be owned by the player
        while gameState.map.graph.nodes[territoryIDDef]["player"] == player or territoryIDDef not in gameState.map.graph.neighbors(territoryIDAtt):
            click.echo("Territory must be adjacent and owned by an opponent.")
            territoryIDDef = getTerritory(gameState.map, None, False)
        
        # Gets ID of player who owns the attacked territory
        attackedPlayer = gameState.map.graph.nodes[territoryIDDef]["player"]


        # Gets number of troops lost while defending
        troopsLostDef = click.prompt(f"Enter the number of defending troops lost", type = click.IntRange(min=0, max=gameState.map.graph.nodes[territoryIDDef]["troops"]))
        gameState.playerDict[attackedPlayer]["troops"] -= troopsLostDef

            
        # Gets number of troops lost while attacking
        # When attacking worst case is losing all but 1 troop.
        troopsLostAtt = click.prompt(f"Enter the number of attacking troops lost", type = click.IntRange(min=0, max=gameState.map.graph.nodes[territoryIDAtt]["troops"] - 1))
        gameState.map.graph.nodes[territoryIDAtt]["troops"] -= troopsLostAtt
        gameState.playerDict[attackedPlayer]["troops"] -= troopsLostAtt


        

        # Checks whether territory was taken
        if troopsLostDef >= gameState.map.graph.nodes[territoryIDDef]["troops"]:
            captureFlag = True
            # If territory was taken, gets number of troops moved to attacked territory
            if gameState.map.graph.nodes[territoryIDAtt]["troops"] <= 4:
                troopsMoved = gameState.map.graph.nodes[territoryIDAtt]["troops"] - 1
            else:
                troopsMoved = click.prompt(f"Enter the number of troops moved to the attacked territory", type=click.IntRange(min=3, max=gameState.map.graph.nodes[territoryIDAtt]["troops"]-1))
            
            # Reassigns territory, adds opponents new troops to territory, updates old territory troops
            gameState.map.graph.nodes[territoryIDDef]["player"] = player
            gameState.map.graph.nodes[territoryIDDef]["troops"] = troopsMoved
            gameState.map.graph.nodes[territoryIDAtt]["troops"] -= troopsMoved
            
            # Updates territory counts for attacking and attacked players
            gameState.playerDict[player]["territories"].add(territoryIDDef)
            gameState.playerDict[attackedPlayer]["territories"].remove(territoryIDDef)
            
            # Updates bonuses
            bonus = gameState.map.graph.nodes[territoryIDDef]["bonus"]
            # Attacked player must have lost bonus
            gameState.playerDict[attackedPlayer]["bonusesHeld"].discard(bonus)
            # Check if attacking player now controls all of bonus
            if gameState.map.bonuses[bonus]["territories"].issubset(gameState.playerDict[player]["territories"]):
                gameState.playerDict[player]["bonusesHeld"].add(bonus)
                
            
            # If all of an opponents territories are taken, they are eliminated, 
            # and their cards are given to the attacker.
            if len(gameState.playerDict[attackedPlayer]["territories"]) == 0:
                click.echo(f"The {gameState.playerDict[attackedPlayer]['colour']} has been eliminated.")
                return (True, attackedPlayer)
                
        else:
            # If territory was not captured, updates defending troop count
            gameState.map.graph.nodes[territoryIDDef]["troops"] -= troopsLostDef
            
        repititionFlag = click.prompt("Was there another territory attacked?", type=bool, prompt_suffix=' ')    
    
    return (captureFlag, None)



def getFortifyOpp(player : int, gameState : GameState):
    """
    Gets which player fortified, where they fortified from, where they fortified to, and how many troops they fortified.
    """
    
    if len(gameState.playerDict[player]["territories"]) == 1:
        click.echo(f"{gameState.playerDict[player]['colour']} has only one territory and cannot fortify.")
        fortifyFlag = False
    else:
        fortifyFlag = click.prompt(f"Did {gameState.playerDict[player]['colour']} fortify?", type=bool, prompt_suffix=' ')    
    
    if fortifyFlag:
        # Gets territory player is fortifying from
        click.echo("Territory fortifying from. ", nl=False)
        fortFromID = getTerritory(gameState.map, player, True)

        
        # Gets territory player is fortifying to
        click.echo("Territory fortifying to. ", nl=False)
        fortToID = getTerritory(gameState.map, player, False)
        
        # !Does not check that there is a valid path of fortifying, probably won't implement
                
        # Ensures that troops aren't moved from a territory to itelf
        while fortFromID == fortToID and not ownedTerrConnected(gameState.map, player, fortFromID, fortToID):
            
            # Allows exit so player doesn't softlock from invalid fortify
            breakFlag = click.prompt("Territories must be connected in a valid path. Would you like to cancel fortify?", type=bool, prompt_suffix=' ')
            if breakFlag:
                 return
                 
            click.echo("Territory fortifying to. ", nl=False)
            
            fortToID = getTerritory(gameState.map, player, False)
            
        # Gets number of troops moved, updates territories on map
        troopsMoved = click.prompt(f"Enter the number of troops moved", type = click.IntRange(min=1, max=gameState.map.graph.nodes[fortFromID]["troops"] - 1))
        gameState.map.graph.nodes[fortFromID]["troops"] -= troopsMoved
        gameState.map.graph.nodes[fortToID]["troops"] += troopsMoved




def getTurn(player : int, gameState: GameState) -> bool:
    """
    Calls draft, attack and fortify functions to execute the interface between the turns played 
    by opponents in game and the internal representation. Outputs a bool to indicate whether the game has concluded.
    """
    drawBoard(gameState)
    getDraftOpp(player, gameState)
    # Gets data on whether a player was killed, and if the player captured at least one territory
    drawBoard(gameState)

    
    captureFlag, killedPlayer = getAttackOpp(player, gameState)
    drawBoard(gameState)

    
    # If a player was killed, their cards are given to the attacker
    while killedPlayer is not None:
        gameState.playerDict[player]["cardsNum"] += gameState.playerDict[killedPlayer]["cardsNum"]
        gameState.playersAlive.remove(killedPlayer)
        
        # If only one player is left, the game is over so terminate early. 
        if len(gameState.playersAlive) == 1:
            return True
        
        # Allow the player to continue attacking
        _, killedPlayer = getAttackOpp(player, gameState)
        drawBoard(gameState)

        
    getFortifyOpp(player, gameState)
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
        # Subtract 1 because territorynames indexed from 0
        return f"{card.type.name.capitalize()} at {gameState.map.territoryNames[card.territory - 1]}"

def instructTrade(trades : list[Trade], gameState : GameState) :
    """
    Tells user whether to trade cards, what cards to use. Updates gamestate 
    values as trade is carried out: adds troops and removes cards. Added troops 
    for drafting should already have been accounted for in Draft move and drafted 
    troops should be added in that phase. 
    """
    # empty list indicates not to trade
    if len(trades) == 0:
        click.echo("You should not trade")

    else:
        click.echo("You should trade the following cards:")
        for trade in trades:
            click.echo(f"Trade in the {tradeText(trade[0], gameState)}, the {tradeText(trade[0], gameState)}, and the {tradeText(trade[0], gameState)}.")
            
            # Checks if a traded card is in one of the player's territories
            for i in range (3):
                if trade[i].territory in gameState.playerDict[gameState.agentID]["territories"]:
                    # If so adds bonus troops but only once
                    gameState.playerDict[gameState.agentID]["troops"] += 2
                    gameState.map.graph.nodes[trade[i].territory]["troops"] += 2
                    break
            
            # Updates card count
            gameState.playerDict[gameState.agentID]["cardsNum"] -= 3
            gameState.cards.remove(trade[0])
            gameState.cards.remove(trade[1])
            gameState.cards.remove(trade[2])

        
    
def instructDraft(draft : Draft, gameState : GameState) :
    """
    Tells user where to draft troops, whether to trade cards, what cards to use.
    """
    instructTrade(draft[0], gameState)
    
    click.echo("Draft to the following territories:")
    for singleDraft in draft[1]:
        click.echo(f"Draft {singleDraft[1]} troops to {gameState.map.territoryNames[singleDraft[0] - 1]}")
        gameState.playerDict[gameState.agentID]["troops"] += singleDraft[1]
        gameState.map.graph.nodes[singleDraft[0]]["troops"] += singleDraft[1]
     





def instructAttack(attacks : Attack, gameState : GameState) -> Tuple[bool, Optional[int], Attack]:
    """
    Tells user which territories to attack with, where to attack, how many to attack with, and how many to move. 
    Indicates gameover with boolean.  If a player is killed, terminates early and returns the ID of the player killed. 
    Otherwise returns None. Also outputs whether a territory was captured for card updates. Finally outputs 
    The remaining attacks to be made if terminated early via elimination.
    """
    
    if len(attacks) == 0:
        click.echo("Do not attack.")
    
    captureFlag = False
    
    # !! Currently no active tracking if attack fails, complete alongside heuristic
    # Attacks do not give perfect dice calculations
    for attack in attacks:
        territoryIDAtt = attack[0]
        territoryIDDef = attack[1]
        
        attackedPlayer = gameState.map.graph.nodes[territoryIDDef]["player"]
        
        click.echo(f"Attack from {gameState.map.territoryNames[territoryIDAtt - 1]} to {gameState.map.territoryNames[territoryIDDef - 1]} with {attack[2]} troops")
        
        # Gets number of troops lost while defending
        troopsLostDef = click.prompt(f"Enter the number of defending troops lost", type = click.IntRange(min=0, max=gameState.map.graph.nodes[territoryIDDef]["troops"]))
        gameState.playerDict[attackedPlayer]["troops"] -= troopsLostDef

            
        # Gets number of troops lost while attacking
        troopsLostAtt = click.prompt(f"Enter the number of attacking troops lost", type = click.IntRange(min=0, max=gameState.map.graph.nodes[territoryIDAtt]["troops"] - 1))
        gameState.map.graph.nodes[territoryIDAtt]["troops"] -= troopsLostAtt
        gameState.playerDict[attackedPlayer]["troops"] -= troopsLostAtt


        # Checks whether territory was taken
        if troopsLostDef >= gameState.map.graph.nodes[territoryIDDef]["troops"]:
            captureFlag = True
            # If territory was taken, gets number of troops moved to attacked territory
            if gameState.map.graph.nodes[territoryIDAtt]["troops"] <= 4:
                troopsMoved = gameState.map.graph.nodes[territoryIDAtt]["troops"] - 1
                click.echo(f"Move {troopsMoved} troops to the attacked territory.")

            else:
                # !!Needs runtime troop for moving. For now move all troops. 
                troopsMoved = gameState.map.graph.nodes[territoryIDAtt]["troops"] - 1
                click.echo(f"Move {troopsMoved} troops to the attacked territory.")   
                
                         
            # Reassigns territory, adds opponents new troops to territory, updates old territory troops
            gameState.map.graph.nodes[territoryIDDef]["player"] = gameState.agentID
            gameState.map.graph.nodes[territoryIDDef]["troops"] = troopsMoved
            gameState.map.graph.nodes[territoryIDAtt]["troops"] -= troopsMoved
            
            # Updates territory counts for attacking and attacked players
            gameState.playerDict[gameState.agentID]["territories"].add(territoryIDDef)
            gameState.playerDict[attackedPlayer]["territories"].remove(territoryIDDef)
            
            # Updates bonuses
            bonus = gameState.map.graph.nodes[territoryIDDef]["bonus"]
            # Attacked player must have lost bonus
            gameState.playerDict[attackedPlayer]['bonusesHeld'].discard(bonus)
            # Check if attacking player now controls all of bonus
            if gameState.map.bonuses[bonus]["territories"].issubset(gameState.playerDict[gameState.agentID]["territories"]):
                gameState.playerDict[gameState.agentID]["bonusesHeld"].add(bonus)
            
            # If all of an opponents territories are taken, they are eliminated, 
            # and their cards are given to the attacker.
            if len(gameState.playerDict[attackedPlayer]["territories"]) == 0:
                click.echo(f"The {gameState.playerDict[attackedPlayer]['colour']} has been eliminated.")
                # Returns list of attacks still to be made. Does this by finding the index of the current attack
                # and finding next attack then returning slice of list containing the rest. 
                nextAttackIndex = attacks.index(attack) + 1
                return (True, attackedPlayer, attacks[nextAttackIndex:])
                
        else:
            # If territory was not captured, updates defending troop count
            gameState.map.graph.nodes[territoryIDDef]["troops"] -= troopsLostDef

        
    return (captureFlag, None, [])
       
       
# !Note: The player parameter for all turninfo related functions may not be necesarry. It could be implicit. 
def getCard(gameState : GameState) -> Card:
    """
    Gets which player drafted, how many troops they drafted, where they drafted, and whether they traded in cards.
    """    
    cardTList = [elem.name.capitalize() for elem in CardType]
    cardTypeInput = click.prompt(f"Enter the card type recieved", type=click.Choice(cardTList, case_sensitive=True), show_choices=False)
    cardType = CardType.from_str(cardTypeInput)
    if cardType != CardType.WILD:
        click.echo("Card territory. ", nl=False)
        territory = getTerritory(gameState.map, None, False)
    else :
        territory = None

    return Card(cardType, territory)
        
    

def instructFortify(fortify : Fortify, gameState : GameState):
    """
    Tells user whether to fortify, where fortify from, where to fortify to, and how many to fortify with.
    """
    if fortify is None:
        click.echo("Do not fortify.")
        
    else:  
        click.echo(f"Fortify from {gameState.map.territoryNames[fortify[0] - 1]} to {gameState.map.territoryNames[fortify[1] - 1]} with {fortify[2]} troops.")
        gameState.map.graph.nodes[fortify[0]]["troops"] -= fortify[2]
        gameState.map.graph.nodes[fortify[1]]["troops"] += fortify[2]
        
        

        



def executeAgentTurn(move: Move, gameState: GameState) -> bool:
    """
    Tells user full list of actions to to implement as instructed by the AI agent. 
    """
    
    drawBoard(gameState)
    # Gets user to input draft action into game client
    instructDraft(move[0], gameState)
    drawBoard(gameState)

    # Gets user to make attacks until all are made or they eliminate a player
    captureFlag, killedPlayer, remainingAttack = instructAttack(move[1], gameState)
    drawBoard(gameState)

    
    # If a player was killed, their cards are given to the attacker
    while killedPlayer is not None:
        # Must manually enter cards gotten
        for _ in range(gameState.playerDict[killedPlayer]["cardsNum"]):
            newCard = getCard(gameState)
            gameState.cards.append(newCard)
            
        gameState.playersAlive.remove(killedPlayer)
        
        # If only one player is left, the game is over so terminate early. 
        if len(gameState.playersAlive) == 1:
            return True
        
        
        if remainingAttack != []:
            # Allow the player to continue attacking
            _, killedPlayer, remainingAttack = instructAttack(remainingAttack, gameState)
            drawBoard(gameState)
        
        else: 
            break

        
    instructFortify(move[2], gameState)
    drawBoard(gameState)

    
    if captureFlag:
        card = getCard(gameState)
        gameState.cards.append(card)
    
    return False

    
    

def displayGameover(winnerID : int, gameState : GameState):
    """
    Outputs information about the winner of the game and any final information which might be helpful
    for testing.
    """
    click.echo(f"The game is over. The winner is {gameState.playerDict[winnerID]['colour']}!")
    click.echo("The final state of the game is as follows:")
    print(gameState)
    
