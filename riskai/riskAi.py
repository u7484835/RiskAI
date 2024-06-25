from .structures import *
from .actions import *
from typing import List, Dict
import itertools
import signal
import click
from .agentHelper import generalDraft, generalFortify
from .simpleAI import attackSimple


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
    ActionType.TAKETERRITORIES: generateTTSet(),
    ActionType.TAKECARD: generateTCSet(),
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


def generateActionSeq(actionDict : Dict[ActionType, Set[ActionSet]], length : int) -> Set[ActionSet]:
    """
    Given a list of actions, generates the sequence of actions that should be 
    taken. This should be the final step in the action generation process. 
    """
    
    if length == 1:
        return set().union(*actionDict.values())
    
    else:
        combSet = actionDict[ActionType.KILLPLAYER] | actionDict[ActionType.TAKEBONUS] | actionDict[ActionType.BREAKBONUS] | actionDict[ActionType.EXPANDBORDERS]
        combinations = {frozenset(comb) for comb in itertools.combinations(combSet, length)}
        return {comb for comb in combinations if validateActionSet(comb)}
    


def calculateAction(gameState : GameState, action : Action) -> Optional[Territories]:
    match action.action:
        case ActionType.KILLPLAYER:
            return kpData(gameState, action)
        case ActionType.TAKEBONUS:
            return tbData(gameState, action)
        case ActionType.BREAKBONUS:
            return bbDataWeakest(gameState, action)
        case ActionType.EXPANDBORDERS:
            return ebData(gameState, action)
        case ActionType.TAKETERRITORIES:
            return None
        case ActionType.TAKECARD:
            return tcData(gameState)
        case ActionType.TAKECARD:
            return None
        case _:
            raise ValueError("Invalid agent type")
        


def evalAction(action : Action) -> int:
    match action.action:
        case ActionType.KILLPLAYER:
            return 1000
        case ActionType.TAKEBONUS:
            return 300
        case ActionType.BREAKBONUS:
            return 50
        case ActionType.EXPANDBORDERS:
            return 20
        case ActionType.TAKETERRITORIES:
            return 10
        case ActionType.TAKECARD:
            return 40
        case ActionType.TAKECARD:
            return 0
        case _:
            raise ValueError("Invalid agent type")
    

# !Note: Iterative deepening search should save all maps of hard calculation  
# paths into a dictionary for lookup. Iterative deepening should then also 
# prioritise continuing from nodes which have already been calculated.
# @ This is now far beyond the scope of the project.
def calculateActionSeq(gameState : GameState, actionSet : ActionSet, depth : int) -> Optional[Tuple[Move, int]]:
    """
    Given an action from the heavily pruned list of actions, perform 
    pathing calculations using definitive action rules. Should return 
    Moves calculated and heuristic value. 
    """
    actionEval = 0
    
    totalTerritories = set()
    for action in actionSet:
        actionEval += evalAction(action)
        territories = calculateAction(gameState, action)
        if territories is None:
            if action.action == ActionType.TAKETERRITORIES:
                territories = ttData(gameState, depth)
            if action.action == ActionType.NOATTACK:
                move = (generalDraft(gameState), [], generalFortify(gameState))
                return (move, 0)
            
        totalTerritories = totalTerritories.union(territories)
    
    draft, attack, sumTroops = attackSimple(gameState, totalTerritories)
    
    fortify = generalFortify(gameState)
    
    return ((draft, attack, fortify), sumTroops, actionEval)
    
    
    
    
        
        
        




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
    actionDict = generateActionDict(gameState.agentID, gameState)
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
            
            for seq in actionSeqs:
                move, sumTroops, eval = calculateActionSeq(gameState, seq, depth)
                
                # Early stopping if sequence isn't viable
                if sumTroops * 2 > gameState.playerDict[gameState.agentID]["troops"]:
                     continue
    
                
                if eval > bestMove[1]:
                    bestMove = (move, eval)
            
            depth += 1
            actionSeqs = generateActionSeq(actionDict, depth)

        # If the search completes within time constraint, cancel the alarm
        signal.alarm(0)
        return bestMove 

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
    

    
