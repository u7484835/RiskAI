from .structures import *
from .actions import *
from typing import List
from .heuristic import findBorders, findInternalTerritories



# ---------------------------- Agent Helper Functions ----------------------------
# General purpose functions for use in the AI which can be utilised by any agent. 


def firstTrade(gameState : GameState) -> Optional[Trade]:
    """
    Chooses the most optimal trade to make based on the current game state. And 
    returns the action to make it immediately. 
    """
    cards = gameState.cards
    
    if len(cards) < 3:
        return None

    # Count the number of each type of card
    typeDict = {CardType.INFANTRY: {}, CardType.CAVALRY: {}, CardType.ARTILLERY: {}, CardType.WILD: {}}
    for card in cards:
        typeDict[card.type].add(card)
        
        

    # Check for one of each type
    if len(typeDict[CardType.INFANTRY]) > 0 and len(typeDict[CardType.CAVALRY]) > 0 and len(typeDict[CardType.ARTILLERY]) > 0:
        # Searches for cards with +2 bonus owned
        bonusCards = [card for card in cards if card.territory in gameState.playerDict[gameState.agentID]["territories"]]
        tradeList = []
        seenTypes = set()

        # Adds if possible
        if len(bonusCards) > 0:
            tradeList.append(bonusCards[0])
            seenTypes.add(bonusCards[0].type)
            # Removes from game structures as it is used
            gameState.playerDict[gameState.agentID]["cards"].remove(bonusCards[0])

        # Gets first possible cards of other types without bonuses if possible
        for card in cards:
            if card.type not in seenTypes and card not in bonusCards:
                tradeList.append(card)
                seenTypes.add(card.type)
                
                # Removes from player's hand as it is used
                gameState.playerDict[gameState.agentID]["cards"].remove(card)

                
                if len(seenTypes) == 3:
                    break
                
        # If not adds bonus cards, searching again 
        for card in bonusCards:
            if card.type not in seenTypes:
                tradeList.append(card)
                seenTypes.add(card.type)
                
                # Removes from player's hand as it is used
                gameState.playerDict[gameState.agentID]["cards"].remove(card)

                
                if len(seenTypes) == 3:
                    break
        
        if len(tradeList) != 3:
            RuntimeError("Different trade list not of length 3")
                
        return tuple(tradeList)
    
    
    # Check for three cards of the same type, loops to check highest 
    # val triple trade first
    for cType in [CardType.ARTILLERY, CardType.CAVALRY, CardType.INFANTRY]:
        # Checks if there are enough cards to trade
        if len(typeDict[cType]) + len(typeDict[CardType.WILD]) >= 3:
            currTrade = []
            
            # Gets cards which are owned and give +2 bnus
            bonusCards = [card for card in typeDict[cType] if card.territory in gameState.playerDict[gameState.agentID]["territories"]]
            if len(bonusCards) > 0:
                # Adds a single bonus card
                currTrade.append(bonusCards[0])
                gameState.playerDict[gameState.agentID]["cards"].remove(card)
                typeDict[cType].remove(card)

            # Attempts to add non bonus cards to complete trade
            for card in typeDict[cType]:
                if card not in bonusCards:
                    currTrade.append(card)
                    gameState.playerDict[gameState.agentID]["cards"].remove(card)
                    
                    if len(currTrade) == 3:
                        return tuple(currTrade)
                    
            # If not, adds unused bonus carsd too to trade
            for card in bonusCards:
                currTrade.append(card)
                gameState.playerDict[gameState.agentID]["cards"].remove(card)
                
                if len(currTrade) == 3:
                    return tuple(currTrade)
                
            # If not enough cards of the one type, adds wilds until trade is made
            for card in typeDict[CardType.WILD]:
                currTrade.append(card)
                gameState.playerDict[gameState.agentID]["cards"].remove(card)
                
                if len(currTrade) == 3:
                    return tuple(currTrade)
                
            RuntimeError("Same card trades not enough cards")
                
    # ! No inclusion of wild cards for different trade. 
    return None


def makeTrade(gameState : GameState) -> list[Trade]:
    """
    From GameState gets list of the near optimal greedy trading sequence, 
    trading in as many cards as possible and maximising value of trades, 
    using owned bonuses if available but without wasting them, and using 
    wild cards sparringly. 
    """
    tradeList = []
    trade = firstTrade(gameState)
    
    while trade is not None:
        tradeList.append(trade)
        trade = firstTrade(gameState)
    
    return tradeList


