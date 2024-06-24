from .structures import *
from .actions import *
from .drawInterface import drawArborescence, drawPath
from .simpleAI import stackSelect, weightNode
from .heuristic import findInternalTerritories


# Does not work as arborescence is the wrong function for the task. Could try territory drafting process. 
def attackGraphMulti(gameState : GameState, territories : Territories) -> Tuple[nx.DiGraph, set[int], int]:
    """
    Given a list of target territories, calculates the optimal attacking graph. Outputs the graph,
    the stack attacking from, and the sum of all troops on territories to attack
    """
    
    # Get all stacks with large enough size
    stacks = stackSelect(gameState, gameState.agentID)
    
    # Gets internal territories to remove from graph
    internalTerritories = findInternalTerritories(gameState.agentID, gameState)
    print("Internal territories")
    print(internalTerritories)
    
    # Stacks must be external to be used
    filteredStacks = stacks - set(internalTerritories)
    
    # Creates node weightings
    weightDict = {node : weightNode(node, gameState, territories) for node in gameState.map.graph.nodes()}
 
    # Creates new directed graph for msa prep
    directedGraph = nx.DiGraph(gameState.map.graph)
    
    # Removes all territories not to attack from 
    ownedToRemove = set(gameState.playerDict[gameState.agentID]["territories"]) - filteredStacks
    
    print("Owned to remove", ownedToRemove)
    directedGraph.remove_nodes_from(ownedToRemove)
    print("Graph nodes after remove")
    print(directedGraph.nodes())
    
    # Generates new weighted edges for graph. Weight is based on the desirablility 
    # to go to that territory. High troop low connection neutral territories are the least desirable. 
    for u, v in gameState.map.graph.edges():
        # Ensure that edge is in the connected graph! Inefficient operation 
        # style but should be negligible. 
        if u in directedGraph.nodes() and v in directedGraph.nodes():
            directedGraph.add_edge(u, v, weight=weightDict[v])
            directedGraph.add_edge(v, u, weight=weightDict[u])
        
        
    # Do special treatment of stack nodes afterwards    
    for stack in filteredStacks:
        # Remove all incoming edges to stack 
        # Convert in_edges to a list before removing to avoid interation errors
        edges_to_remove = list(directedGraph.in_edges(stack))
        directedGraph.remove_edges_from(edges_to_remove)
        
        # Add outward edges to neighbours in stack, ensuring it is not a new 
        # edge to another stack
        for neighbour in gameState.map.graph.neighbors(stack):
            if gameState.map.graph.nodes[neighbour]["player"] != gameState.agentID and neighbour in directedGraph.nodes():
                # They should only be in the direction away from the stack
                directedGraph.add_edge(stack, neighbour, weight=weightDict[neighbour] // 10)

    print("Graph nodes")
    print(directedGraph.nodes())
    print("Graph edges")
    print(directedGraph.edges())
    drawArborescence(gameState, directedGraph, 100)
    arborescence = nx.minimum_branching(directedGraph)
    print("Arborescence edges")
    print(arborescence.edges())
    drawArborescence(gameState, arborescence, 500)

    
    # In this iteration neutral nodes includes stacks which can be filtered out
    neutralNodes = set(arborescence.nodes()) - territories
    
    print("Neutral nodes")
    print(neutralNodes)
    drawArborescence(gameState, arborescence, 100)
    
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
                
    # Check how optimal the arborescence is
    minTroops = 0 
    
    for node in arborescence.nodes():
        minTroops += gameState.map.graph.nodes[node]["troops"]
        
    stacksUsed = {node for node in arborescence.nodes() if gameState.map.graph.nodes[node]["player"] == gameState.agentID}
                
    drawPath(gameState, arborescence, 200)
    return arborescence, stacksUsed, minTroops

