import click
from structures import *
from actions import *


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

# !Note: Iterative deepening search should save all maps of hard calculation  
# paths into a dictionary for lookup. Iterative deepening should then also 
# prioritise continuing from nodes which have already been calculated.
def calculateActionNode(action : Action) -> Tuple[Move, int]:
    """
    Given an action from the heavily pruned list of actions, perform 
    pathing calculations using definitive action rules. Should return 
    Moves calculated and heuristic value. 
    """
    pass

def pruneActionNodes():
    """
    Given the output of generateActionNodes(), performs iterative pruning 
    to eliminate as many action possibilites as possible. In this case 
    "iterative" means that it should do as many simple checks for each 
    action's viability as possible before serious calculations. This is 
    essentially finding the lower bound of action cost, comparing it with 
    the upper bound of action reward, and determining whether the action 
    is profitable. Returns a list of viable actions for concrete 
    calculations and heuristics.
    """
    
    # Example pseudo code for pruning the killPlayer action:
    #  - calculate the simple expected value of remaining troops and 
    #    cards, territories and bonuses after killing the player.
    #  - if profitable, do a super auto pets style expected value 
    #    attacks of largest owned troop stacks attacking theirs, and 
    #    second largest, down to the smallest. Recalculate troop distribution
    #    and profitability. If still profitable, return the action for future 
    #    pathing calculations. 
    pass

def generateActionNodes():
    """
    Given a node in the action search tree, creates new possible action nodes
    according to simple action logic. For example, killing a player should 
    be considered a "clean slate" where all other aggressive and neutral actions 
    are possible. After any attacking moves have already been taken, actions like 
    "take a card" and "no attacks" are redundant. Should act with high pruning 
    intent rather than an a comprehensive search. 
    """
    pass

def depthLimitedSearch (gameState : GameState, depth : int) -> Move:
    """
    A simple depth limited search which tests how effective each possible
    combinations of abstract actions is. The full calculations for each 
    action have very significant computational requirements, so it will 
    call harsh pruning functions to limit the node paths expanded drastically. 
    Note that the pruning will allow the possibility of suboptimal play. 
    
    Requires:
        - `generateActionNodes()`
        - `pruneActionNodes()`
        - `calculateActionNode()`
        - `gameStateHeuristic()`
    """
    pass

def ids (gameState : GameState, timeConstraint : int) -> Move:    
    """
    Iterative deepening search which generates "nodes" that each represent
    an abstract action that the AI can take (such as killing a player, taking 
    a bonus etc). Given time constrains, this will perform a continuous search 
    of all possible combinations of actions until the time constraint it met. 
    It should then return the action with the highest utility as measured by the 
    heuristic function. Note that it should exit at any point during execution 
    as soon as the time constraint is met. 
    
    Requires:
        - `depthLimitedSearch()`
    """
    pass 



def riskAgent(gameState : GameState) -> Move:
    """
    Main function to call AI agent. Gets move from iterative deepening search.
    Should define the time constraints on the search. 
    
    Requires:
        - `ids()`
    """
    pass
    
    
    
