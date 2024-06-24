from .structures import *
from .actions import *
from typing import List, Dict
import itertools
import signal
import click


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


def weightNodes(gameState : GameState, graph : nx.Graph, territories : Territories) -> Dict[int, int]:
    # Stack Nodes are infinity
    
    # Neutral Territories are very high 
    
    # Territories to attack are very low
    
    # "Corner" territories to attack are a bit higher
        # Dictionary to store the weights of edges
    pass

    # See how long one stack can traverse, make it do so 
    
    
def attack(gameState : GameState, territories : Territories) -> Tuple[Draft, Attack]:
    """
    Given a list of target territories, calculates the required moves to attack 
    all of them in the most efficient possible way.
    """
    # Filter graph for only externally owned territories
    stacks = stackSelect(gameState, gameState.agentID)
    bestPathCost = float('inf')
    
    for stack in stacks:
        # Create graph with only enemy territories other than the stack
        filterGraph = gameState.graph.copy()
        nonStackOwned = gameState.playerDict[gameState.agentID]["territories"] - stack
        filterGraph.remove_nodes_from(nonStackOwned)
        components = nx.connected_components(filterGraph)
                        
    pass
    
    
    

def fortify(gameState : GameState, territories : Territories) -> Fortify:
    """
    Given a list of target territories, calculates the best possible 
    fortify action
    """
    # Applies a fortify heuristic? Then takes into account desired territories?
    pass
    

def calculateActionNode(actionSet : ActionSet) -> Tuple[Move, int]:
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


# @ Will not implement pruning
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
    

    
