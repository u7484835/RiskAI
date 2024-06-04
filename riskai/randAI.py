from .structures import *
from .actions import *
from typing import List, Dict
import random

def firstTrade(gameState : GameState) -> Optional[Trade]:
    """
    Chooses the most optimal trade to make based on the current game state. And 
    returns the action to make it immediately. 
    """
    cards = gameState.playerDict[gameState.agentID]["cards"]
    
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



def randDraft(gameState : GameState) -> Draft:
    """
    Gets all possible trades to make, actions all of them, then 
    drafts all available troops to a single territory. 
    """
    tradeList = makeTrade(gameState)
        
    draftAmount = draftTroopsAmount(gameState, tradeList)
        
    draftTerr = random.choice(gameState.playerDict[gameState.agentID]["territories"])
    
    return (tradeList, [(draftTerr, draftAmount)])
    



def randAttack(gameState : GameState) -> Attack:
    """
    Randomly selects an attack to make. 
    """
    attackable = []
    for node in gameState.playerDict[gameState.agentID]["territories"]:
        if gameState.graph.nodes[node]["troops"] > 1:
            for neighbour in gameState.graph.neighbors(node):
                if gameState.graph.nodes[neighbour]["player"] != gameState.agentID:
                    attackable.append((node, neighbour))
    # Get all possible attacks
    
    if len(attackable) == 0:
        return []
    else:
        randAttack = random.choice(attackable)
        attack = (randAttack[0], randAttack[1], gameState.graph.nodes[node]["troops"], gameState.graph.nodes[node]["troops"])
        return [attack]
    
    
def randFortify(gameState : GameState) -> Fortify:
    """
    Randomly selects a fortify to make. 
    """
    fortifiable = []
    for node in gameState.playerDict[gameState.agentID]["territories"]:
        if gameState.graph.nodes[node]["troops"] > 1:
            for neighbour in gameState.graph.neighbors(node):
                if gameState.graph.nodes[neighbour]["player"] == gameState.agentID:
                    fortifiable.append((node, neighbour))
    
    # Get all possible fortifies
    
    if len(fortifiable) == 0:
        return None
    else:
        randFortify = random.choice(fortifiable)
        return (randFortify[0], randFortify[1], gameState.graph.nodes[node]["troops"] - 1)
    

def randAI(gameState : GameState) -> Move:
    """
    Randomly selects a move to make. 
    """
    return (randDraft(gameState), randAttack(gameState), randFortify(gameState))