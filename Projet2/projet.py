# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import math
import io
import random
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.special import binom

#-----------------------------------------------------------------
#                LECTURE DES FICHIERS ET DONNEES
#-----------------------------------------------------------------

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
    return len(sequence)

def lit_fasta(fichier):
    '''
    fichier -> [[int]]
    retourne la liste de liste de int
    '''
    L = enleve_titre_sequence(fichier)
    retour = []
    for lettre in L:
        if lettre == "A":
            retour.append(0)
        elif lettre == "C":
            retour.append(1)
        elif lettre == "G":
            retour.append(2)
        elif lettre == "T":
            retour.append(3)
        else:
            retour.append(-1)
    return retour

def enleve_titre_sequence(fichier):
    L = ouvre(fichier)
    retour = []
    for i in range(len(L)):
        if L[i][0] != ">":
           retour.append(L[i])
    return ''.join(retour)
                    
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

def simule_sequence2(lg,m):
    retour = []
    v = np.cumsum(m)
    for i in lg:
        retour.append(random.choice(v))
    return retour
    
def simule_sequence(lg,m):
    """ lg -> longueur, m frequences des lettres
    legerement incorrect car on cast le nombre d'element"""
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
#                  PARTIE 3 : DESCRIPTION EMPIRIQUE
#-----------------------------------------------------------------

def transforme_en_nombre(mot):
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
    '''
    m : mot préalablement converti en tableau d'entiers
    k : longueur du mot
    '''
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

def transforme_en_lettre(nombre):
    """tableau de int -> str"""
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

def nb_occurrences(occur,sequence,mots,k):
    '''
    dico : dictionnaire dans lequel on stocke les couples (mot, occurrences)
    sequence : sequence a regarder
    k : longueur d'un mot
    '''

    for i in range(0,len(sequence)-k+1):
        valeur = code(sequence[i:i+k],k)
        if valeur >= 0:
            occur[valeur] += 1
    return occur

def mots_possibles(k):
    '''
    renvoie le tableau des entiers correspondant aux entiers possibles
    '''
    return [x for x in range(4**k)]

def mots_possibles_lettres(k):
    '''
    renvoie le dico des mots de longueur k qui peuvent être rencontrés
    '''
    mots = mots_possibles(k)
    dico = dict((key, 0) for key in mots)
    for i in dico:
        num = invCode(i,k)
        #print("num : ",num)
        #tabk.append(transforme_en_lettre(num))
        dico[i] = transforme_en_lettre(num)
    return dico



def affiche_nb_mots(dico):
    for i in dico:
        print("{}: {}".format(i,dico[i]))

def dico_tabk(tabk,dico):
    dico_lettre = dict()
    for i in range(len(tabk)):
        dico_lettre[dico[i]] = tabk[i]
    return dico_lettre
                

def comptage_observe(k,sequence,mots):
    """
    k : longueur d'un mot
    mots : tableau des mots possibles de longueur k
    compte les mots de longueur k suivant le tableau de mots possibles
    """
    # initialisation du dictionnaire pour chaque mot possible
    occur = dict((key, 0) for key in mots)
    nb_occurrences(occur,sequence,mots,k)
    return occur

def comptage_attendu(k,mots,freq,nb):
    '''
    k : longueur du mot
    mots : liste de mots possibles (sous forme de tableau d'entiers)
    freq : tuple contenant la frequence attendue de chaque lettre
    nb : nombre total de nucléotides dans la séquence
    '''
    dico = dict((key, 0) for key in mots)
    for mot in mots:
        proba = 1
        tab_mot = invCode(mot, k)
        for chiffre in tab_mot:
            proba *= freq[chiffre]
        dico[mot] = proba*nb
    return dico
        

