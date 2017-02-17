import os
#-*- coding: utf-8 -*-

import math
import io
import random

def ouvre(fichier):
    L = []
    os.chdir("sequences")
    f = io.open(fichier,'r')
    for lire in f.readlines():
        L.append(lire)
    f.close()
    os.chdir("..")
    return L

def compte_nucleotide(sequence):
    cpt = 0
    for i in range(len(sequence)):
        if sequence[i][0] != ">":
            cpt += len(sequence[i])
    return cpt

def lit_fasta(fichier):
    L = ouvre(fichier)
    retour = []
    for i in range(len(L)):
        if L[i][0] != ">":
            ligne = []
            for lettre in L[i]:
                if lettre == "A":
                    ligne.append(0)
                elif lettre == "C":
                    ligne.append(1)
                elif lettre == "G":
                    ligne.append(2)
                elif lettre == "T":
                    ligne.append(3)
                else:
                    ligne.append(-1)
            retour.append(ligne)
    return retour
                    
def compte_lettres(liste_entier):
    #on travail sur des entier(le numero associé au lettre) pas sur les indices des dico
    dico = dict()
    dico[0] = 0
    dico[1] = 0
    dico[2] = 0
    dico[3] = 0
    dico[-1] = 0
    for i in liste_entier:
        dico[i] += 1
    return (dico[0],dico[1],dico[2],dico[3])

def frequence_lettres(liste_entier):
    t = compte_lettres(liste_entier)
    cpt = 0
    L = []
    for i in t:
        cpt += i
        L.append(i)
    #si aucun nucleotide n'a été lu on retourne ce tuple pour ne pas avoir de division par 0
    if (cpt == 0):
        return (0,0,0,0)    
    for i in range(len(L)):
        L[i] = L[i]/(float)(cpt)    
    return (L[0], L[1], L[2], L[3])

def frequence_lettres_genome(genome):
    # init
    frequence = []
    for i in range(4):
        frequence.append(0)

    nb = len(genome)
    for ligne in genome:
        res = frequence_lettres(ligne)
        if res == (0,0,0,0):
            nb -= 1
        for i in range(len(res)):
            frequence[i] += res[i]

    for i in range(len(frequence)):
        frequence[i] = frequence[i] / (float)(nb)
    return (frequence[0], frequence[1], frequence[2], frequence[3])

def logproba(liste_entier, m):
    proba = 0
    for nb in liste_entier:
        proba += math.log(m[nb])
    return proba

def logprobafast(nb_lettre, m):
    proba = 0
    for i in range(len(nb_lettre)):
        proba += nb_lettre[i]*math.log(m[i])
    return proba

def simule_sequence(lg,m):
    L = []
    retour = []
    entiers= [0,1,2,3]
    for idfrequence in range(len(m)):
        for i in range((int)(m[idfrequence]*lg)):
            L.append(entiers[idfrequence])
    for nb in range(lg):
        retour.append(random.choice(L))
    return retour

genome = lit_fasta("yeast_s_cerevisae_genomic_chr1-4.fna")
#for i in range(5):
#    print(frequence_lettres(Question2[i]))
print (frequence_lettres_genome(genome))
print (sum(frequence_lettres_genome(genome)))
sequence = [1,0,3]
print(logprobafast(compte_lettres(sequence),(0.2,0.3,0.1,0.4)))
s = simule_sequence(20,[0.2,0.3,0.1,0.4])
print(s)
print(frequence_lettres(s))
