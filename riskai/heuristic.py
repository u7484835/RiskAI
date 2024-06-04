from .structures import *



def heuristic(gameState : GameState) -> int:
    return 100

def gameStateHeuristic(gameState : GameState) -> int:
    """
    Calculates how favourable the current GameState is. Considerations should be:
    
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
    pass