def plot_expected_vs_observed(sequence, k):
    ''' 
    k est la longueur des mots à dénombrer
    comptage_att et comptage_obs sont des dictionnaires (mot, nombre d'occurrences)
    '''

    freq = frequence_lettres(sequence)              # fréquence des lettres
    nbtotal = compte_nucleotide(sequence)           # occurrences des nucléotides

    mots = mots_possibles(k)
    mots_lettres = mots_possibles_lettres(k)
    comptage_att = comptage_attendu(k,mots,freq,nbtotal)
    comptage_obs = comptage_observe(k,sequence,mots)


    xvalues = comptage_att.values()
    yvalues = comptage_obs.values()
    #difference = [(x[i] - y[i]) for i in range(len(x))]
    #print(difference)

    # affichage graphique des occurrences
    fig, ax = plt.subplots()
    ax.plot(xvalues, yvalues, 'o')
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
    ]
    ax.plot(lims, lims)
    ax.set_xlabel("Nombre d'occurrences attendu")
    ax.set_ylabel("Nombre d'occurrences observé")
    ax.set_xlim(lims)
    ax.set_ylim(lims)

    title = "Mots de longueur " + str(k) + " pour la sequence PHO"
    ax.set_title(title)
    ax.legend(loc='best')

    # on montre les mots si la longueur est égale à 2
    # illisible si > 2
    if (k == 2):
        print("nombre de nucléotides : " + str(nbtotal))
        print("fréquences de lettres attendues")
        print(freq)
        print("comptage attendu")
        affiche_nb_mots(comptage_att)
        print("somme = " + str(sum(comptage_att.values())))
        print("")
        print("comptage observe")
        affiche_nb_mots(comptage_obs)
        print("somme = " + str(sum(comptage_obs.values())))
        
        labels = [i for i in mots_lettres]
        for label, x, y in zip(labels, xvalues, yvalues):
            plt.annotate(
                label,
                xy=(x, y), xytext=(-20, 20), fontsize=8,
                textcoords='offset points', ha='right', va='bottom',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5),
                arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

    fig.set_size_inches(10, 6)
    fig.show()

#-----------------------------------------------------------------
#             SIMULATION DE SEQUENCES ALEATOIRES
#-----------------------------------------------------------------

def simulation(taille_sequence, nombre_sequence, frequence_lettres):
    L = []
    for i in range(nombre_sequence):
        L.append(simule_sequence(taille_sequence,frequence_lettres))
    return L

def calcule_proba_empirique(n, k, liste_mots, liste_sequences, frequence_lettres):
    '''
    n : nombre de fois où on observe chaque mot, pour calculer la probabilité empirique
    '''

    # stocke le nombre de séquences où chaque mot est apparu au moins n fois
    count_nb_sequences = [0 for i in range(len(liste_mots))]

    mots = mots_possibles(k)
    mots_lettres = mots_possibles_lettres(k)
    comptage_att = comptage_attendu(k, mots, frequence_lettres, len(liste_sequences[0]))
    somme = 0
    for sequence in liste_sequences:
        comptage_obs = comptage_observe(k,sequence,mots)
        for key in comptage_obs:
            for i in range(len(liste_mots)):
                #si c'est un des mots recherchés et qu'on a nombre d'occurences >= n
                if liste_mots[i] == key:
                    if comptage_obs[key] >= n:
                        count_nb_sequences[i] += 1

    dico_proba = dict()
    for i in range(len(count_nb_sequences)):
        tab_mot = invCode(liste_mots[i], k)
        mot_lettre = transforme_en_lettre(tab_mot)
        count_nb_sequences[i] = count_nb_sequences[i] / (len(liste_sequences)*1.0)
        dico_proba[mot_lettre] = count_nb_sequences[i]
                
    return dico_proba

