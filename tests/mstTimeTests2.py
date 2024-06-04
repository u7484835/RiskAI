import time
import random


# During regular games, this should be used to show the map of territories with the 
# node number being the troop amount, colour indicating player so that we can see
# the internal game state

def main():


    print("Importing packages")
    start_import = time.time()
    from maps.classic import Classic
    import networkx as nx
    from riskAI.interface import setupGameState
    import scipy as sp
    import os
    print("Done. That took", time.time() - start_import, "seconds.")
    
    testGS = setupGameState()
    
    graphList = []
    
    print("Testing MST time ")
    start_mst = time.time()
    for i in range(1000):    
        currGraph = testGS.map.graph.copy()
        for node in currGraph:
            currGraph.nodes[node]['troops'] = random.randint(1, 100)
        mst = nx.minimum_spanning_tree(currGraph, weight='troops', algorithm='kruskal')
        graphList.append((currGraph, mst))
    print("Done. That took", time.time() - start_mst, "seconds.")
    
    print(graphList[-1][0].nodes())
    
    
    
if __name__ == "__main__":
    main()
    
