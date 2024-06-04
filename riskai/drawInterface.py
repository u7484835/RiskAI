from maps.classic import *
import networkx as nx
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
    
    ax = plt.subplot(111)
    
    # Gets list of colours
    playerNodes = [gameState.map.graph.nodes[node]["player"] for node in gameState.map.graph.nodes()]
    nodeColours = [gameState.playerDict[player]["colour"] for player in playerNodes]
    
    
    troopLabels = {node: data['troops'] for node, data in Classic.nodes(data=True)}
    
    # Makes background image the background of the plot
    ax.imshow(backgroundIm, extent=[0, backgroundIm.shape[1], 0, backgroundIm.shape[0]])

    # Draws nodes
    nx.draw(gameState.map.graph, pos = newClassicPosCoords, labels = troopLabels, with_labels=True, font_weight="bold", node_color=nodeColours)

    # Save the figure with the custom background
    outputImPath = os.path.join('riskAI', 'GameOutput.png')
    plt.savefig(outputImPath, bbox_inches='tight', transparent=True)
    
      
    # opens image for user
    os.system(f'start {outputImPath}')