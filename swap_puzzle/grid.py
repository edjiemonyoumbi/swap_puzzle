"""
This is the grid module. It contains the Grid class and its associated methods.
"""

import random
import matplotlib.pyplot as plt
import pygame 
from graph import Graph
import copy

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

    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorte and returns the answer as a boolean.
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        for i in range(self.m):
            for j in range(self.n-1):
                if self.state[i][j]!=self.state[i][j+1]-1:
                    return False
        return True

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        i1=cell1[0]
        i2=cell2[0]
        j1=cell1[1]
        j2=cell2[1]
        if (i1>=0 and i2>=0 and j1>=0 and j2>=0) and ((i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1)):
            c=self.state[i1][j1]
            self.state[i1][j1]=self.state[i2][j2]
            self.state[i2][j2]=c
        else:
            raise Exception ("The swap is not allowed.")

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
            self.swap(cell1, cell2)

    def representation(self):
        pygame.init()
        fenetre = pygame.display.set_mode((1000,1000))
        pygame.display.set_caption('Représentation graphique de la grille')
        blanc = pygame.Color(255, 255, 255)
        noir = pygame.Color(0,0,0)
        fenetre.fill(noir)
        
        for i in range(self.m):
            for j in range(self.n):
                font=pygame.font.Font(None, 32)
                texte = font.render(str(self.state[i][j]),True,noir)
                pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50))
                fenetre.blit(texte, ((55*j)+20, 20+(55*i)))
                

        
        pygame.display.update()
        
        pygame.quit()

    
    def hashage(self):
        grille=""
        for i in range(self.m):
            for j in range(self.n):
                grille+=str(self.state[i][j])
            grille+="/"
        return grille


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



#Question 7
    
def transforme_en_grille(l, m, n):
    sortie=[]
    compteur=0
    for i in range(m):
        k=[]
        for j in range(n):
            k.append(l[compteur])
            compteur+=1
        sortie.append(k)
    return sortie

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


