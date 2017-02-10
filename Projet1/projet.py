#-*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as pt

#-------------------------------------------------------------
#                          FONCTION
#-------------------------------------------------------------
def liste_bateaux():
    L = []
    L.append(Bateau("porte avion",1,5))
    L.append(Bateau("croiseur",2,4))
    L.append(Bateau("contre-torpilleur", 3,3))
    L.append(Bateau("sous-marin", 4,3))
    L.append(Bateau("torpilleur",5,2))
    return L
    
def genere_grille(taille=10):
    g = Grille(taille)
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

def nb_place_kBateauRec(G,L):
    #on fixe recursivement les differents bateaux
    nbgrille = 0
    if len(L) == 1:
        #On calcule le nombre de facon de placer le dernier bateau
        return nb_facon_grille(G,L[0])
    else:
        direction = ['h','v']
        for i in range(0,G.taille):
            for j in range(0,G.taille):
                for d in direction:
                    if G.peut_placer(L[0],(i,j),d):
                        G.place(L[0],(i,j),d)
                        nbgrille += nb_place_kBateauRec(G,L[1:])
                        G.enleve(L[0],(i,j),d)
    return nbgrille


#APPROXIMATION A FAIRE (TOUT DOUX)>.<

def nb_place_kBateauRec_Memoisation(G,L,dico):
    #apparament comme G est un objet statique ne marche pas
    TailleBateau = []
    for i in L:
        TailleBateau.append(i.taille)
    if (G.matrice,TailleBateau) in dico:
        return dico[(G.matrice,TailleBateau)]
    nbgrille = 0
    if len(L) == 1:
        #On calcule le nombre de facon de placer le dernier bateau
        n = nb_facon_grille(G,L[0])
        dico[(G.matrice,L)] =  n
        return n
    else:
        direction = ['h','v']
        for i in range(0,G.taille):
            for j in range(0,G.taille):
                for d in direction:
                    if G.peut_placer(L[0],(i,j),d):
                        G.place(L[0],(i,j),d)
                        nbgrille += nb_place_kBateauRec(G.matrice,L[1:])
                        G.enleve(L[0],(i,j),d)
    dico[(G.matrice,L)] = nbgrille
    return nbgrille

def genere_grille_egale(G):
    cpt = 1
    Galea = genere_grille(G.taille)
    while Galea != G:
        cpt += 1
        Galea = genere_grille(G.taille)
    return cpt

#-----------------------------------------------
#                    CLASSES
#-----------------------------------------------

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
        

    def show(self,title="Bataille navale TAVU"):
        pt.imshow(self.matrice, interpolation="nearest")
        pt.title(title)
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
            b = False
           # print("impossible de placer le bateau renvoi l'ancienne grille")
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
        while self.peut_placer(bateau,(x,y),indDir) == False:
             x = random.randint(0,self.taille-1)
             y = random.randint(0,self.taille-1)
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