def tradeAmount(trade : Trade) -> int:
    """
    Calculates the number of troops to be awarded based on the trade.
    """
    if trade is None:
        return 0
    
    # If cards of the same type give 4, 6, 8 as needed. Enum stores 
    # val of card types for 3 trade. 
    if trade[0].type == trade[1].type == trade[2].type:
        return trade[0].type.value
    
    # If it is not three of the same it must be 3 unique 
    # and give 10. Note that this allows for 3 wild cards, 
    # which is not technically possible but still valid behaviour.
    return 10


def draftTroopsAmount(gameState : GameState, tradeList : List[Trade]) -> int:
    """
    Calculates the number of troops to be drafted based on the current game state and trade list.
    """
    # Troops generated from territories is total int div 3
    terrTroops = len(gameState.playerDict[gameState.agentID]["territories"]) // 3
    
    # Loops through owned bonuses, gets all values
    bonusTroops = 0
    for bonus in gameState.playerDict[gameState.agentID]["bonusesHeld"]:
        bonusTroops += gameState.map.bonuses[bonus]["bonusVal"]
    
    # Calculate the number of troops to be drafted based on the number of territories owned
    troopsToDraft = max(terrTroops + bonusTroops, 3)
    
    # Calculate the additional troops to be drafted based on the trade list
    for trade in tradeList:
        troopsToDraft += trade.bonus
        
    return troopsToDraft




def ownedTerrConnected(player : int, gameState : GameState, terr1 : int, terr2 : int) -> bool:
    """
    Given a player and two territories, checks if they are connected by owned territories. Used to 
    determine whether a player can fortify from one location to another. 
    """
    # Create a subgraph containing only nodes owned by the player
    playerSubgraph = gameState.map.graph.subgraph(gameState.playerDict[player]["territories"])
    
    # Check if there is a path between terr1 and terr2 in the subgraph
    return nx.has_path(playerSubgraph, terr1, terr2)

    




    
    
    
    



def stackSelect(gameState : GameState, player: int) -> Territories:
    """
    Generally, optimal play is to have a very high troop
    density, with troops placement tending to be 1 in all internal and non-important territories, and 
    as high as possible for critical and mobile locations. Selects the territories which are considered
    a "stack" with a significant amount of troops. This is both relative to the player and the game. Stacks
    should have a significant % of the players troops, and it should also be considered in comparison to 
    other players totals. Beyond a certain point, say 10 troops these territories have significant mobility and attacking 
    power and should also be considered stacks. 
    """
    # This defines a stack to have at least 10% of the player's total troops. Should and can be changed during testing. 
    totalTroopPercent = 10
    percCutoff = gameState.playerDict[player]["troops"] // totalTroopPercent
    
    # Any territories with more than 10 troops are considered stacks
    largeStackSize = 10
    
    stacks = {
    terr for terr in gameState.playerDict[player]["territories"]
    if gameState.map.graph.nodes[terr]["troops"] >= percCutoff or gameState.map.graph.nodes[terr]["troops"] >= largeStackSize
    }   
    
    return stacks


def weightNode(node : int, gameState : GameState, territories : Territories) -> int:
    """
    Given a node, calculates the weight of the node based on the current game state and territories. 
    """
    # Weights are calculated based on the number of troops in the territory, the number of adjacent 
    # enemy territories, and the number of adjacent friendly territories. 
    nodeWeight = 0
    
    # If the territory is owned by the player, the weight is the number of troops in the territory
    if gameState.map.graph.nodes[node]["player"] == gameState.agentID:
        nodeWeight = gameState.map.graph.nodes[node]["troops"]
        
    # If the territory is not owned by the player, the weight is the number of troops in the territory 
    # plus the number of adjacent friendly territories minus the number of adjacent enemy territories
    else:
        nodeWeight = gameState.map.graph.nodes[node]["troops"]
        
        for neighbour in gameState.map.graph.neighbors(node):
            if neighbour in territories:
                nodeWeight += 1
            elif gameState.map.graph.nodes[neighbour]["player"] != gameState.agentID:
                nodeWeight -= 1
                
    return nodeWeight