def histo_proba_mot(n, liste_mots, proba_mots, nombre_sequences):
    fig, ax = plt.subplots()

    # espacement des labels sur l'axe x
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    x = np.arange(len(liste_mots))
    labels = []
    proba = []
    bar_width = 0.3
    alpha = 0.8
    for i in range((n/2)+1):
        proba.append(proba_mots[i].values())
        labels.append("n = " + str(i*2+1))

    #ax.bar(x - bar_width, proba[0], bar_width, label=labels[0], align='center', alpha=alpha)
    ax.bar(x, proba[0], bar_width, label=labels[0], align='center', alpha=alpha)
    #ax.bar(x + bar_width, proba[2], bar_width, label=labels[2], align='center', alpha=alpha)

    ax.set_xticks(x)
    ax.set_xticklabels(proba_mots[0].keys())
    ax.set_title("Probabilité d'observer un mot au moins " + str(n) + " fois sur "
                  + str(nombre_sequences) + " sequences")
    ax.set_ylabel("Probabilité")
    ax.legend(loc='best')
    fig.show()

def plot_distribution_mots(n, sequence, liste_mots_lettres, k, nombre_sequences):
    '''
    n : nombre de fois où on observe chaque mot, pour calculer la probabilité empirique
    k est la longueur d'un mot
    '''
    liste_mots = []
    for m in liste_mots_lettres:
        liste_mots.append(code(transforme_en_nombre(m), k))
        
    freq = frequence_lettres(sequence)
    print(freq)
    liste_sequences = simulation(len(sequence), nombre_sequences, freq)
    dist = calcule_proba_empirique(n, k, liste_mots, liste_sequences, freq)
        
    print("n = 1",dist)
    
    histo_proba_mot(n, liste_mots, [dist], nombre_sequences)

#-----------------------------------------------------------------
#                     PROBABILITES DE MOTS
#-----------------------------------------------------------------

'''
Dans les fonctions qui suivent, les paramètres sont les suivants :
    k : longueur d'un mot
    n : nombre de fois où le mot dont on souhaite calculer la probabilité
    l : longueur totale de la séquence étudiée
    mot : mot dont on veut étudier la probabilité d'apparition
    freq : tuple des fréquences d'apparition de chaque lettre dans une séquence donnée
'''

def proba_theorique(k, n, l):
    q = l - k + 1
    a = binom(q, n)
    b = (1.0/4**k)**n
    c = (1 - (1.0/4**k))**(q-n)
    return a*b*c

def proba_theorique_freq(mot, k, n, l, freq):
    proba = 1
    tab_mot = invCode(mot, k)
    for chiffre in tab_mot:
        proba *= freq[chiffre]

    q = l - k + 1
    a = binom(q, n)
    b = (proba)**n
    c = (1.0 - proba)**(q-n)
    return a*b*c

def proba_poisson(mot, k, n, l, freq):
    proba = 1
    tab_mot = invCode(mot, k)
    for chiffre in tab_mot:
        proba *= freq[chiffre]

    q = l - k + 1
    lamb = q * proba
    return math.exp(-lamb)*(lamb**n)/math.factorial(n)

def proba_occurrence(liste_mots, n, longueur_sequence, freq):
    '''
    liste_mots est la liste des mots en chaines de caracteres (pour la visibilité)
    '''
    proba = dict((key, 0) for key in liste_mots)

    for mot in liste_mots:
        mot_entiers = code(transforme_en_nombre(mot),len(mot))
        proba_mot = 1

        # par application de la formule de l'événement contraire
        for i in range(n):
            proba_mot -= proba_poisson(mot_entiers, len(mot), i, longueur_sequence, freq)
        proba[mot] = proba_mot
    return proba

def plot_graph_theo(n, liste_mots, proba_mots, proba_theo, nombre_sequences):
    fig, ax = plt.subplots()

    # espacement des labels sur l'axe x
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    x = np.arange(len(liste_mots))
    labels = ["empirique", "théorique"]
    proba = [proba_mots.values(), proba_theo.values()]
    bar_width = 0.3
    alpha = 0.8

    #ax.bar(x - bar_width, proba[0], bar_width, label=labels[0], align='center', alpha=alpha)
    ax.bar(x - bar_width/2, proba[0], bar_width, label=labels[0], align='center', alpha=alpha)
    ax.bar(x + bar_width/2, proba[1], bar_width, label=labels[1], align='center', alpha=alpha)

    ax.set_xticks(x)
    ax.set_xticklabels(proba_mots.keys())
    ax.set_title("Probabilité d'observer un mot au moins " + str(n) + " fois sur "
                  + str(nombre_sequences) + " sequences")
    ax.set_ylabel("Probabilité")
    ax.legend(loc='best')
    fig.show()

