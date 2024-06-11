from .structures import *
from .actions import *
from typing import List, Dict
import random
from .riskAI import makeTrade, draftTroopsAmount



def randDraft(gameState : GameState) -> Draft:
    """
    Gets all possible trades to make, actions all of them, then 
    drafts all available troops to a single territory. 
    """
    tradeList = makeTrade(gameState)
        
    draftAmount = draftTroopsAmount(gameState, tradeList)
    
    territoriesList = list(gameState.playerDict[gameState.agentID]["territories"])
        
    draftTerr = random.choice(territoriesList)
    
    return (tradeList, [(draftTerr, draftAmount)])
    



def randAttack(gameState : GameState) -> Attack:
    """
    Randomly selects an attack to make. 
    """
    attackable = []
    for node in gameState.playerDict[gameState.agentID]["territories"]:
        if gameState.map.graph.nodes[node]["troops"] > 1:
            for neighbour in gameState.map.graph.neighbors(node):
                if gameState.map.graph.nodes[neighbour]["player"] != gameState.agentID:
                    attackable.append((node, neighbour))
    # Get all possible attacks
    
    if len(attackable) == 0:
        return []
    else:
        randAttack = random.choice(attackable)
        attack = (randAttack[0], randAttack[1], gameState.map.graph.nodes[node]["troops"], gameState.map.graph.nodes[node]["troops"])
        return [attack]
    
    
def randFortify(gameState : GameState) -> Fortify:
    """
    Randomly selects a fortify to make. 
    """
    fortifiable = []
    for node in gameState.playerDict[gameState.agentID]["territories"]:
        if gameState.map.graph.nodes[node]["troops"] > 1:
            for terr in gameState.playerDict[gameState.agentID]["territories"]:
                if terr != node:
                    fortifiable.append((node, terr))
    # Get all possible fortifies
    
    if len(fortifiable) == 0:
        return None
    else:
        randFortify = random.choice(fortifiable)
        return (randFortify[0], randFortify[1], gameState.map.graph.nodes[randFortify[0]]["troops"] - 1)
    

def randAI(gameState : GameState) -> Move:
    """
    Randomly selects a move to make. 
    """
    return (randDraft(gameState), randAttack(gameState), randFortify(gameState))