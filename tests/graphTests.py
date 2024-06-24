from maps.classic import *
import networkx as nx



def graphTest():
    classicGraph = Classic
    diClassic = nx.MultiDiGraph(classicGraph)
    
    print("Nodes of graph: ")
    
    for node in diClassic.nodes():
        print(node)
        
    print("Edges of graph: ")    
        
    for edge in diClassic.edges():
        print(edge)
    
    
if __name__ == "__main__":
    graphTest()
    
