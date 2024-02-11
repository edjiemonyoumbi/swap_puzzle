#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 17:16:52 2024

@author: aroldtoubert
"""

"""
This is the graph module. It contains a minimalistic Graph class.
"""



class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes 
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))
        

 
    #Algorithme de la question 5
    def bfs(self, src, dst) :
        
        #si la grille est déjà la grille voulue, on renvoie elle même :
        if src == dst:
            return [src]
        
        #On initialise un dictionnaire de parents, qui va nous permettre de remonter grâce aux parents à la solution. 
        parents={src:None}

        #On crée une file de noeuds à visiter et une liste avec les noeuds visités. 
        file = [src]
        noeuds_visites = [src]
        
        
        while len(file) != 0 : #On continue de parcourir tant que la file de noeuds à visiter contient encore des neouds. 
            sommet = file.pop(0) #On enlève le premier élément de la file, et on le retient en mémoire dans sommet
            
            if sommet==dst: #Si sommet est bien égal au noeud qu'on souhaite, alors on n'a plus besoin de continuer à parcourir le graph, donc on stoppe la boucle. 
                break

            for v in self.graph[sommet] : #On regarde parmi tous les voisins du sommet auquel on se situe ...
                if v not in noeuds_visites: #ceux que l'on n'a pas encore visités 
                   file.append(v) # on rajoute tous les voisins pas encore vus dans la file
                   noeuds_visites.append(v) #On les ajoute aux noeuds visités pour ne pas avoir à les réintégrer dans les parents
                   parents[v]=sommet #Et on met dans le dictionnaire des parents leurs parents qui est donc sommet. Cela permettra ensuite, en partant de dst, et en parcourant le dictionnaire des parents, d'arriver de voisin en voisin à la grille d'origine. Il ne nous restera alors plus qu'à inverser la liste des noeuds parcourus pour obtenir le chemin obtenu par bfs pour aller de src à dst. 
                   
                
        
        if dst not in noeuds_visites: 
            return None #Si nous n'avons pas vu le noeud que l'on voulait en parcourant le graph, alors il n'y a pas de chemin possible pour aller de src à dst, donc on renvoie None. 
        
        chemin=[dst]
        i=dst
        while i!=None: #On avait mis comme valeur à src dans parents la valeur None exprès pour pouvoir savoir quand arrêter la liste
            chemin.append(parents[i])
            i=parents[i] #On parcourt le chemin inverse en partant de l'arrivée dst puis en parcourant de parent en parent jusqu'à arriver à src.
        chemin.pop()   #On enlève le None de la liste du chemin
        chemin.reverse() #On l'inverse afin d'avoir le chemin de src à dst et non l'inverse
        return chemin

        #Nous pouvons vérifier que cet algorithme fonctionne sur graph1.in et graph2.in en comparant avec graph1.path.out et graph2.path.out. Pour cela, on crée graphique=Graph.graph_from_file("/Users/aroldtoubert/projet_programmation/input/graph1.in") et on applique bfs en mettant demandant graphique.bfs(src, dst).

    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph

