import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import os
from maps.classic import *
from riskAI.simpleAI import *

def arborescenceTest():
    seed = 13648  # Seed random number generators for reproducibility
    orig = nx.random_k_out_graph(10, 30, 2, seed=seed)
    G = nx.minimum_spanning_arborescence(orig)
    pos = nx.spring_layout(G, seed=seed)

    node_sizes = [3 + 10 * i for i in range(len(G))]
    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    cmap = plt.cm.plasma

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="indigo")
    edges = nx.draw_networkx_edges(
        G,
        pos,
        node_size=node_sizes,
        arrowstyle="->",
        arrowsize=10,
        edge_color=edge_colors,
        edge_cmap=cmap,
        width=2,
    )
    # set alpha value for each edge
    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])

    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)

    ax = plt.gca()
    ax.set_axis_off()
    plt.colorbar(pc, ax=ax)

    # Path to save the output image
    output_image_path = os.path.join('tests', 'branching.png')

    # Save the figure with the custom background
    plt.savefig(output_image_path, bbox_inches='tight', transparent=True)


    
if __name__ == "__main__":
    arborescenceTest()
    