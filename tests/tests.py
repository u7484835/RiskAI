from maps.classic import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy as sp



bonus_color_map = {
        "NA": "blue",
        "SA": "red",
        "AF": "purple",
        "EU": "green",
        "AS": "orange",
        "AU": "yellow"
    }


background_image = mpimg.imread('/path/to/your/background/image.png')




# During regular games, this should be used to show the map of territories with the 
# node number being the troop amount, colour indicating player so that we can see
# the internal game state

def drawTest():
    ax = plt.subplot(111)
    node_colors = [bonus_color_map[Classic.nodes[node]["bonus"]] for node in Classic.nodes()]
    posConfig = nx.kamada_kawai_layout(Classic)
    ax.imshow(background_image, extent=[0, background_image.shape[1], 0, background_image.shape[0]])

    nx.draw(Classic, pos = new2ClassicPosCoords, with_labels=True, font_weight="bold", node_color=node_colors)
    plt.savefig("ClassicGraphTest.png")
    
    new2Coords = newClassicPosCoords
    for key in new2Coords.keys():
        new2Coords[key] = [new2Coords[key][0] - 260, new2Coords[key][1] - 230]
    print(new2Coords)
    
    
if __name__ == "__main__":
    drawTest()
    
