from .structures import *
from .actions import *
from typing import List, Dict
import itertools
import signal
import click


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



def attack(gameState : GameState, territories : Territories) -> Tuple[Draft, Attack]:
    """
    Given a list of target territories, calculates the required moves to attack 
    all of them in the most efficient possible way.
    """
    # Filter graph for only externally owned territories
    
    # node weights for MST
    
    # MST
    
    # See how long one stack can traverse, make it do so 
    pass
    
    
def findInternalTerritories(player : int, gameState : GameState) -> Territories:
    """
    For a given player, finds all territories which have no external borders.
    """
    internalTerr = []
    # Iterate through blue nodes and check their neighbours
    # Currently treating node as the int index from another list, does this work?
    for node in gameState.playerDict[player]["territories"]:
        if all(neighbour in gameState.playerDict[player]["territories"] for neighbour in gameState.graph.neighbors(node)):
            internalTerr.append(node)
    return internalTerr
    
    

def fortify(gameState : GameState, territories : Territories) -> Fortify:
    """
    Given a list of target territories, calculates the best possible 
    fortify action
    """
    # Applies a fortify heuristic? Then takes into account desired territories?
    pass
    





# !Note: Iterative deepening search should save all maps of hard calculation  
# paths into a dictionary for lookup. Iterative deepening should then also 
# prioritise continuing from nodes which have already been calculated.
def calculateActionSeq(actionSet : ActionSet) -> Tuple[Move, int]:
    """
    Given an action from the heavily pruned list of actions, perform 
    pathing calculations using definitive action rules. Should return 
    Moves calculated and heuristic value. 
    """
    pass



def generateActionDict(player: int, gameState : GameState) -> Dict[ActionType, Set[ActionSet]]:
    """
    Creates all basic actions possible from gameState for creating action sequence sets. 
    Note that sets of any length can be generated from these actions.
    """
    currentActions = {
    ActionType.KILLPLAYER: generateKPSet(player, gameState),
    ActionType.TAKEBONUS: generateTBSet(player, gameState),
    ActionType.BREAKBONUS: generateBBSet(player, gameState),
    ActionType.EXPANDBORDERS: generateEBSet(),
    ActionType.MIGRATE: generateMSet(),
    
    
    ActionType.TAKETERRITORIES: generateTTSet(),
    ActionType.TAKECARD: generateTCSet(),
    ActionType.DEFENDBORDERS: generateDBSet(),
    ActionType.NOATTACK: generateNASet(),
    }
    return currentActions




def validateActionSet(actionSet : ActionSet) -> bool:
    """
    Given a set of actions, validates whether they are mutually possible in sequence.
    """
    killSet = set()
    takeSet = set()
    breakSet = set()


    # Basic check to ensure that actions aren't attempting to kill a player and then
    # take their bonus
    for action in actionSet:
        if isinstance(action, KillPlayer):
            killSet.add(action.player)
        elif isinstance(action, BreakBonus):
            breakSet.add(action.player)
        elif isinstance(action, TakeBonus):
            takeSet.add(action.player)
            
    # Returns check of overlap. set returns true if non empty I believe    
    return not ((killSet & breakSet) or (killSet & takeSet) or (breakSet & takeSet))


def pruneActionSeq(actionSeq : ActionSet, gameState : GameState) -> bool:   
    """
    Given the a set of actions to be performed simultaniously, performs iterative 
    pruning to eliminate as many action possibilites as possible. In this case 
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
    return True


def generateActionSeq(actionDict : Dict[ActionType, Set[ActionSet]], length : int) -> Set[ActionSet]:
    """
    Given a list of actions, generates the sequence of actions that should be 
    taken. This should be the final step in the action generation process. 
    """
    
    if length == 1:
        return set().union(*actionDict.values())
    
    else:
        combSet = actionDict[ActionType.KILLPLAYER] | actionDict[ActionType.TAKEBONUS] | actionDict[ActionType.BREAKBONUS] | actionDict[ActionType.EXPANDBORDERS] | actionDict[ActionType.MIGRATE] 
        combinations = {frozenset(comb) for comb in itertools.combinations(combSet, length)}
        return {comb for comb in combinations if validateActionSet(comb)}
    


    
def depthLimitedSearch (actionDict : Dict[ActionType, Set[ActionSet]], gameState : GameState, depth : int, currBest : Tuple[int, Move]) -> Tuple[int, Move]:
    """
    A simple depth limited search which tests how effective each possible
    combinations of abstract actions is. The full calculations for each 
    action have very significant computational requirements, so it will 
    call harsh pruning functions to limit the node paths expanded drastically. 
    Note that the pruning will allow the possibility of suboptimal play. 
    """
    actionSeqs = generateActionSeq(actionDict, depth)
    prunedSeqs = {seq for seq in actionSeqs if pruneActionSeq(seq, gameState)}
    
    for seq in prunedSeqs:
        move = calculateActionNode(seq)
        if move[1] > currBest[1]:
            currBest = move
    
    return currBest

# Creating error classes and handling to implement a timer interupt for the 
# iterative deepening search.
class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Search timed out after 45 seconds")

def ids (gameState : GameState, timeConstraint : int) -> Move:    
    """
    Iterative deepening search which generates "nodes" that each represent
    an abstract action that the AI can take (such as killing a player, taking 
    a bonus etc). Given time constraints, this will perform a continuous search 
    of all possible combinations of actions until the time constraint it met. 
    It should then return the action with the highest utility as measured by the 
    heuristic function. Note that it should exit at any point during execution 
    as soon as the time constraint is met. 
    """
    actionDict = generateActionDict(gameState.currentPlayer, gameState)
    depth = 0
    bestMove = (float('-inf'), None)

    # Set up timer to interrupt after specified length of time. 
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeConstraint)

    try:
        # Perform iterative deepening search
        depth = 0
        actionSeqs = generateActionSeq(actionDict, depth)
        
        while len(actionSeqs) > 0:
            prunedSeqs = {seq for seq in actionSeqs if pruneActionSeq(seq, gameState)}
            
            for seq in prunedSeqs:
                move = calculateActionNode(seq)
                if move[1] > bestMove[1]:
                    bestMove = move
            
            depth += 1
            actionSeqs = generateActionSeq(actionDict, depth)

        # If the search completes within time constraint, cancel the alarm
        signal.alarm(0)

    except TimeoutError:
        # Handle the timeout here
        click.echo(f"Search timed out after {timeConstraint} seconds")
        return bestMove 





def riskAgent(gameState : GameState, timeConstraint : int) -> Move:
    """
    Main function to call AI agent. Gets move from iterative deepening search.
    Should define the time constraints on the search. 
    """
    return ids(gameState, timeConstraint)[0]
    

    