class Joueur(object):
    def __init__(self,nom="J1",taille=10, ListeBateauAdv=liste_bateaux()):
        """Correspond a un joueur de bataille navale, possede une Grille et une Grille remplis de : 0 si la case non exploré, -1 si le coup a raté et 1 si il a touché un bateau"""
        self.nom = nom
        self.taille = taille
        self.MaGrille = genere_grille(taille)
        self.GrilleAdv = Grille()
        self.ListeBateauAdv = ListeBateauAdv
        self.GrilleProba = Grille()

    def Tir(self,Adv,i,j):
        """ Grille,int,int -> met a jour GrilleAdv""" 
        if Adv.matrice[(i,j)] == 0:
            #aucun bateau n'a ete touché
            self.GrilleAdv.matrice[(i,j)] = -1
            return False
        else:
            self.GrilleAdv.matrice[(i,j)] = 1
            return True

    def Aleatoire(self,Adv):
        """ Grille -> (boolean, int, int) 
        Appelle la fonction Tir"""
        x = random.randint(0,Adv.taille-1)
        y = random.randint(0,Adv.taille-1)
        #si la case n'a pas encore été exploré
        while(self.GrilleAdv.matrice[(x,y)] != 0):
            x = random.randint(0,Adv.taille-1)
            y = random.randint(0,Adv.taille-1)
            #print("(x,y) : ({},{})".format(x,y))
        return (self.Tir(Adv,x,y),x,y)

    def Coup_Cible(self,Adv,x,y):
        #on peut ameliorer la fonction car si il trouve a gauche chercher seulement a droite apres et inversement de meme pour haut et bas
        cpt = 0
        curseur = 1
        #explore a droite
        while  x+curseur < Adv.taille and self.Tir(Adv,x+curseur,y):
            curseur += 1
            cpt += 1
        curseur = 0
        #gauche
        while x-curseur >= 0 and self.Tir(Adv,x-curseur,y):
            curseur += 1
            cpt += 1
        curseur = 0
        #bas
        while y+curseur < Adv.taille and self.Tir(Adv,x,y+curseur):
            curseur += 1
            cpt += 1
        curseur = 0
        #haut
        while y-curseur >= 0 and self.Tir(Adv,x,y-curseur):
            curseur += 1
            cpt += 1
        curseur = 0
        return cpt
        
        
    def BateauCouler(self,Adv,idBateau):
        for x in range(Adv.taille):
            for y in range(Adv.taille):
                if Adv.matrice[(x,y)] == idBateau and self.GrilleAdv.matrice[(x,y)] != 1:
                    return False
        return True

    def ResteBateau(self,Adv):
        for bateau in self.ListeBateauAdv:
            if not(self.BateauCouler(Adv,bateau.idB)):
                return True
        return False

    def StrategieAleatoire(self,Adv):
        cpt = 0
        while self.ResteBateau(Adv):
            self.Aleatoire(Adv)
            cpt += 1
        return cpt

    def StrategieHeuristique(self,Adv):
        cpt = 0
        while self.ResteBateau(Adv):
            (b,i,j) = self.Aleatoire(Adv)
            cpt += 1
            #tant qu'il n'a pas touché une case
            while b != True:
                #La fonction aleatoire tire renvoi un boolean et la case
                (b,i,j) = self.Aleatoire(Adv)
            cpt += 1
            print("entrer coup cible : ({},{})".format(i,j))
            cpt += self.Coup_Cible(Adv,i,j)
        return cpt

    def BateauPossible(self,b,x,y,i,j,d):
        """ Prend un bateau b, et une position initiale x,y et une borne i,j """
        if d == "h":
            for c in range(i,j+1):
                if self.GrilleAdv.matrice[(c,y)] == -1:
                    return False
            return True
        else:
            for c in range(i,j+1):
                if self.GrilleAdv.matrice[(x,c)] == -1:
                    return False
            return True
    
    def PossibiliteBateauSurCase(self,b,x,y):
        """ Retourne si le bateau b peut être sur la case x,y en fonction des cases explorées
        amelioration possible"""
        i = x - b.taille
        j = x
        #verif des bornes inferieures
        if i < 0:
            i = 0
            j = b.taille
        nb = 0
        #Axe horizontal
        while  j < self.GrilleAdv.taille and j < x + b.taille:
            if self.BateauPossible(b,x,y,i,j,"h"):
                nb += 1
            i += 1
            j += 1
            
        #Axe vertical
        i = y - b.taille
        j = y
        if i < 0:
            i = 0
            j = b.taille
        while j < self.GrilleAdv.taille and j < y + b.taille:
            if self.BateauPossible(b,x,y,i,j,"v"):
                nb += 1
            i += 1
            j += 1
        return nb


    def MatriceProba(self, b):
        """ Renvoie un tuple (b, GrilleProba) avec b = false si on peut placer le bateau nule part""" 
        GrilleProba = Grille()
        cpt = 0
        #on calcule le nombre de position possible
        for x in range(self.GrilleAdv.taille):
            for y in range(self.GrilleAdv.taille):
                cpt += self.PossibiliteBateauSurCase(b,x,y)
        if cpt == 0:
            return (False, GrilleProba)
        #on actualise la matrice
        for x in range(self.GrilleAdv.taille):
            for y in range(self.GrilleAdv.taille):
                nb = (float)(self.PossibiliteBateauSurCase(b,x,y))
                GrilleProba.matrice[(x,y)] = nb/cpt
        return (True, GrilleProba)

    def UpdateGrilleProba(self):
        cpt = 0
        for b in self.ListeBateauAdv:
            #si on peut placer le bateau
            if self.MatriceProba(b)[0]:
                self.GrilleProba.matrice = np.add(self.GrilleProba.matrice, self.MatriceProba(b)[1].matrice)
        #print("UpdateGrilleProba :", self.GrilleProba)

    def StrategieProbaSimple(self,Adv):
        cpt = 0
        maxPb = 0
        xMax = 0
        yMax = 0
        while self.ResteBateau(Adv):
            self.UpdateGrilleProba()
            for x in range(self.GrilleProba.taille):
                for y in range(self.GrilleProba.taille):
                    #on verifie que la case n'a pas été deja exploré
                    if self.GrilleProba.matrice[(x,y)] > maxPb and self.GrilleAdv.matrice[(x,y)] == 0:
                        maxPb = self.GrilleProba.matrice[(x,y)]
                        xMax = x
                        yMax = y
            #print(self.GrilleProba.matrice)
            self.Tir(Adv,xMax,yMax)
            print("tire sur la case ({},{})".format(xMax,yMax))
            cpt += 1
        return cpt
        

# if __name__ == "__main__":
#g = genere_grille(4)
#g.show()
g2 = Grille(3)
L = liste_bateaux()
test = []
test.append(L[-2])
test.append(L[-2])
test.append(L[-2])

print(test)
cpt = nb_facon_grille(g2,test[0])
errorincoming = nb_place_kBateau(g2,test)
print(cpt)
print(errorincoming)
print("version recursive : ")
Rec = nb_place_kBateauRec(g2,test)
print(Rec)
dico = dict()
#nb = genere_grille_egale(g)
#print("Nombre de tentative avant d'obtenir la meme grille : ",nb)

j1 = Joueur()
adv = genere_grille()
print(adv)
n = j1.StrategieProbaSimple(adv)
print("nombre de coup : ",n)
print("matrice probabiliste :",j1.GrilleProba.matrice)
j1.GrilleAdv.show("matrice d'exploration")
adv.show("matrice de l'adversaire")
