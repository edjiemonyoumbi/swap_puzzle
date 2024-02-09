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
    def hashage(self):
        grille=""
        for i in range(self.m):
            for j in range(self.n):
                grille+=str(self.state[i][j])
            grille+="/" #Nous avons fait le choix de représenter les grilles par des chaînes de caractères, en utilisant des / pour indiquer les fins de ligne
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
        #On construit toutes les permutations possibles des entiers de 1 à m*n puis on les transforme en grilles
        
        if len(E)==1:
            return [[E[0]]]
        Lp = self.permutations_possibles(E[1:]) 
        L = []
        for x in Lp :
            for i in range(len(E)) : 
                L.append(x[:i]+[E[0]]+x[i:])
        return L
    
    
    

    def grilles_possibles(self):
        
        L=self.permutations_possibles([i for i in range(1, self.m*self.n+1)])
        sortie=[]
        for i in L:
            if self.de_liste_a_grid(i) not in sortie : 
                sortie.append(self.de_liste_a_grid(i))
        return sortie

    @staticmethod
    def sont_liees_par_un_swap(g, h):
        l=[]
        for i in range(len(h.state)):
            
            for j in range(len(h.state[0])):
                if g.state[i][j]-h.state[i][j]!=0:
                    l.append((i, j))
                    if len(l)>2:
                        return False
        
        if len(l)==2:
            i1=l[0][0]
            i2=l[1][0]
            j1=l[0][1]
            j2=l[1][1]
            if ((g.state[i1][j1]-h.state[i1][j1])==-(g.state[i2][j2]-h.state[i2][j2])) and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)):
                return True
        return False

        
    

    def graph_des_sommets(self):
        dico={}
        l=self.grilles_possibles()
        
        for k in l:
            dico[k.hashage()]=[]
        
        

        for i in l:
            for j in l:
                if self.sont_liees_par_un_swap(i, j)==True:
                    dico[i.hashage()].append(j.hashage())
          
                
        return dico

    def grille_voulue(self):
        l=[i for i in range(1, self.m*self.n+1)]
        l=self.de_liste_a_grid(l)
        return l.hashage()

    def bfs_sur_grilles(self):
        dico=Graph(list(self.graph_des_sommets().keys()))
        for i in dico.nodes:
            for j in self.graph_des_sommets()[i]:
                dico.add_edge(i, j)
        
        return dico.bfs(self.hashage(), self.grille_voulue())

    def voisins_de_la_grille(self):
        L=[]
        
        for i in range(self.m-1):
            for j in range(self.n-1):
                self.swap((i, j), (i+1, j))
                k=copy.deepcopy(self.state)
                L.append(k)
                
            
                self.swap((i, j), (i+1, j))
                self.swap((i, j), (i, j+1))
                k=copy.deepcopy(self.state)
                L.append(k)
                
                
                self.swap((i, j), (i, j+1))
                
        for j in range(self.n-1):
            self.swap((self.m-1, j), (self.m-1, j+1))
            k=copy.deepcopy(self.state)
            L.append(k)
            
            self.swap((self.m-1, j), (self.m-1, j+1))
            
        for i in range(self.m-1):
            self.swap((i, self.n-1), (i+1, self.n-1))
            k=copy.deepcopy(self.state)
            L.append(k)
            
            self.swap((i, self.n-1), (i+1, self.n-1))
        H=[]
        for y in L:
            k=Grid(self.m, self.n, y).hashage()
            H.append(k)
            
        return H
            
    @staticmethod
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
        



    def bfs_ameliore(self) :
        src=self.hashage()
        dst=self.grille_voulue()
        dico={src:self.voisins_de_la_grille()}
        
        if src == dst:
            return [src]
        parents={src:None}

        file = [src]
        noeuds_visites = [src]
            
        while len(file) != 0 :
            sommet = file.pop(0)
                
            if sommet==dst:
                break
           
            for v in Grid(self.m, self.n, self.de_hashage_a_grille(sommet)).voisins_de_la_grille() :
                if v not in noeuds_visites:
                    file.append(v) # on rajoute tous les voisins pas encore vus dans la file
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


