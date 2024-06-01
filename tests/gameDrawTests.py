from maps.classic import *
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp



bonus_color_map = {
        "NA": "blue",
        "SA": "red",
        "AF": "purple",
        "EU": "green",
        "AS": "orange",
        "AU": "yellow"
    }


# During regular games, this should be used to show the map of territories with the 
# node number being the troop amount, colour indicating player so that we can see
# the internal game state

def drawTest():
    ax = plt.subplot(111)
    node_colors = [gameState.playerDict[Classic.nodes[node]["player"]]["colour"] for node in Classic.nodes()]
    node_labels = [bonus_color_map[Classic.nodes[node]["troops"]] for node in Classic.nodes()]
    posConfig = nx.kamada_kawai_layout(Classic)
    nx.draw(Classic, pos = classicPosCoords, with_labels=True, font_weight="bold", node_color=node_colors)
    plt.savefig("ClassicGraphTest.png")

    
    
if __name__ == "__main__":
    drawTest()
    
