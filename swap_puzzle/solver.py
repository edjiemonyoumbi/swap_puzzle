from grid import Grid
import heapq
import math as maths
import pygame
import random

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
                
                S+=abs((i-posx[0]))+abs((j-posx[1]))
        return S
    

    #Implémentation de l'algorithme A*

    def astar(self):
        src=super().hashage()
        dst=super().grille_voulue()
        Dejavu={} #On crée un dictionnaire Dejavu dans lequel on attribuera aux noeuds(les clés) des valeurs booléennes (True) si on les a déjà visité
        Distance={src:0} #Dictionnaire qui compte les distances au noeud d'origine
        Parents={src:None} #Comme pour bfs, il faut crée un dictionnaire de parents qui nous permettra de remonter à la solution. 
        avisiter=[] #Nous allons créer une file de priorité à partir de cette liste avisiter
        
        heapq.heapify(avisiter) #On utilise alors le module heapq pour cela
        heapq.heappush(avisiter, (self.heuristique(), src)) #Et cette file de priorité sera basée sur la distance à l'origine et la valeur de l'heuristique pour aller à la grille ordonnée
        while len(avisiter)!=0: #On boucle sur le fait que la liste avisiter contienne encore des éléments, mais en réalité, on arrêtera cette boucle dès que l'on aura visité dst. 
            x=heapq.heappop(avisiter)[1] #On utilise heapq pour prendre l'élément qui minimise la valeur distance à l'origine+heuristique jusqu'à la grille ordonnée
            
            
            if x==dst:
                break
            
            if x in Dejavu: #On stoppe l'itération en cours si x a déjà été visité, afin de ne pas perdre en temps
                continue
            if x not in Distance.keys(): 
                Distance[x]=maths.inf #On fixe la valeur de distance à l'origine de base de tous les sommets à +inf

          
                    
            Dejavu[x]=True #On indique que le sommet a déjà été visité
            for y in Grid(self.m, self.n, self.de_hashage_a_grille(x)).voisins_de_la_grille(): #On parcourt tous les voisins de la grille 
                if y in Dejavu: #Si le voisin a déjà été visité, alors on peut éviter de perdre du temps en passant à l'itération suivante
                    continue
                if y not in Distance.keys(): 
                    Distance[y]=maths.inf
                
                

                        
                


                if Distance[x]+1<Distance[y]: #On construit le chemin le plus court de src à dst en faisant du proche en proche
                    Distance[y]=Distance[x]+1 #A* est un algorithme sur les graphs pondérés, mais ici la pondération vaut 1, car tous les voisins sont accessibles de la même manière (par un swap)
                    Parents[y]=x #On ajoute aux parents pour pouvoir ensuite remonter le chemin le pus court. 
                    if y not in Dejavu:
                        heapq.heappush(avisiter, (Solver(self.m, self.n, self.de_hashage_a_grille(y)).heuristique()+Distance[y], y)) #si y n'a pas encore été déjà visitée, on l'ajoute alors à la file de priorité de heapq
        #Mêmes explications que pour bfs_ameliore pour la suite 
        chemin=[dst]
        i=dst
        while i!=None:
            chemin.append(Parents[i])
            i=Parents[i]
        chemin.pop()   
        chemin.reverse()
        L=[]
        for i in range(len(chemin)-1):
            L.append(self.obtenir_le_swap(chemin[i], chemin[i+1]))
        return L
    
    def genere_grille(self): #Programme qui génère une grille aléatoirement, en utilisant le module random
        L=[i for i in range(1, self.m*self.n+1)]
        S=[]
        for i in range(len(L)):
            index=random.randint(0,len(L)-1) #On tire un index au hasard
            S.append(L[index]) #On ajoute l'élement donc l'index a été tiré
            del L[index] #Puis on le supprime de la liste, car tous les nombres n'apparaissent qu'une fois. 
        return self.de_liste_a_grid(S)

    #Interface graphique du jeu

    def jeu(self):
        pygame.init() #Initiation de Pygame
        fenetre = pygame.display.set_mode((1000,1000)) #Création de la fenêtre
        pygame.display.set_caption('Représentation graphique de la grille') #On donne un titre à la grille
        blanc = pygame.Color(255, 255, 255) #on code les couleurs noir, blanc, vert et bleu grâce au code rgb
        noir = pygame.Color(0,0,0)
        vert=pygame.Color(0,255,0)
        bleu=pygame.Color(0,0,255)
        jaune=pygame.Color(255,255,0)
        fenetre.fill(noir) #On remplit la couleur par un fond noir car on va représenter la grille par des cases blanches
        running=True #Nous utilisons running=True pour nous permettre de faire fonctionner les interfaces tant qu'on le souhaite, puis dès que l'on voudra changer d'interface, il suffira de mettre Running=False puis refaire une autre interface avec running=True
        font2=pygame.font.Font(None, 32) #Police d'écriture
        erreur = font2.render("Vous n'avez pas le droit d'échanger ces deux cases !", True, blanc)  #Message d'erreur 
        gagne=font2.render("Vous avez gagné !", True, blanc) #Message pour annoncer qu'on a gagné
        score=0 #Compteur qui compte le score de l'utilisateur
        solution=font2.render("Voir la meilleure solution", True, noir) #Meilleure solution
        selection = font2.render("Veuillez sélectionner le niveau de difficulté",True,blanc) #On va créer d'abord un menu de sélection de difficulté du jeu
        fenetre.blit(selection, (400, 200)) 
        facile = font2.render("FACILE",True,blanc) 
        
        moyen = font2.render("MOYEN",True,blanc) 
        
        difficile = font2.render("DIFFICILE",True,blanc) 
        


        L=[i for i in range(1, self.m*self.n+1)] 
        L.reverse() #On crée la pire grille possible, afin de calculer son heuristique, afin de pouvoir créer des grilles plus ou moins faciles
        grille=self.de_liste_a_grid(L)
        pire_solveuse=Solver(self.m, self.n, grille.state)
        pire_h=pire_solveuse.heuristique()
        while running: #Première interface pour sélectionner le niveau de difficulté
            fenetre.fill(noir)
            fenetre.blit(selection, (400, 200))
            pygame.draw.rect(fenetre, bleu, (400, 400, 300, 100)) 
            fenetre.blit(facile, (500, 450)) 
            pygame.draw.rect(fenetre, bleu, (400, 600, 300, 100)) 
            fenetre.blit(moyen, (500, 650)) 
            pygame.draw.rect(fenetre, bleu, (400, 800, 300, 100)) 
            fenetre.blit(difficile, (500, 850)) 
            pygame.display.update()
            for event in pygame.event.get(): #On attend un évenement de l'utilisateur, en l'occurence qu'il clique sur un des boutons de difficulté
                if event.type == pygame.QUIT:
                    pygame.quit()
                            
                        
                if event.type == pygame.MOUSEBUTTONDOWN: #S'il clique :
                    fenetre.fill(noir)
                    x, y = pygame.mouse.get_pos() #On obtient les coordonnées du clic, et grâce à ça et grâce aux coordonnées des boutons, on pourra savoir quel niveau de difficulté il a choisi
                    
                    if 400<=x<=700 and 400<=y<=500:
                        self.state=self.genere_grille().state
                        while self.heuristique()>(pire_h/3): #On a choisi de mettre le niveau de difficulté en trois parties : facile, moyen ou difficile, en fonction de la valeur de l'heuristique de la pire grille possible (ie la plus grande heuristique possible) donc on divise en trois intervalles égaux
                            self.state=self.state=self.genere_grille().state #On génère des grilles aléatoirement tant que le niveau de difficulté ne correspond pas à celui choisi par l'utilisateur
                        running=False #Si l'utilisateur a cliqué, alors on arrête cette interface pour passer à la prochaine, celle du jeu lui-même
                    if 400<=x<=700 and 600<=y<=700:
                        self.state=self.genere_grille().state
                        while self.heuristique()<(pire_h/3) or self.heuristique()>(pire_h*(2/3)):
                            self.state=self.state=self.genere_grille().state
                        running=False

                    if 400<=x<=700 and 800<=y<=900:
                        self.state=self.genere_grille().state
                        while self.heuristique()<(pire_h*(2/3)):
                            self.state=self.state=self.genere_grille().state
                        running=False
        
        running=True #On remet donc running à la valeur True, pour la nouvelle interface
        fenetre.fill(noir)
        pygame.display.update()



        meilleurscore=len(self.astar()) #Le meilleur score correspond au nombre de swaps que renvoie astar sur la grille
        grille_en_entree=copy.deepcopy(self.state) #On garde en mémoire la grille de départ, car on la modifie ensuite à chaque fois que l'utilisateur fait un swap.
        L=[] #Liste qui va collecter les coordonnées des clics pour faire les swaps
        while running:
            #On affiche la grille : 
            
            for i in range(self.m):
                for j in range(self.n):
                    font=pygame.font.Font(None, 32) #Police d'écriture
                    texte = font.render(str(self.state[i][j]),True,noir) #Texte à mettre dans les cases
                    pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50)) #On dessine les cases
                    fenetre.blit(texte, ((55*j)+20, 20+(55*i))) #On met le texte dans les cases

            
            
            
            if self.is_sorted()==True: #Si l'utilisateur a gagné
                
                fenetre.blit(gagne, (400, 350)) #On affiche qu'il a gagné
                
                
                
                scoretexte=font2.render("Voici votre score : "+str(score), True, blanc) 
                fenetre.blit(scoretexte, (400, 400)) #On affiche son score, ainsi que le meileur score
                
                

                meilleurscoretexte=font2.render("Voici quel était le meilleur score : "+str(meilleurscore), True, blanc)
                fenetre.blit(meilleurscoretexte, (400, 450))
                pygame.draw.rect(fenetre,vert,((400,500,300,100)))
                fenetre.blit(solution, (430, 530)) #On ajoute un bouton s'il veut voir la solution donnée par A*, qui s'effectuera toute seule
                pygame.display.update() #On met à jour le display
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                    
                    if event.type == pygame.MOUSEBUTTONDOWN: #S'il clique sur voir la solution : 
                        fenetre.fill(noir)
                        x, y = pygame.mouse.get_pos()
                        self.state=grille_en_entree #On repart de la grille de début et on la dessine : 

                        for i in range(self.m):
                                for j in range(self.n):
                                    font=pygame.font.Font(None, 32) #Police d'écriture
                                    texte = font.render(str(self.state[i][j]),True,noir) #Texte à mettre dans les cases
                                    pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50)) #On dessine les cases
                                    fenetre.blit(texte, ((55*j)+20, 20+(55*i))) #On met le texte dans les cases
                        pygame.display.update()
                        pygame.time.delay(1000)
                        #Puis on applique A* sur la grille, en mettant à jour le display entre chaque swap
                        if 400 <= x <= 700 and 500 <= y <= 600:
                            L=self.astar()
                            for el in L:
                                cell1=el[0]
                                cell2=el[1]
                                self.swap(cell1, cell2)
                                for i in range(self.m):
                                    for j in range(self.n):
                                        font=pygame.font.Font(None, 32) #Police d'écriture
                                        texte = font.render(str(self.state[i][j]),True,noir) #Texte à mettre dans les cases
                                        if (i==cell1[0] and j==cell1[1]) or (i==cell2[0] and j==cell2[1]):
                                            pygame.draw.rect(fenetre,jaune,((55*j),(55*i),50,50)) #On dessine les cases
                                        else:
                                            pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50)) #On dessine les cases
                                        fenetre.blit(texte, ((55*j)+20, 20+(55*i))) #On met le texte dans les cases
                                
                                pygame.display.update()
                                pygame.time.delay(2500) #On laisse un peu de temps entre chaque swap pour que l'utilisateur puisse bien voir la solution
                            pygame.quit()


                            
                
                                

                






                

                   
            #Tant qu'il n'a pas encore gagné, cette partie du code s'effectuera : 
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    ligne = y // 52 #On obtient le numéro de la ligne et de la colonne en divisant à peu près par la largeur des cases
                    colonne = x // 52
                    L.append((ligne, colonne)) #Puis on ajoute ainsi les coordonnées de la case sur la grille à L

            if len(L)==2: #Si l'utilisateur a cliqué sur deux cases : 
                i1=L[0][0]
                i2=L[1][0]
                j1=L[0][1]
                j2=L[1][1]
                if (i1==i2 and abs(j2-j1)==1) or (j1==j2 and abs(i2-i1)==1):
                    self.swap(L[0], L[1]) #On swap les deux cases
                    score+=1 #Et on ajoute 1 au score
                else:
                    
                    #Si le swap n'est pas valable, on ajoute un message d'erreur qui dure un certain temps, puis on redessine la grile telle qu'elle l'était avant. 
                    fenetre.blit(erreur, (200, 200)) #On met le texte dans les cases
                    pygame.display.update() #On met à jour le display
                    pygame.time.delay(2000)
                    fenetre.fill(noir)
                    for i in range(self.m):
                        for j in range(self.n):
                            font=pygame.font.Font(None, 32) #Police d'écriture
                            texte = font.render(str(self.state[i][j]),True,noir) #Texte à mettre dans les cases
                            pygame.draw.rect(fenetre,blanc,((55*j),(55*i),50,50)) #On dessine les cases
                            fenetre.blit(texte, ((55*j)+20, 20+(55*i))) #On met le texte dans les cases

            #La boucle while Running se remet en marche, donc on redessine la grille, avec le swap pris en compte s'il était valide


                    
                    



                L=[] #On vide la liste des boutons cliqués à 0, pour pouvoir de nouveau enreigistrer les clics de l'utilisateur
            


                    

        
    
                

        
            pygame.display.update() #On met à jour le display
        
        pygame.quit() #On quitte Pygame

    
    



        











        











        
        
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
        