def plot_theorique_vs_empirique(n, sequence, liste_mots, nombre_sequences):
    liste_mots2 = []
    for m in liste_mots:
        liste_mots2.append(code(transforme_en_nombre(m), len(m)))
    freq = frequence_lettres(sequence)

    sim = simulation(len(sequence), nombre_sequences, freq) 
    proba_emp = calcule_proba_empirique(n, len(liste_mots[0]), liste_mots2, sim, freq)
    proba_theo = proba_occurrence(liste_mots, n, len(sequence), freq)
    print(proba_theo)
    print(proba_emp)
    plot_graph_theo(n, liste_mots, proba_emp, proba_theo, nombre_sequences)

def mots_inattendus(n, k, sequence, nombre_sequences):
    '''
    n : nombre d'occurences minimum
    k : longueur d'un mot
    '''
    
    mots = mots_possibles(k)
    mots_lettres = mots_possibles_lettres(k)
    freq = frequence_lettres(sequence)
    sim = simulation(len(sequence), nombre_sequences, freq) 
    proba_emp = calcule_proba_empirique(n, k, mots, sim, freq)

    liste_mots = [mots_lettres[i] for i in range(len(mots_lettres))]
    proba_theo = proba_occurrence(liste_mots, n, len(sequence), freq)

    #print(proba_theo)
    #print(proba_emp)
    mots_surprise = []
    for key in proba_theo:
        if 5*proba_theo[key] < proba_emp[key]:
            mots_surprise.append((key, proba_theo[key], proba_emp[key]))
    return mots_surprise

#-----------------------------------------------------------------
#                           TESTS
#-----------------------------------------------------------------

genome = lit_fasta("yeast_s_cerevisae_genomic_chr1-4.fna")
pho = lit_fasta("regulatory_seq_PHO.fasta")
gal = lit_fasta("regulatory_seqs_GAL.fasta")
met = lit_fasta("regulatory_seqs_MET.fasta")

print(len(genome))
print(len(pho))
print(len(gal))
print(len(met))

#-----------------------------------------------------------------
#                  TEST DESCRIPTION EMPIRIQUE
#-----------------------------------------------------------------

m = transforme_en_nombre("TAC")
i = code(m,len(m))
print(invCode(i,len(m)))


s = transforme_en_nombre("ATCAT")
print(s)
print("-----------------------------")
print("")

#-----------------------------------------------------------------
#                  TEST FREQUENCES ATTENDUES
#-----------------------------------------------------------------

#print(frequence_lettres(pho))
#plot_expected_vs_observed(pho, 2)

#-----------------------------------------------------------------
#             TEST SIMULATION DE SEQUENCES ALEATOIRES
#-----------------------------------------------------------------

liste_mots = ["ATCTGC", "TTTAAA", "ATATAT", "AAAAAA"]

print("probabilités empiriques")
#plot_distribution_mots(1, pho, liste_mots, len(liste_mots[0]), 1000)
mot = code(transforme_en_nombre(liste_mots[0]),6)

print("\nprobabilités théoriques")
#print(1-proba_theorique(len(liste_mots[i]), 0, len(pho)))
#print(1-proba_theorique_freq(mot,len(liste_mots[0]), 0, len(pho), freq))
#print(1 - proba_poisson(mot, len(liste_mots[0]), 0, len(pho), freq))

#plot_theorique_vs_empirique(1, pho, liste_mots, 1000)
#print(mots_inattendus(4, 6, pho, 100))
