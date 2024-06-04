from maps.classic import *
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os



bonus_color_map = {
        "NA": "blue",
        "SA": "red",
        "AF": "purple",
        "EU": "green",
        "AS": "orange",
        "AU": "yellow"
    }


background_image_path = os.path.join('tests', 'BlankSlate12.png')
background_image = mpimg.imread(background_image_path)




# During regular games, this should be used to show the map of territories with the 
# node number being the troop amount, colour indicating player so that we can see
# the internal game state

def drawTest():
    ax = plt.subplot(111)
    node_colors = [bonus_color_map[Classic.nodes[node]["bonus"]] for node in Classic.nodes()]
    ax.imshow(background_image, extent=[0, background_image.shape[1], 0, background_image.shape[0]])

    nx.draw(Classic, pos = newClassicPosCoords, with_labels=True, font_weight="bold", node_color=node_colors)
    
    # Path to save the output image
    output_image_path = os.path.join('tests', 'drawTests9.png')

    # Save the figure with the custom background
    plt.savefig(output_image_path, bbox_inches='tight', transparent=True)
    
    
if __name__ == "__main__":
    drawTest()
    
