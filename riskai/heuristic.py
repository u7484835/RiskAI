from .structures import *
import statistics
import math


# How much to scale the contribution of each metric to the eval
PLAYERWEIGHT = 200
TROOPWEIGHT = 20
DEFENCEWEIGHT = 10
BONUSWEIGHT = 100
TERRITORYWEIGHT = 10
CARDWEIGHT = 10
INCOMEWEIGHT = 20
DANGERWEIGHT = 100

# How much to scale down each quick opponent evaluation
OPPNORMALISE = 10



    
def findInternalTerritories(player : int, gameState : GameState) -> Territories:
    """
    For a given player, finds all territories which have no external borders.
    """
    internalTerr = []
    # Iterate through player nodes and check their neighbours
    for node in gameState.playerDict[player]["territories"]:
        # Internal territories have all neighbours owned by the player
        if all(neighbour in gameState.playerDict[player]["territories"] for neighbour in gameState.map.graph.neighbors(node)):
            internalTerr.append(node)
    return internalTerr



def findBorders(player : int, gameState : GameState) -> Territories:
    """
    Finds player borders which are chokepoints defending a bonus, or otherwise constitute the outside 
    region of a player's central mass. Defining all useful border territories to also be border territories 
    of bonuses. Typical play has player's using borders directly on top of bonuses, or a single tile over so 
    this is a useful metric. 
    """
    # Gets all classified borders owned by player
    ownedBorders = gameState.map.borderTerr & gameState.playerDict[player]["territories"]
    internalTerr = findInternalTerritories(player, gameState)
    # Removes all bonus borders which are internal
    return ownedBorders - internalTerr
  
  
  
  
  

"""
Here is the full list of considerations for the heuristic function. Note 
that currently not all considerations have been implemented. 
  - Number of players: having less players is hugely preferrable
    
  - Player relationships: Having friendly relationships is very beneficial, 
  conversely vengence or hatred is very bad in human games. According to the 
  player matrix, high aggressions between two non-user players is very 
  favourable. 
  
  - Amount of troops: should be measured in relation to everyone else
  
  - Troop density: Concentrated stacks are very preferrable
  
  - Bonuses: Having strong bonuses is vital
  
  - Defence points: fewest points of defence 
  
  - Bonus defence: Borders strong enough to disuade attacks is necessary
    (it is unlikely troop counts allow for entirely negative attacks)
    
  - Player proximity: It is best to have distance for expansion
  
  - Untaken bonus proximity: Maneuvering for bonuses is key
  
  - Card count + values
  
  - Territories: Gives passive troops and is important    
  
  - Danger by troops/bonuses/cards/ aggression from other players is vital
"""

def heuristic(gameState : GameState) -> int:
    """
    Calculates how favourable the current GameState is. Considerations are listed above. 
    Achieves this calculation by first calculating the agent's position as primary metric. 
    Then assesses the quality of position of all other players, and biases against their 
    positive outcomes. Weights for internal heuristic bias are constants set at top of file. 
    """
    # Initialise eval
    eval = 0
    
    # Agent should strongly bias towards removing players
    numPlayers = len(gameState.playersAlive)
    eval -= numPlayers * PLAYERWEIGHT
    
    # @Relationships not done 
    
    # Get troop total metrics
    troopList = [gameState.playerDict[player]["troops"] for player in gameState.playersAlive]
    avgTroops = sum(troopList) / numPlayers
    medianTroops = statistics.median(troopList)
    
    # Agent should bias towards having more troops than average. Median total 
    # is also added to prevent outliers from swaying eval. 
    eval += (avgTroops - gameState.playerDict[gameState.agentID]["troops"]) * TROOPWEIGHT 
    eval += (medianTroops - gameState.playerDict[gameState.agentID]["troops"]) * TROOPWEIGHT   
      
    # Fewer defence choke points is preferred
    eval -= len(findBorders(gameState.agentID, gameState)) * DEFENCEWEIGHT
    
    # Agent should bias towards owning territories
    eval += len(gameState.playerDict[gameState.agentID]["territories"]) * TERRITORYWEIGHT
    
    for card in gameState.cards:
        eval += card.type.value * CARDWEIGHT
        
    for bonus in gameState.playerDict[gameState.agentID]["bonusHeld"]:
        eval += gameState.map.bonuses[bonus]["bonusVal"] * BONUSWEIGHT
    
    # Temp value for opponent evaluation
    oppEval = 0    
    
    # Loops over opponent players. The stronger they are, the more undesirable 
    # the state is. 
    for opponent in gameState.playersAlive:
      # Ensure only alive opponents are considered, filters out agent
      if opponent != gameState.agentID:
        # Add their bonuses to quick calculation
        for bonus in gameState.playerDict[opponent]["bonusHeld"]:
          oppEval += gameState.map.bonuses[bonus]["bonusVal"] * BONUSWEIGHT
        
        # Add their previous income
        oppEval += gameState.playerDict[opponent]["prevIncome"] * INCOMEWEIGHT
        
        # Add their card count. Assumes an average card value of 8
        oppEval += gameState.playerDict[opponent]["cardsNum"] * 8 * CARDWEIGHT
        
        # @Consider adding their defence points in the future. For now it is a costly calculation
        
        # Danger is approxiated by how much of the map a player owns. The troopScale function 
        # is an approximation of 1.1/pi * atan(10x - 3.5) + 0.5, which scales from 0 to 1.
        # This function acts on the percentage of the map owned by the player, and decrees 
        # that players should be considered dangerous if they hit a critical percent of map ownership
        terrPerc = len(gameState.playerDict[opponent]["territories"]) / len(gameState.map.graph.nodes())
        troopScale = 0.35 * math.atan(10*terrPerc - 3.5) + 0.5
        oppEval += int(troopScale * DANGERWEIGHT)     
        
        
        # Subtract how favourable the state is for the opponent from the eval
        eval -= (oppEval // OPPNORMALISE)
        # Reset for next loop
        oppEval = 0
    
    
    return eval