# Separated from rest due to function usage
def bbDataClosest(gameState : GameState, bb : BreakBonus) -> Optional[Territories]:
    bonusBorders = gameState.map.bonuses[bb.bonus]["territories"] & gameState.map.borderTerr
    
    stacks = stackSelect(gameState, gameState.agentID)
    
    minLen = float("inf")
    minAtt = None
    
    for stack in stacks:
        for terr in bonusBorders:
            pathLen = nx.shortest_path(gameState.map.graph, source=stack, target=terr)
            if pathLen < minLen:
                minLen = pathLen
                minAtt = terr
    
    if minAtt is None:
        return None    
    return {minAtt}



def splitTroops(troopsNum : int, numSplits : int) -> List[int]:
    """
    Splits the troops for each branch as evenly as possible, 
    spreading the remainder to the first few territories.  
    """
    splitTroops = [troopsNum // numSplits] * numSplits
    
    # Distribute remaining troops as evenly as possible
    for i in range(troopsNum % numSplits):
        splitTroops[i] += 1
        
    return splitTroops




def generalDraft(gameState : GameState) -> Draft:
    """
    Gets all possible trades to make, actions all of them, then 
    drafts all available troops to a needed border, and if not, the largest stack.
    """
    tradeList = makeTrade(gameState)
        
    draftAmount = draftTroopsAmount(gameState, tradeList)
    
    # Attempts to shore up gaping hole in defences
    borders = findBorders(gameState.agentID, gameState)
    if len(borders) != 0:
        return (tradeList, [(min(borders), draftAmount)]) 
        
    # If not, drafts to largest stack
    stacks = stackSelect(gameState, gameState.agentID)
    return (tradeList, [(max(stacks), draftAmount)]) 
    

def contestedBonuses(player : int, gameState : GameState) -> set[str]:
    """Gets list of which bonuses are planned to be taken by the agent"""
    contestedBonuses = set()
    
    for bonus in gameState.map.bonuses:
        # Planned bonuses cannot already be taken
        if bonus not in gameState.playerDict[player]["bonuses"]:
            # Check how many territories are owned by the agent
            terrsOwned = len(gameState.map.bonuses[bonus]["territories"] & gameState.playerDict[player]["territories"])
            # If the agent owns more than half of the territories in the bonus, it is contested
            if terrsOwned / len(gameState.map.bonuses[bonus]["territories"]) > 0.5:
                contestedBonuses.add(bonus)
    
    return contestedBonuses
    
    
    
    

"""    
Pseudocode for a more ideal fortify function. The current one is bare bones, 
this would be an extended implementation. 

    For owned (or nearly owned) bonuses, 
        - checks all borders to see weak points, 
        - finds troops to disperse
    
    Attempts to reclaim distant stack
    
    For all stacks 
        checks if stack is distant to bonuses
        returns stack to bonus
    
    Attempts to ferry troops from internal territories
    
    For all internal territories
        checks if territory has too many troops
        returns troops to border
    
    Increases troop density 
    Takes second least dense stack and merges.

"""    
    

def generalFortify(gameState : GameState) -> Fortify:
    """
    Given a list of target territories, calculates the best possible 
    fortify action
    """
    fortTo = None
    
    # Attempts to shore up gaping hole in defences
    
    borders = findBorders(gameState.agentID, gameState)
    if len(borders) != 0:
        fortTo = min(borders)
        
    
    stacks = stackSelect(gameState, gameState.agentID)
    internalTerr = findInternalTerritories(gameState.agentID, gameState)
    
    # Defaults to fortify to largest stack
    fortTo = max(stacks)
        
    
    # Checks if there is internal stack to move
    internalStacks = stacks & internalTerr
    for stack in internalStacks:
        # Checks it has enough troops to fortify, checks if fortify is valid
        if gameState.map.graph.nodes[stack]["troops"] > 1 and stack != fortTo and ownedTerrConnected(gameState.agentID, gameState, stack, fortTo):
            # Fortifies all troops
            return (stack, fortTo, gameState.map.graph.nodes[stack]["troops"] - 1)
        
    # Checks if there is internal terr to move
    for stack in internalTerr:
        # Checks if fortify is valid
        if gameState.map.graph.nodes[stack]["troops"] > 1 and stack != fortTo and ownedTerrConnected(gameState.agentID, gameState, stack, fortTo):
            # Fortifies all troops
            return (stack, fortTo, gameState.map.graph.nodes[stack]["troops"] - 1)
        
    # Else return none
    return None