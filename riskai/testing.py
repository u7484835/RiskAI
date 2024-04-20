from maps import *
import networkx as nx
import matplotlib.pyplot as plt




def drawTest():
    ax = plt.subplot(111)
    nx.draw(Classic, with_labels=True, font_weight='bold')
    plt.savefig('ClassicGraphTest.png')

    
    
if __name__ == '__main__':
    drawTest()
    
