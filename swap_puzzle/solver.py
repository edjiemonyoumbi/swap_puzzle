from grid import Grid

class Solver(Grid): 
    
    """
    A solver class, to be implemented.
    """
    def position(self, k):
        for i in range(self.m):
            for j in range(self.n):
                if self.state[i][j]==k:
                    return (i, j)
    
    def position_voulue(self, k):
        k=int(k)
        compteur=1
        for i in range(self.m):
            for j in range(self.n):
                if compteur==k:
                    return (i, j)
                compteur+=1
        

    def get_solution(self):
        L=[]
        for i in range(1, (self.m)*(self.n)+1):
            pos=self.position(i)
           
            posv=self.position_voulue(i)
            
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
            
            while pos[0]>posv[0]:
                super().swap(pos, (pos[0]-1, pos[1]))
                L.append((pos, (pos[0]-1, pos[1])))
                pos=(pos[0]-1, pos[1])
        
        return L

                

        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.


