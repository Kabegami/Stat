#-*- coding: utf-8 -*-

from random import *
from datastructures import *

class Generateur(object):
    """ On veut construire des graphes ergodiques: il faut donc qu'ils soient apériodiques, et irréductible(une seule composante fortement connexe) et finie(forcement finie)
-pour avoir un graphe apériodique : il faut 2 cycle et que leur pgcd soit egal a 1
- pour avoir une seule composante fortement connexe : a chaque fois que l'on rajoute un arc, on verifie qu'il existe un chemin depuis le nouveau sommet vers tous les sommets du graphe ( complexite tres grande)
une methode plus rapide serai de faire tous nos sommets dans une grande boucle mais on a des graphes trop specifiques, perte de généralité
methode du boss : On construit notre de graphe de maniere completement aléatoire, puis on met une boucle sur un sommet, ensuite on calcule le graphe des composantes fortements connexes et pour chaque composante sans arc sortant on en genere un aléatoirement
la methode du boss c de la merd du coup on fait un anneau de sommet ou pour eviter une perte de généralité un anneau d'anneau"""

    def __init__(self, nbSommet):
        self.nbSommet = nbSommet
        self.nbArc = nbSommet

    def genere(self):
        graphe = SimpleWeb(self.nbSommet)
        #on initialise le noeud de depart
        prec = randint(0,self.nbSommet-1)
        first = prec
        deja_vu = set()
        deja_vu.add(prec)
        for i in range(self.nbArc-1):
            #do while
            r = randint(0, self.nbSommet-1)
            while r in deja_vu:
                r = randint(0, self.nbSommet-1)
            deja_vu.add(r)
            graphe.addArc(prec, r)
            if i == 1:
                graphe.addArc(first,r)
            prec = r
        #on ajoute un arc vers le debut
        graphe.addArc(prec, first)
        #D'apres le theoreme de bezout le pgcd(n,n+1) = 1, donc si on a une boucle de taille 1 c'est ergodique.
        return graphe
    
        
