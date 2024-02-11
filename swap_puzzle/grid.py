"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random
import matplotlib.pyplot as plt
import pygame 
from graph import Graph
import copy

#Création de la classe Grid
class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """
    
    #Init de la classe Grid
    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

    #Permet d'imprimer la grille
    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    #Renvoie une représentation de la grille avec le nombre de ligne et de colonnes
    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    #Fonction qui permet de renvoyer True si la grille est bien triée, et False sinon
    def is_sorted(self):
        """
        Checks is the current state of the grid is sorte and returns the answer as a boolean.
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        for i in range(self.m):
            for j in range(self.n-1):
                if self.state[i][j]!=self.state[i][j+1]-1: #On compare l'élement de la boucle et le suivant en parcourant la grille ligne par ligne, afin de voir s'ils se suivent par une incrémentation de 1
                    return False
        return True

    #Implémentation de la fonction swap qui permet d'échanger deux cases de la grille, du moment qu'elles sont adjacentes
    #Question 2
    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        #On renomme les éléments des tuples pour pouvoir plus facilement les appeler ensuite dans la fonction
        i1=cell1[0]
        i2=cell2[0]
        j1=cell1[1]
        j2=cell2[1]
        if (i1>=0 and i2>=0 and j1>=0 and j2>=0) and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)): #Condition d'adjacence des cases pour pouvoir effectuer le swap
            c=self.state[i1][j1] #On stocke la valeur de la case dans une variable pour pouvoir ensuite la réutiliser pour échanger les valeurs
            self.state[i1][j1]=self.state[i2][j2]
            self.state[i2][j2]=c
        else:
            raise Exception ("The swap is not allowed.")

    #Implémentation d'une fonction qui permet d'effectuer une suite de swaps donnés en entrée
    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for el in cell_pair_list:
            cell1=el[0]
            cell2=el[1]
            self.swap(cell1, cell2) #On parcourt la liste des cases à échanger et on utilise la méthode swap implémentée auparavant 

    #Implémentation d'une méthode qui permet de représenter graphiquement la grille grâce à Pygame
    #Algorithme de la question 4
    def representation(self):
        pygame.init() #Initiation de Pygame
        fenetre = pygame.display.set_mode((1000,1000)) #Création de la fenêtre
        pygame.display.set_caption('Représentation graphique de la grille') #On donne un titre à la grille
        blanc = pygame.Color(255, 255, 255) #on code les couleurs noir et blanc grâce au code rgb
        noir = pygame.Color(0,0,0)
        fenetre.fill(noir) #On remplir la couleur par un fond noir car on va représenter la grille par des cases blanches
        
        for i in range(self.m):
            for j in range(self.n):
                font=pygame.font.Font(None, 32) #Police d'écriture
                texte = font.render(str(self.state[i][j]),True,noir) #Texte à mettre dans les cases
                pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50)) #On dessine les cases
                fenetre.blit(texte, ((55*j)+20, 20+(55*i))) #On met le texte dans les cases

    
                

        
        pygame.display.update() #On met à jour le display
        
        pygame.quit() #On quitte Pygame
    
    #Implémentation d'une fonction de hashage afin de rendre les grilles en objets qui puissent être utilisés pour les dictionnaires
    #Algorithme de la question 6
    def hashage(self):
        grille=""
        for i in range(self.m):
            for j in range(self.n):
                grille+=str(self.state[i][j])
            grille+="/" #Nous avons fait le choix de représenter les grilles par des chaînes de caractères, en utilisant des / pour indiquer les fins de ligne. EX : [[1, 2], [3, 4]] sera '12/34/'
        return grille
    
    #Implémentation d'une fonction pour transformer une liste Python en un objet de la classe Grid
    def de_liste_a_grid(self, l):
        sortie=[]
        compteur=0
        #On crée grâce à la boucle suivante un tableau à partir de la grille, en connaissant m et n
        for i in range(self.m):
            k=[]
            for j in range(self.n):
                k.append(l[compteur])
                compteur+=1
            sortie.append(k)
        return Grid(self.m, self.n, sortie) #On crée un objet Grid à partir de m, n et du tableau créé
    
    def permutations_possibles(self, E):
        #On construit toutes les permutations possibles des entiers de 1 à m*n puis on les transforme en grilles.
        #On procède pour cela par récursivité.
        
        if len(E)==1:
            return [[E[0]]] #Initiation de la récursivité : si la liste ne contient qu'un seul élément i, on renvoie [[i]]
        Lp = self.permutations_possibles(E[1:]) #On fait un appel récursif sur la liste à laquelle on a enlevé le premier élément
        L = [] #On crée une liste dans laquelle on va stocker toutes les permutations
        for x in Lp :
            for i in range(len(E)) : 
                L.append(x[:i]+[E[0]]+x[i:]) #On a utilisé un appel récursif, donc à la fin des appels récursifs, on se sera retrouvé dans le cas de l'initialisation, où Lp contient une liste de la forme [[e]], puis on case l'élement précédent avant ou après, cela donne une liste de deux permutations, à laquelle on va encore faire des permutations en ajoutant l'élément précédent dans ces listes, etc. Au final, on arrivera à des tailles de permutations de len(E), et en construisant au fur et à mesure par récursivité les permutations en augmentant leur taille et en casant à chaque fois les éléments dans tous les emplacments possibles, on aura obtenu la liste des permutations.  
        return L
    
    
    
    #Implémentation d'une fonction qui utilise la fonction permutations_possibles sur la grille qui nous intéresse: [1, 2, ..., m*n] afin d'obtenir toutes les grilles d'entiers de 1 à m*n possibles. 
    def grilles_possibles(self):
        
        L=self.permutations_possibles([i for i in range(1, self.m*self.n+1)]) #Appel de permutations_possibles
        sortie=[]
        for i in L:
            if self.de_liste_a_grid(i) not in sortie : 
                sortie.append(self.de_liste_a_grid(i)) #On transforme les permutations en objets Grid
        return sortie

    @staticmethod #On utilise une staticmethod qui prend en entrée deux objets de type Grid, et qui renvoie True si un swap permet de passer de l'une à l'autre et False sinon, afin de pouvoir construire les voisins de toutes les grilles. 
    def sont_liees_par_un_swap(g, h):
        l=[]
        for i in range(len(h.state)):
            
            for j in range(len(h.state[0])):
                if g.state[i][j]-h.state[i][j]!=0:
                    l.append((i, j)) 
                    if len(l)>2:
                        return False #On stocke dans une liste l les emplacements des éléments différents entre les deux grilles, mais on renvoie false si le nombre de différences est strictement supérieur à 2, car cela indique qu'il ne serait pas possible de passer de l'une à l'autre par un swap. 
        
        if len(l)==2: #Il nous faut que le nombre de différences soit exactement égal à 2
            i1=l[0][0]
            i2=l[1][0]
            j1=l[0][1]
            j2=l[1][1] #On utilise des noms pour leurs indices pour pouvoir plus facilement les appeler.
            if ((g.state[i1][j1]-h.state[i1][j1])==-(g.state[i2][j2]-h.state[i2][j2])) and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)): #Si la différence des éléments de l'emplacement 1 est égal à la différence des ééments de l'emplacement 2 et les emplacements des différences sont adjacents verticalement ou horizontalement
                return True #Alors, on a bien un swap qui permet de passer de l'une à l'autre
        return False #Sinon, il n'est pas possible, donc on renvoie False. 

        
    
    #On implémente un algorithme qui vient calculer le graph des sommets en prenant la taille de la grille qu'on a entrée. 
    def graph_des_sommets(self):
        dico={} #On stocke le graph dans un dictionnaire
        l=self.grilles_possibles() 
        
        for k in l:
            dico[k.hashage()]=[] #On construit toutes les clés du dictionnaire en prenant toutes les grilles possibles comme clés. 
        
        

        for i in l:
            for j in l:
                if self.sont_liees_par_un_swap(i, j)==True:
                    dico[i.hashage()].append(j.hashage()) #Pour chaque clé, on ajoute dans ses valeurs toutes ses voisines parmi toutes les grilles possibles, si elles sont bien liées par un swap. 
          
                
        return dico

    #On crée une fonction qui renvoie, sous forme hashable, la grille souhaitée, qui est celles des entiers ordonnés par ordre croissant. 
    def grille_voulue(self):
        l=[i for i in range(1, self.m*self.n+1)]
        l=self.de_liste_a_grid(l)
        return l.hashage()

    #Algorithme de la question 7
    def bfs_sur_grilles(self):
        dico=Graph(list(self.graph_des_sommets().keys())) #On crée un objet de type graph, en initialisant ses nodes à partir de tous les noeuds du graph des grilles possibles. 
        for i in dico.nodes:
            for j in self.graph_des_sommets()[i]:
                dico.add_edge(i, j) #On ajoute les add_edge entre les grilles et leurs voisines. On a ainsi construit un objet de type Graph qui contient le graph de toutes les grilles possibles, et leurs voisines par un swap. 
        
        return dico.bfs(self.hashage(), self.grille_voulue()) #On peut maintenant grâce à cela utiliser l'algorithme bfs précédemment construit dans la classe Graph, afin de résoudre le swap puzzle. 
    
    #La longueur du chemin renvoyé est bien plus faible que dans la méthode naïve : la méthode naïve n'était donc bien pas optimale en terme de nombre de swaps à effectuer pour atteindre la grille ordonnée. Cependant, la méthode naïve est plus rapide.
    #Nombre de noeuds : Il est égal au nombre de permutations de la liste des entiers de 1 à m*n, donc il y en a (m*n)!
    #Nombre d'arêtes : On regarde les add_edge dans l'algo : (n*m)!*(m*(n−1)+n*(m−1)), car il y a (m*n)! noeuds, et m*(n−1)+n*(m−1) voisins par un swap pour chaque noeud, car il y a m*(n-1) swaps horizontaux, et n*(m-1) swaps verticaux. 
    #Complexité de l'algo : La complexité du bfs est de O(nbre d'arêtes+nbre de sommets) donc ici de O((n*m)!*(m×(n−1)+n×(m−1))+1)=O((m*n)!(2m*n-m-n+1))

    #Question 8 
    def voisins_de_la_grille(self): #On crée un algorithme qui construit toutes les grilles voisines d'une grille par un swap, au lieu de les chercher parmi toutes les grilles possibles comme précédemment. 
        L=[]
        
        for i in range(self.m-1): #Swaps en excluant la dernière colonne et la dernière ligne
            for j in range(self.n-1):
                self.swap((i, j), (i+1, j))
                k=copy.deepcopy(self.state) #Il faut utiliser une deep copy, sinon la valeur de k est modifiée quand on modifie self.state
                L.append(k)
                
            
                self.swap((i, j), (i+1, j))
                self.swap((i, j), (i, j+1))
                k=copy.deepcopy(self.state)
                L.append(k)
                
                
                self.swap((i, j), (i, j+1))
                
        for j in range(self.n-1): #Swaps sur la dernière ligne
            self.swap((self.m-1, j), (self.m-1, j+1))
            k=copy.deepcopy(self.state)
            L.append(k)
            
            self.swap((self.m-1, j), (self.m-1, j+1))
            
        for i in range(self.m-1): #Swaps sur la dernière colonne
            self.swap((i, self.n-1), (i+1, self.n-1))
            k=copy.deepcopy(self.state)
            L.append(k)
            
            self.swap((i, self.n-1), (i+1, self.n-1))
        H=[]
        for y in L:
            k=Grid(self.m, self.n, y).hashage()
            H.append(k)
            
        return H
     


    @staticmethod #On utilise une staticmethod car cette fonction prend en entrée un objet de type string et non une grille, et qui permet de le transformer en tableau. 
    def de_hashage_a_grille(grille):

        l=[]
        k=[]
        
        for i in grille:
            if i=='/':
                l.append(k)
                

                k=[]
                
            else:
                k.append(int(i))
                
        return l
        


    #Algorithme de la question 8
    #On reprend l'algorithme de la classe Graph, en le modifiant pour qu'il construise les voisins au fur et à mesure, afin de ne pas conserver tout le graph en mémoire, mais le construire au fur et à mesure qu'on le parcourt. 
    def bfs_ameliore(self) :
        src=self.hashage()
        dst=self.grille_voulue()
        dico={src:self.voisins_de_la_grille()} #On initialise le dictionnaire qu'on parcourt avec uniquement la grille en entrée et ses voisins au départ. 
        
        if src == dst:
            return [src]
        
        parents={src:None} #On initialise le dictionnaire des parents.

        file = [src]
        noeuds_visites = [src]
            
        while len(file) != 0 :
            sommet = file.pop(0)
                
            if sommet==dst:
                break
           
            for v in Grid(self.m, self.n, self.de_hashage_a_grille(sommet)).voisins_de_la_grille() : #C'est ici que la différence apparaît : on regarde pour chaque sommet qu'on parcourt ses voisins au fur et à mesure, au lieu de stocker le graph en mémoire. La fin de l'algorithme est similaire à celui de Graph. 
                if v not in noeuds_visites:
                    file.append(v) 
                    noeuds_visites.append(v)
                    parents[v]=sommet
                    
                    
                    
                    
            
        if dst not in noeuds_visites: 
            return None
            
        chemin=[dst]
        i=dst
        while i!=None:
            chemin.append(parents[i])
            i=parents[i]
        chemin.pop()   
        chemin.reverse()
        return chemin



    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid





    