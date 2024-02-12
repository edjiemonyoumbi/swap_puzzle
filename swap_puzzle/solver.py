from grid import Grid
import heapq
import math as maths

class Solver(Grid): #On fait un héritage pour utiliser les fonctions de la classe Grid, comme swap
    
    """
    A solver class, to be implemented.
    """
    #Implémentation d'un algo qui permet d'accéder à la position d'un élément k dans la grille. 
    def position(self, k):
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j]==k:
                    return (i, j)
    
    #Implémentation d'une fonction qui permet de renvoyer la position à laquelle doit aller l'élément k pour que la grille soit ordonnée. 
    def position_voulue(self, k):
        k=int(k)
        compteur=1
        for i in range(self.m):
            for j in range(self.n):
                if compteur==k:
                    return (i, j)
                compteur+=1

    def heuristique(self):
        S=0
        for i in range(self.m):
            for j in range(self.n):
                x=self.state[i][j]
                
                posx=self.position_voulue(x)
                
                S+=abs(((i-posx[0]))+abs((j-posx[1])))//2
        return S
    
    def astar(self):
        
        src=super().hashage()
        dst=super().grille_voulue()
        avisiter=[]
        heapq.heappush(avisiter, (0, src))
        coutsdepart={src : 0}
        coutsarrivee={src:self.heuristique()}
        parents={src:None}
        while len(avisiter)!=0:
            sommet=heapq.heappop(avisiter)[1]
            if sommet==dst:
                break
            for voisin in Grid(self.m, self.n, self.de_hashage_a_grille(sommet)).voisins_de_la_grille():
                d=1
                if voisin not in coutsdepart.keys() and voisin not in coutsarrivee.keys() : 
                    coutsarrivee[voisin]=maths.inf
                    coutsdepart[voisin]=maths.inf

                if coutsdepart[sommet]+d<coutsdepart[voisin]:
                    parents[voisin]=sommet
                    coutsdepart[voisin]=coutsdepart[sommet]+d
                    coutsarrivee[voisin]=coutsdepart[sommet]+d+Solver(self.m, self.n, self.de_hashage_a_grille(voisin)).heuristique()
                    if (coutsarrivee[voisin], voisin) not in avisiter:
                        heapq.heappush(avisiter, (coutsarrivee[voisin], voisin))
        chemin=[dst]
        i=dst
        while i!=None:
            chemin.append(parents[i])
            i=parents[i]
        chemin.pop()   
        chemin.reverse()
        return chemin











        
        
    #Algorithme de la question 3
    def get_solution(self):
        L=[]
        for i in range(1, (self.m)*(self.n)+1): #On fait une boucle sur tous les éléments de la grille : on va d'abord ranger 1, puis 2, etc...
            pos=self.position(i)
           
            posv=self.position_voulue(i)
            #On met l'élément à sa bonne colonne : on swap donc vers la droite s'il est trop à gauche et vers la gauche s'il est trop à droite
            if pos[1]>posv[1]:
                while pos[1]>posv[1]:
                    super().swap(pos, (pos[0], pos[1]-1))
                    L.append((pos, (pos[0], pos[1]-1)))
                    pos=(pos[0], pos[1]-1)

            if pos[1]<posv[1]:
                while pos[1]<posv[1]:
                    super().swap(pos, (pos[0], pos[1]+1))
                    L.append((pos, (pos[0], pos[1]+1)))
                    pos=(pos[0], pos[1]+1)
            #Puis une fois qu'il est dans la bonne colonne, on le remonte jusqu'à sa bonne ligne. Notons qu'il est impossible de devoir descendre un élément, car on range d'abord 1, puis 2, puis 3 etc donc tous les éléments du haut sont déjà bien placés. 
            while pos[0]>posv[0]:
                super().swap(pos, (pos[0]-1, pos[1]))
                L.append((pos, (pos[0]-1, pos[1])))
                pos=(pos[0]-1, pos[1])
        
        return L

        #La complexité de cet algorithme est de O((n*m)**2).
        #En terme de nombre de swaps, il est de 0 dans le meilleur des cas, et dans le pire cas (grille complètement inversée) de (m*n)*(m+n-2)/2, car il y a (m*n) éléments dans la grille, et ils font en moyenne (m+n-2)/2 swaps pour arriver dans leur position voulue. La longueur de chemin parcourue n'est donc pas optimale. 
        #Toute grille peut être résolue par cet algorithme naïf. 
        
