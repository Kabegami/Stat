#-*- coding: utf-8 -*-

from datastructures import *
import random

class Internaute(object):
    def __init__(self, graphe):
        self.graphe = graphe
        self.pos = 0
        self.pi = []
        self.nb_pas = None
        self.fichier = None

    def goTo(self,id_node):
        self.pos = id_node
        self.pi = [0 for i in range(self.graphe.nombreSommet)]

    def pas(self):
        liste_proba = self.graphe.matriceProba[self.pos]
        i = trouve_noeud(liste_proba)
        #print("on va sur le somme : {} ".format(i))
        self.pos = i
        self.pi[i] += 1

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
        
    def walk(self,nb_iter,seuil):
        cpt = 0
        epsilon = 1
        old_pi = self.pi[::]
        new_pi = self.pi[::]
        while cpt < nb_iter and epsilon > seuil:
            old_pi = self.pi[::]
            self.pas()
            new_pi = self.pi[::]
            epsilon = calcule_epsilon(old_pi, new_pi)
            if (self.nb_pas != None and self.fichier != None):
                if cpt % self.nb_pas == 0 and cpt != 0:
                    self.ecrit(cpt, epsilon)
                    #print("epsilon : {}".format(epsilon))
            cpt += 1
            
        #print("\n------- INTERNAUTE -------")
        #print("iterations : {}".format(cpt))
        #print("epsilon : {}\n".format(epsilon))
            

    def showFrequencies(self):
        print("pi : {}".format(self.pi))
        somme_new = sum(self.pi)
        L = []
        for i in range(len(self.pi)):
            if somme_new == 0:
                L.append(0)
            else:
                L.append(self.pi[i]/(1.0*somme_new))
        print(L)

# -----------------------------------------------------------
#                   FONCTION
# -----------------------------------------------------------

def trouve_noeud(liste_noeud):
    r = random.random()
    for i in range(len(liste_noeud)):
        if r < liste_noeud[i]:
            return i
        r = r - liste_noeud[i]

def calcule_epsilon(old_pi, pi):
    #on transforme en frequences
    somme_old = sum(old_pi)
    somme_new = sum(pi)
    for i in range(len(old_pi)):
        if somme_old == 0:
            old_pi[i] = 0
        else:
            old_pi[i] = old_pi[i]/(1.0*somme_old)
        if somme_new == 0:
            pi[i] = 0
        else:
            pi[i] = pi[i]/(1.0*somme_new)

    #on calcule la distance
    epsilon = 0
    for i in range(len(old_pi)):
        epsilon = max(epsilon, abs(old_pi[i] - pi[i]))
    return epsilon
