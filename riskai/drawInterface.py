from maps.classic import *
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from .structures import GameState




# During regular games, this should be used to show the map of territories with the 
# node number being the troop amount, colour indicating player so that we can see
# the internal game state
def drawBoard(gameState : GameState):
    # Gets background image
    backgroundPath = os.path.join('tests', 'BlankSlate12.png')
    backgroundIm = mpimg.imread(backgroundPath)
    
    plt.figure(figsize=(10, 7.5), dpi=300)
    ax = plt.subplot(111)
    
    # Gets list of colours
    playerNodes = [gameState.map.graph.nodes[node]["player"] for node in gameState.map.graph.nodes()]
    nodeColours = [gameState.playerDict[player]["colour"] for player in playerNodes]
    
    # Changes black to grey for visibility
    nodeColours = ["grey" if c == "black" else c for c in nodeColours]
    
    
    
    troopLabels = {node: data['troops'] for node, data in Classic.nodes(data=True)}
    
    # Makes background image the background of the plot
    ax.imshow(backgroundIm, extent=[0, backgroundIm.shape[1], 0, backgroundIm.shape[0]])

    # Draws nodes
    nx.draw(gameState.map.graph, pos = newClassicPosCoords, labels = troopLabels, with_labels=True, font_weight="bold", node_color=nodeColours)

    # Save the figure with the custom background
    outputImPath = os.path.join('riskAI', 'GameOutput.png')
    plt.savefig(outputImPath, bbox_inches='tight', transparent=True)
    
    # Close the current figure to prevent blocking
    plt.close()



def drawArborescence(gameState : GameState, arbGraph : nx.Graph, stack : int):
    """
    Draws the arborescence, adds stack name for identification
    """
    # Gets background image
    backgroundPath = os.path.join('tests', 'BlankSlate12.png')
    backgroundIm = mpimg.imread(backgroundPath)
    
    plt.figure(figsize=(10, 7.5), dpi=300)
    ax = plt.subplot(111)    
    
    # Gets list of colours
    playerNodes = [gameState.map.graph.nodes[node]["player"] for node in arbGraph.nodes()]
    nodeColours = [gameState.playerDict[player]["colour"] for player in playerNodes]
    
    # Changes black to grey for visibility
    nodeColours = ["grey" if c == "black" else c for c in nodeColours]
    
    troopLabels = {node: gameState.map.graph.nodes[node]["troops"]  for node in arbGraph.nodes()}
    
    # Makes background image the background of the plot
    ax.imshow(backgroundIm, extent=[0, backgroundIm.shape[1], 0, backgroundIm.shape[0]])
    
    # Gets filtered pos dict
    filtPos = {key: newClassicPosCoords[key] for key in arbGraph.nodes if key in newClassicPosCoords}

    nx.draw_networkx(arbGraph, filtPos, labels = troopLabels, with_labels=True, font_weight="bold", node_size = 300, node_color=nodeColours, arrowstyle="->", arrowsize=10, width=2, edge_color = 'r')
    """nodes = nx.draw_networkx_nodes(arbGraph, filtPos, labels = troopLabels, with_labels=True, font_weight="bold", node_color=nodeColours)
    edges = nx.draw_networkx_edges(
        arbGraph,
        filtPos,
        arrowstyle="->",
        arrowsize=10,
        width=2,
    )"""
    
    name = f'arborescence{stack}.png'

    # Save the figure with the custom background
    outputImPath = os.path.join('riskai', name)
    plt.savefig(outputImPath, bbox_inches='tight', transparent=True)
    
    # Close the current figure to prevent blocking
    plt.close()



def drawPath(gameState : GameState, arbGraph : nx.Graph, stack : int):
    """
    Draws the arborescence, adds stack name for identification
    """
    # Gets background image
    backgroundPath = os.path.join('tests', 'BlankSlate12.png')
    backgroundIm = mpimg.imread(backgroundPath)
    
    plt.figure(figsize=(10, 7.5), dpi=300)
    ax = plt.subplot(111)    
    
    # Gets list of colours
    playerNodes = [gameState.map.graph.nodes[node]["player"] for node in arbGraph.nodes()]
    nodeColours = [gameState.playerDict[player]["colour"] for player in playerNodes]
    
    # Changes black to grey for visibility
    nodeColours = ["grey" if c == "black" else c for c in nodeColours]
    
    troopLabels = {node: gameState.map.graph.nodes[node]["troops"]  for node in arbGraph.nodes()}
    
    # Makes background image the background of the plot
    ax.imshow(backgroundIm, extent=[0, backgroundIm.shape[1], 0, backgroundIm.shape[0]])
    
    # Gets filtered pos dict
    filtPos = {key: newClassicPosCoords[key] for key in arbGraph.nodes if key in newClassicPosCoords}
    
    troopLabelsFull = {node: data['troops'] for node, data in Classic.nodes(data=True)}
    nx.draw(gameState.map.graph, pos = newClassicPosCoords, labels = troopLabelsFull, with_labels=True, font_weight="bold", node_color='grey')
    nx.draw_networkx(arbGraph, filtPos, labels = troopLabels, with_labels=True, font_weight="bold", node_size = 300, node_color=nodeColours, arrowstyle="->", arrowsize=10, width=2, edge_color = 'r')

    
    name = f'arborescence{stack}.png'

    # Save the figure with the custom background
    outputImPath = os.path.join('riskai', name)
    plt.savefig(outputImPath, bbox_inches='tight', transparent=True)
    
    # Close the current figure to prevent blocking
    plt.close()
