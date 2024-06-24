from .structures import *
from .actions import *
from typing import List, Dict
import itertools
from .riskAI import makeTrade, draftTroopsAmount, stackSelect
from .dice import perfectDice
from .drawInterface import drawArborescence, drawPath
from .heuristic import findBorders, findInternalTerritories




def weightNode(node : int, gameState : GameState, territories : Territories) -> int:
    """
    Given a node, calculates the weight of the node based on the current game state and territories. 
    """
    # The weight of nodes are assigned orders of magnitude. The 10^0 order is for territories
    # to capture as these are by far the most desirable. The 10^2 order is for territories which 
    # are from an attacking stack as they should be undesirable but used frequently. The 10^4 order
    # is for neutral territories which should not be attacked unless necessary. A 10^2 difference 
    # in magnitude is used to clearly ensure the MSA algorithm prioritises the correct territories. 
    
    
    
    # Weights are calculated based on the number of troops in the territory, the number of adjacent 
    # enemy territories, and the number of adjacent friendly territories. 
    nodeWeight = 0
    
    # If the territory is owned by the player, the weight is the number of troops in the territory
    if gameState.map.graph.nodes[node]["player"] == gameState.agentID:
        # Balances troop sum to be relative to player's total troop count to ensure comparison is 
        # normalised for games with many and few troops. 
        return (gameState.map.graph.nodes[node]["troops"] // gameState.playerDict[gameState.map.graph.nodes[node]["player"]]["troops"] )* 100
        
        
    # If the territory is not owned by the player, the weight is the number of troops in the territory 
    # plus the number of adjacent friendly (territories to attack) territories minus the number of 
    # adjacent enemy territories. 
    else:
        # Normalises troop weight
        nodeWeight = gameState.map.graph.nodes[node]["troops"] // gameState.playerDict[gameState.map.graph.nodes[node]["player"]]["troops"] 
        
        nodeWeight += len(list(gameState.map.graph.neighbors(node))) // 10
        
        for neighbour in gameState.map.graph.neighbors(node):
            if neighbour in territories:
                nodeWeight -= 0.1
            elif gameState.map.graph.nodes[neighbour]["player"] != gameState.agentID:
                nodeWeight += 0.1
                
    if node not in territories:
        nodeWeight = nodeWeight * 10000
                     
    return nodeWeight


def attackGraphSimple(gameState : GameState, territories : Territories) -> Tuple[nx.DiGraph, int, int]:
    """
    Given a list of target territories, calculates the optimal attacking graph. Outputs the graph,
    the stack attacking from, and the sum of all troops on territories to attack
    """
    # Firstly removes all owned territories from a copied graph so that we 
    # can search only on the attackable space. 
    filterGraph = gameState.map.graph.copy()
    filterGraph.remove_nodes_from(gameState.playerDict[gameState.agentID]["territories"])
    
    # Check if all territories to capture are even connected
    
    components = nx.connected_components(filterGraph)
    
    foundComponent = {} 
    foundFlag = False
    
    for component in components:
        if all(terr in component for terr in territories):
            foundComponent = component
            foundFlag = True
            break
    
    if not foundFlag:
        return None
    
    # Get all stacks with large enough size
    stacks = stackSelect(gameState, gameState.agentID)
    
    # Filter to stacks which have a connection to the component
    filteredStacks = set()
    for stack in stacks:
        if any(neigh in foundComponent for neigh in gameState.map.graph.neighbors(stack)):
            filteredStacks.add(stack)
            
    """ Suggested code to streamline prcess 
    filteredStacks = {stack for stack in stacks if any(neigh in foundComponent for neigh in gameState.graph.neighbors(stack))} """
            
            
    # Getting base graph to perform MSA over
    componentGraph = gameState.map.graph.subgraph(foundComponent)
    
    # Removes all edges from the graph. Could be an inefficient process
    # componentGraph.remove_edges_from(list(componentGraph.edges))
    
    
    weightDict = {node : weightNode(node, gameState, territories) for node in componentGraph.nodes()}
 
    directedGraph = nx.DiGraph(componentGraph)
    
    # Unsure as to whether this correctly creates the directed graph
    for u, v in componentGraph.edges():
        directedGraph.add_edge(u, v, weight=weightDict[v])
        directedGraph.add_edge(v, u, weight=weightDict[u])
        
    minTroops = float('inf')
    minBranches = float('inf')
    minArborescence = nx.DiGraph()
    minStack = 0    
    
    for stack in filteredStacks:
        print("Stack is ", stack)
        
        # Add stack node to the graph for MSA 
        directedGraph.add_node(stack)
        
        # Add paths exiting the stack to the component to attack
        for neighbour in gameState.map.graph.neighbors(stack):
            if neighbour in foundComponent:
                # They should only be in the direction away from the stack
                directedGraph.add_edge(stack, neighbour, weight=weightDict[neighbour] // 10)
                
                
        # Make arborescence
        arborescence = nx.minimum_spanning_arborescence(directedGraph)
    
        # Filter out neutral territories as best as possible
        # Get all neutral nodes which are not desired to attack and are not the 
        # stack attacking from 
        neutralNodes = set(arborescence.nodes()) - territories - {stack}
        print("Neutral nodes")
        print(neutralNodes)
        print(type(neutralNodes))
        drawArborescence(gameState, arborescence, (stack + 100))
       
        # Loop until no more neutral nodes can be removed
        trimmedNode = True 
        while trimmedNode:
            trimmedNode = False
            
            # Creates a list so there is a separate object to loop over while neutral nodes is modified
            for node in list(neutralNodes):
                # If neutral node is a leaf then remove it
                print("curr node is ", node)
                if (arborescence.out_degree(node)) == 0:
                    print("Trimmed a node")
                    arborescence.remove_node(node)
                    # Importantly removes node from list of nodes to search and trim
                    neutralNodes.remove(node)

                    trimmedNode = True
                    
        drawPath(gameState, arborescence, stack)

        
        # Check how optimal the arborescence is
        tempTroops = 0 
        
        for node in arborescence.nodes():
            tempTroops += gameState.map.graph.nodes[node]["troops"]
            
        # Updates minimum arborescence if it requires less troop expenditure
        if tempTroops < minTroops:
            minTroops = tempTroops
            
            # The continuity of the path found is used as a tiebreaker. 
            # Ideally, the path should branch as few times as possible.
            minBranches = 0
            for deg in dict(arborescence.out_degree()).values():
                if deg > 1:
                    minBranches += deg
            
            minStack = stack
            minArborescence = arborescence
            
        # Perform tiebreak     
        elif tempTroops == minTroops:
            tempBranches = 0
            for deg in dict(arborescence.out_degree()).values():
                if deg > 1:
                    tempBranches += deg
            
            if tempBranches < minBranches:
                minBranches = tempBranches
                minStack = stack
                minArborescence = arborescence
                
        # Remove stack node from the graph to clean for next iteration
        directedGraph.remove_node(stack)
        
    return (minArborescence, minStack, minTroops)
      
      
      
      
def simpleDraft(gameState : GameState, stack : int) -> Draft:
    """
    Gets optimal greedy draft and places all troops onto attacking stack. 
    """
    tradeList = makeTrade(gameState)
        
    draftAmount = draftTroopsAmount(gameState, tradeList)
    
    return (tradeList, [(stack, draftAmount)])


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



def graphToAttackRec(gameState : GameState, attackGraph : nx.DiGraph, currNode : int, currTroops: int) -> Attack:
    """
    Functional programming style recursive function to create lists of attacks down a branch
    """
    if attackGraph.out_degree(currNode) == 0:
        return []    
          
    # Gets a list of how to distribute troops
    splitList = splitTroops(currTroops, len(attackGraph.neighbors(currNode)))
    splitIndex = 0
    
    addingList = []    
    for neighbour in attackGraph.nodes[currNode].neighbors:
        # Always asks for perfect attack currently, no matter how many troops there are
        # Also moves troops assuming no losses. !Should be revamped in the future.
        thisAttack = (currNode, neighbour, perfectDice(gameState.map.graph.nodes[neighbour]["troops"]), currTroops)
        addingList += [thisAttack]
        
        # Recurses until all branches are added
        addingList += graphToAttackRec(gameState, attackGraph, neighbour, splitList[splitIndex])
        splitIndex += 1     
        
    return addingList   

# For multi stack expansion make stack a list of ints and troops a list of troop nums associated 
# with that amount 
def graphToAttack(gameState : GameState, attackGraph : nx.DiGraph, stack : int, troops : int) -> Attack:
    """
    Generates attack based on attack graph, moving all troops if possible, and 
    splitting troops on branches.
    """
    return graphToAttackRec(gameState, attackGraph, stack, troops)


        
def attackSimple(gameState : GameState, territories : Territories) -> Optional[Tuple[Draft, Attack]]:
    attackGraph, stack, sumTroops = attackGraphSimple(gameState, territories)
    
    if sumTroops * 2 > gameState.playerDict[gameState.agentID]["troops"]:
        return None
    
    draft = simpleDraft(gameState, stack)
    
    # Creates dict out of list of draft, troop tuples to quickly get stack deploy amount
    draftDict = {id: value for id, value in draft[1]}
    
    # Gets troops number by amount of current troops plus draft amount
    attack = graphToAttack(gameState, attackGraph, stack, gameState.map.graph.nodes[stack]["troops"] + draftDict[stack])
    
    return (draft, attack)



def generalDraft(gameState : GameState, territories : Territories) -> Draft:
    pass


    
def generalAttack(gameState : GameState, territories : Territories) -> Tuple[Draft, Attack]:
    """
    Given a list of target territories, calculates the required moves to attack 
    all of them in the most efficient possible way.
    """
    pass
    
    
def attackTerritory(gameState : GameState, territories : Territories) -> Tuple[Draft, Attack]:
    """
    Given a list of target territories, calculates the required moves to attack 
    all of them in the most efficient possible way.
    """
    pass    

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
    

def generalFortify(gameState : GameState) -> Fortify:
    """
    Given a list of target territories, calculates the best possible 
    fortify action
    """
    # Attempts to shore up gaping hole in defences
    
    borders = findBorders(gameState.agentID, gameState)
    minBorder = min(borders)
    
    
    # For owned (or nearly owned) bonuses, 
        # - checks all borders to see weak points, 
        # - finds troops to disperse
    
    # Attempts to reclaim distant stack
    
    # For all stacks 
        # checks if stack is distant to bonuses
        # returns stack to bonus
    
    # Attempts to ferry troops from internal territories
    
    # For all internal territories
        # checks if territory has too many troops
        # returns troops to border
    
    # Increases troop density 
    # Takes second least dense stack and merges.
    
    
    stacks = stackSelect(gameState, gameState.agentID)
    
    
    
    
    
    # Applies a fortify heuristic? Then takes into account desired territories?
    pass
    







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





