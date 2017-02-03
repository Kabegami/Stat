#-*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as pt

class Grille(object):
    def __init__(self, taille=10):
        self.taille = taille
        self.matrice = np.zeros((taille,taille))

    def __repr__(self):
        return "Grille : \n {}".format(self.matrice)

    def __eq__(self, grilleB):
        for i in range(grilleB.taille):
            for j in range(grilleB.taille):
                if grilleB.matrice[i,j] != self.matrice[i,j]:
                    return False
        return True
        

    def show(self):
        pt.imshow(self.matrice, interpolation="nearest")
        pt.title("Bataille navale TAVU")
        pt.show()

    def peut_placer(self,bateau, position, direction):
    
        for i in range(bateau.taille):
            if (direction == 'h'):
                x = position[0] + i
                y = position[1]
            else:
                x = position[0]
                y = position[1] + i
            if x >= self.taille or y >= self.taille or x < 0 or y < 0:
                return False
            if self.matrice[x,y] != 0:
                return False
        return True

    def place(self,bateau, position, direction):
        #Attention le bateau est toujours placer vers la droite ou le bas par convention
        if not(self.peut_placer(bateau, position , direction)):
            print("impossible de placer le bateau renvoi l'ancienne grille")
        else:
            for i in range(bateau.taille):
                if (direction == 'h'):
                    x = position[0] + i
                    y = position[1]
                else:
                    x = position[0]
                    y = position[1] + i
                self.matrice[x,y] = bateau.idB

    def place_alea(self,bateau):
        x = random.randint(0,self.taille-1)
        y = random.randint(0,self.taille-1)
        direction = ['h','v']
        indDir = direction[random.randint(0,1)]
        return self.place(bateau,(x,y), indDir)

    def enleve(self,bateau, position, direction):
        for i in range(bateau.taille):
            if (direction == 'h'):
                x = position[0] + i
                y = position[1]
            else:
                x = position[0]
                y = position[1] + i
            self.matrice[x,y] = 0

class Bateau(object):
    def __init__(self,nom="RAOUL",idB=1,taille=1):
        self.taille = taille
        self.nom = nom
        self.idB = idB

    def __repr__(self):
        return "nom : {} , taille : {}, id : {}".format(self.nom, self.taille, self.idB)


def liste_bateaux():
    L = []
    L.append(Bateau("porte avion",1,5))
    L.append(Bateau("croiseur",2,4))
    L.append(Bateau("contre-torpilleur", 3,3))
    L.append(Bateau("sous-marin", 4,3))
    L.append(Bateau("torpilleur",5,2))
    return L
    
def genere_grille():
    g = Grille(10)
    L = liste_bateaux()
    for b in L:
        g.place_alea(b)
    return g
    
#Partie Combinatoire du jeu
def nb_facon_grille(G,b):
    #Attention la fonction necessite python 3 sinon utiliser les sets
    cpt = 0
    direction = ['h','v']
    for i in range(0,G.taille):
        for j in range(0,G.taille):
            for d in direction:
                if G.peut_placer(b,(i,j),d):
                    cpt += 1
    return cpt

def nb_place_kBateau(G,L):
    #fait 2 tour de boucles
    nbgrille = 0
    direction = ['h','v']
    for bateau in L:
        for i in range(0,G.taille):
            for j in range(0,G.taille):
                for d in direction:
                    if G.peut_placer(bateau,(i,j),d):
                       G.place(bateau,(i,j),d)
                       nbgrille += nb_facon_grille(G,bateau)
                       print((i,j),d)
                       G.enleve(bateau,(i,j),d)
                       
                    
                        
    return nbgrille

# if __name__ == "__main__":
g = genere_grille()
g.show()
g2 = Grille(2)
L = liste_bateaux()
test = []
test.append(L[-1])
test.append(L[-1])
#test.append(L[-2])

print(test)
cpt = nb_facon_grille(g2,test[0])
errorincoming = nb_place_kBateau(g2,test)
print(cpt)
print(errorincoming)
