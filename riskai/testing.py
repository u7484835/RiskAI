from maps import *
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp



bonus_color_map = {
        'NA': 'blue',
        'SA': 'red',
        'AF': 'purple',
        'EU': 'green',
        'AS': 'orange',
        'AU': 'yellow'
    }

def drawTest():
    ax = plt.subplot(111)
    node_colors = [bonus_color_map[Classic.nodes[node]['bonus']] for node in Classic.nodes()]
    posConfig = nx.kamada_kawai_layout(Classic)
    nx.draw(Classic, pos = posConfig, with_labels=True, font_weight='bold', node_color=node_colors)
    plt.savefig('ClassicGraphTest.png')

    
    
if __name__ == '__main__':
    drawTest()
    
