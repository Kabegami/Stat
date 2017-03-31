#-*- coding: utf-8 -*-
from datastructures import *

class Simulation(object):
    def __init__(self, graphe, pi0):
        self.graphe = graphe
        self.pi0 = pi0
        self.pi = pi0

    def calcule_piT(self,epsilon, itermax):
        convergence = 1
        cpt = 0
        while convergence > epsilon and cpt < itermax:
            new_pi = self.graphe.nextStep(self.pi)
            convergence = calcule_convergence(self.pi, new_pi)
            self.pi = new_pi
            cpt += 1
        print("convergence : {}".format(convergence))
        print("nombre d'itération necessaire : {}".format(cpt))
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
