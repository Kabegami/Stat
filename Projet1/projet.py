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

class Bateau(object):
    def __init__(self,nom="RAOUL",idB=1,taille=1):
        self.taille = taille
        self.nom = nom
        self.idB = idB

    def __repr__(self):
        return "nom : {} , taille : {}, id : {}".format(self.nom, self.taille, self.idB)

class Direction(object):
    def __init__(self, direction):
        self.direction = direction
        if self.direction == "haut":
            self.vecteur = np.array([0,1])
        elif self.direction == "bas":
            self.vecteur = np.array([0,-1])
        elif self.direction == "droite":
            self.vecteur = np.array([1,0])
        else:
            self.vecteur = np.array([-1,0])

    def decalage_direction(self, position, facteur):
        return np.array[position] + facteur*self.vecteur
                
    
def peut_placer(bateau, grille, position, direction):
    #la direction est un tuple appartenant a {(0,1): droite, (1,0):haut ,(-1,0):bas, (0,-1):gauche}
    #Si possible faire classe Direction(nom) -> nom, vecteur comme plus haut
    for i in range(bateau.taille):
        x = position[0] + i*direction[0]
        y = position[1] + i*direction[1]
        if x >= grille.taille or y >= grille.taille or x < 0 or y < 0:
            return False
        if grille.matrice[x,y] != 0:
            return False
    return True

def place(bateau, grille, position, direction):
    if not(peut_placer(bateau, grille, position , direction)):
        print("impossible de placer le bateau renvoi l'ancienne grille")
        return grille
    else:
        for i in range(bateau.taille):
            x = position[0] + i*direction[0]
            y = position[1] + i*direction[1]
            grille.matrice[x,y] = bateau.idB
        return grille
    
def place_alea(bateau, grille):
    x = random.randint(0,9)
    y = random.randint(0,9)
    direction = [(0,1), (0,-1),(1,0),(-1,0)]
    indDir = direction[random.randint(0,3)]
    return place(bateau, grille,(x,y), indDir)


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
        place_alea(b,g)
    return g
    



# if __name__ == "__main__":
g = genere_grille()
g.show()
