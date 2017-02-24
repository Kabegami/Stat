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

#-----------------------------------------------------------------
#                      PARTIE 3 BAGUETTE
#-----------------------------------------------------------------

def transforme_lettre(mot):
    L = []
    for lettre in mot:
        if lettre == "A":
            L.append(0)
        elif lettre == "C":
            L.append(1)
        elif lettre == "G":
            L.append(2)
        elif lettre == "T":
            L.append(3)
        else:
            L.append(-1)
    return L

def code(m,k):
    som = 0
    for chiffre in m:
        k -= 1
        som += chiffre * 4 **(k)
    return som

def invCode(i,k):
    L = []
    for j in range(k,0,-1):
        q = i//(4**(j-1))
        r = i % (4**(j-1))
        L.append(q)
        i = r
    return L

def transforme_mot(nombre):
    """int->str"""
    m = ""
    for chiffre in nombre:
        if chiffre == 0:
            m += ("A")
        elif chiffre == 1:
            m += ("C")
        elif chiffre == 2:
            m += ("G")
        elif chiffre == 3:
            m += ("T")
        else:
            m += ("-")
    return m

def nb_occurences(dico,sequence,k):
    for i in range(0,len(sequence)-k+1):
        valeur = code(sequence[i:i+k],k)
        #valeur = transforme_mot(sequence[i:i+k])
        if valeur >= 0:
            if valeur not in dico:
                dico[valeur] = 1
            else:
                dico[valeur] += 1

def construit_tabk(k):
    tabk = []
    for i in range(4**k):
        num = invCode(i,k)
        #print("num : ",num)
        tabk.append(transforme_mot(num))
    return tabk

def affiche_tabk(tabk,dico):
    for i in dico:
        print("{}:{}".format(tabk[i],dico[i]))

def dico_tabk(tabk,dico):
    dico_lettre = dict()
    for i in range(len(tabk)):
        dico_lettre[dico[i]] = tabk[i]
    return dico_lettre
                

def comptage_observe(k,genome):
    """
        k : taille des mots
        compte les mot dans le genome
    """
    dico = dict()
    for ligne in genome:
        nb_occurences(dico,ligne,k)
    return dico

def comptage_attendu(f,k,l):
    dico = dict()
    tab = construit_tabk(k)
    for mot in tab:
        proba = 1
        nombre = transforme_lettre(mot)
        for chiffre in nombre:
            proba *= f[chiffre]
        dico[mot] = proba*l
    return dico
        
    
        
genome = lit_fasta("yeast_s_cerevisae_genomic_chr1-4.fna")

f = frequence_lettres_genome(genome)
print(f)
m = transforme_lettre("TAC")
i = code(m,len(m))
print(invCode(i,len(m)))

s = transforme_lettre("ATCAT")
print(s)

dico = dict()
nb_occurences(dico,s,2)
print(dico)

tab = construit_tabk(2)
print(tab)

affiche_tabk(tab,dico)

l = compte_nucleotide(genome)
d = comptage_attendu(f,2,l)
d2 = comptage_observe(2,genome)
d2_lettre = dico_tabk(d2,tab)
print("comptage attendu : ",d)
#affiche_tabk(tab,d2)
print("comptage observe",d2_lettre)
#for i in range(5):
#    print(frequence_lettres(Question2[i]))
#print (frequence_lettres_genome(genome))
#print (sum(frequence_lettres_genome(genome)))
#sequence = [1,0,3]
#print(logprobafast(compte_lettres(sequence),(0.2,0.3,0.1,0.4)))
#s = simule_sequence(20,[0.2,0.3,0.1,0.4])
#print(s)
#print(frequence_lettres(s))
