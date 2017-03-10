import os
#-*- coding: utf-8 -*-

import math
import io
import random
import matplotlib.pyplot as plt
import numpy as np

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
#                           PARTIE 3
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

def nb_occurences(occur,sequence,mots,k):
    '''
    dico : dictionnaire dans lequel on stocke les couples (mot, occurences)
    sequence : sequence a regarder
    k : longueur d'un mot
    '''

    for i in range(0,len(sequence)-k+1):
        valeur = code(sequence[i:i+k],k)
        if valeur >= 0:
            occur[valeur] += 1
    return occur

def mots_possibles_lettres(k):
    '''
    renvoie le tableau des mots de longueur k qui peuvent être rencontrés
    '''
    tabk = []
    for i in range(4**k):
        num = invCode(i,k)
        #print("num : ",num)
        tabk.append(transforme_en_lettre(num))
    return tabk

def mots_possibles(k):
    '''
    renvoie le tableau des entiers correspondant aux entiers possibles
    '''
    return [x for x in range(4**k)]

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
    nb_occurences(occur,sequence,mots,k)
    return occur

def comptage_attendu(k,mots,freq,nb):
    '''
    f : tuple contenant la frequence attendue de chaque lettre
    k : longueur du mot
    nb : nombre total de nucléotides dans la séquence
    '''
    dico = dict()
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
    comptage_att et comptage_obs sont des dictionnaires (mot, nombre d'occurences)
    '''

    freq = frequence_lettres(sequence)       # fréquence des lettres
    nbtotal = compte_nucleotide(sequence)           # occurences des nucléotides

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
    ax.plot(lim, lim)
    ax.set_xlabel("Nombre d'occurences attendu")
    ax.set_ylabel("Nombre d'occurences observe")
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

def simulation(tailleSequence, nombreSequence, frequenceDesLettres):
    L = []
    for i in range(nombreSequence):
        L.append(simule_sequence(tailleSequence,frequenceDesLettres))
    return L

def calcule_proba_empirique(k,liste_mot,listeSequence, frequence_lettres, tailleSequence):
    probaMot = [0,0,0,0]
    mots = mots_possibles(k)
    mots_lettres = mots_possibles_lettres(k)
    comptage_att = comptage_attendu(k,mots,frequence_lettres,tailleSequence)
    somme = 0
    for sequence in listeSequence:
        comptage_obs = comptage_observe(k,sequence,mots)
        for key in comptage_obs:
            for i in range(len(probaMot)):
                #si c'est un des mots recherché
                if liste_mot[i] == key:
                    probaMot[i] += comptage_obs[key]
                somme += comptage_obs[key]
    #cast
    somme = somme * 1.0
    for i in range(len(probaMot)):
        probaMot[i] = probaMot[i] / somme
    return probaMot
        
    #difference = [(x[i] - y[i]) for i in range(len(x))]
    #print(difference)

def histo_proba_mot(liste_mots, proba_mots):
    dico = dict((liste_mots[i], proba_mots[i]) for i in range(len(liste_mots)))
    fig, ax = plt.subplots()
    # a corriger
    ax.hist(dico.values())
    ax.set_ylim([min(proba_mots), max(proba_mots)])
    fig.show()



#print (frequence_lettres_genome(genome))
#print (sum(frequence_lettres_genome(genome)))
#sequence = [1,0,3]
#print(logprobafast(compte_lettres(sequence),(0.2,0.3,0.1,0.4)))
#s = simule_sequence(20,[0.2,0.3,0.1,0.4])
#print(s)
#print(frequence_lettres(s))

genome = lit_fasta("yeast_s_cerevisae_genomic_chr1-4.fna")
pho = lit_fasta("regulatory_seq_PHO.fasta")
gal = lit_fasta("regulatory_seqs_GAL.fasta")
met = lit_fasta("regulatory_seqs_MET.fasta")

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


liste_mots2 = ["ATCTGC", "ATATAT", "TTTAAA", "AAAAAA"]
liste_mots = []
k = len(liste_mots2[0])
for m in liste_mots2:
    liste_mots.append(code(transforme_en_nombre(m),len(m)))
print(liste_mots)
    
freq = frequence_lettres(pho)
liste_sequences = simulation(len(pho), 2, freq)
toto = calcule_proba_empirique(k,liste_mots, liste_sequences, freq, len(pho))
print(toto)
histo_proba_mot(liste_mots,toto)
