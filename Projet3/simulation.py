#-*- coding: utf-8 -*-
from datastructures import *
from internautes import calcule_epsilon

class Simulation(object):
    def __init__(self, graphe, pi0):
        self.graphe = graphe
        self.pi0 = pi0
        self.pi = pi0
        self.nb_pas = None
        self.fichier = None

    def trace(self, nb_pas, fichier):
        self.nb_pas = nb_pas
        self.fichier = fichier
        #on supprime l'ancienne valeur
        f = open(self.fichier, 'w')
        f.close()

    def ecrit(self, nb, epsilon):
        #on crée les nouvelles valeurs
        f = open(self.fichier, 'a')
        e = (str)(epsilon)
        f.write(str(nb) + ' ' + e + '\n')
        f.close()
        
    def calcule_piT(self, itermax, seuil):
        epsilon = 1
        cpt = 0
        while epsilon > seuil and cpt < itermax:
            new_pi = self.graphe.nextStep(self.pi)
            epsilon = calcule_convergence(self.pi, new_pi)
            if self.nb_pas != None and self.fichier != None:
                if cpt % self.nb_pas == 0 and cpt != 0:
                    self.ecrit(cpt, epsilon)
                    #print("epsilon : {}".format(epsilon))
            self.pi = new_pi
            cpt += 1
            
        #print("\n------- SIMULATION -------")
        #print("iterations : {}".format(cpt))
        #print("epsilon : {}\n".format(epsilon))
        return self.pi

def calcule_convergence(old_pi, pi):
    dif = abs(pi - old_pi)
    #print("dif : {}".format(dif))
    pgd = 0
    for valeur in dif:
        pgd = max(pgd, valeur)
    return pgd
    
"""
Quelques remarques : Dans NanoWeb 1 on remarque qu'on converge vers le sous graphe absorbant {7,8}, avec une probabilité 0.25 | 0.75 ou l'inverse. c'est du au fait que notre pi represente la probabilité d'etre a la position x a l'instant t. Donc selon qu'on soit entré dans le sous-graphe a une iteration paire ou impaire dans ce cas, cela change les probabilités"""

""" p2 = distribution des probabilités des positions au bout de la 2ème iterations a partir de p"""