"""
#Question 7
    


def permutations_possibles(E):
    #On construit toutes les permutations possibles des entiers de 1 à m*n puis on les transforme en grilles

    if len(E)==1:
        return [[e] for e in E]
    Lp = permutations_possibles(E[1:]) 
    L = []
    for x in Lp :
        for i in range(len(E)) : 
            L.append(x[:i]+[E[0]]+x[i:])
    return L

def grilles_possibles(m, n):
    E=[i for i in range(1, m*n+1)]
    L=permutations_possibles(E)
    sortie=[]
    for i in L:
        if transforme_en_grille(i, m, n) not in sortie : 
            sortie.append(transforme_en_grille(i, m, n))
    return sortie

def sont_liees_par_un_swap(g, h):
    
    
    l=[]
    for i in range(len(h)):
        
        for j in range(len(h[0])):
            if g[i][j]-h[i][j]!=0:
                l.append((i, j))
                if len(l)>2:
                    return False
    
    if len(l)==2:
        i1=l[0][0]
        i2=l[1][0]
        j1=l[0][1]
        j2=l[1][1]
        if ((g[i1][j1]-h[i1][j1])==-(g[i2][j2]-h[i2][j2])) and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)):
            return True
    return False

        
def hashag(g, m, n):
    grille=""
    for i in range(m):
        for j in range(n):
            grille+=str(g[i][j])
        grille+="/"
    return grille

def graph_des_sommets(m, n):
    dico={}
    l=grilles_possibles(m, n)
    
    for i in range(len(l)):
        dico[hashag(l[i], m, n)]=[]
        
        

    for i in l:
        for j in l:
            if sont_liees_par_un_swap(i, j)==True:
                dico[hashag(i, m, n)].append(hashag(j, m, n))
          
                
    return dico

def grille_voulue(m, n):
    l=[i for i in range(1, m*n+1)]
    l=transforme_en_grille(l, m, n)
    return hashag(l, m, n)

def bfs_sur_grilles(m, n, depart):
    dico=Graph(list(graph_des_sommets(m, n).keys()))
    for i in dico.nodes:
        for j in graph_des_sommets(m, n)[i]:
            dico.add_edge(i, j)
    
    return dico.bfs(depart, grille_voulue(m, n))

def voisins_de_la_grille(grille):
    L=[]
    m=len(grille)
    n=len(grille[0])
    grille=Grid(m, n, grille)
    for i in range(m-1):
        for j in range(n-1):
            grille.swap((i, j), (i+1, j))
            k=copy.deepcopy(grille.state)
            L.append(k)
            
        
            grille.swap((i, j), (i+1, j))
            grille.swap((i, j), (i, j+1))
            k=copy.deepcopy(grille.state)
            L.append(k)
            
            
            grille.swap((i, j), (i, j+1))
            
    for j in range(n-1):
        grille.swap((m-1, j), (m-1, j+1))
        k=copy.deepcopy(grille.state)
        L.append(k)
        
        grille.swap((m-1, j), (m-1, j+1))
        
    for i in range(m-1):
        grille.swap((i, n-1), (i+1, n-1))
        k=copy.deepcopy(grille.state)
        L.append(k)
        
        grille.swap((i, n-1), (i+1, n-1))
    H=[]
    for i in L:
        H.append(hashag(i, m, n) )
        
    return H
            

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
        



def bfs_ameliore(grille, src, dst) :
    dico={src:voisins_de_la_grille(grille)}
    
    if src == dst:
        return [src]
    parents={src:None}

    file = [src]
    noeuds_visites = [src]
        
    while len(file) != 0 :
        sommet = file.pop(0)
            
        if sommet==dst:
            break
        for v in voisins_de_la_grille(de_hashage_a_grille(sommet)) :
            if v not in noeuds_visites:
                file.append(v) # on rajoute tous les voisins pas encore vus dans la file
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


"""


    