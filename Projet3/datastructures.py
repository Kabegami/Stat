#-*- coding: utf-8 -*-

import numpy as np
import pydotplus.graphviz as gv

class SimpleWeb(object):
    def __init__(self, nombreSommet):
        """ on crée des noeuds lors de l'initialisation"""
        self.nombreSommet = nombreSommet
        self.listeSommet = []
        self.arcExistant = set()
        for i in range(0,nombreSommet):
            n = Node(i)
            self.listeSommet.append(n)
        self.matriceProba = np.zeros((nombreSommet, nombreSommet))
        self.nb_pas = None
        self.fichier = None

        
    def addArc(self,id_n1,id_n2):
        """ id_n1(tail) : int, id_n2(head) : int -> ajoute les arc aux sommets référencés"""
        if id_n1 == id_n2:
            raise Exception("meme noeud")
        if (id_n1, id_n2) in self.arcExistant:
            raise Exception("l'arc existe deja")
        self.arcExistant.add((id_n1,id_n2))
        n1 = self.listeSommet[id_n1]
        n2 = self.listeSommet[id_n2]
        #print("on ajoute un arc de {} vers {}".format(n1,n2))
        a = Arc(id_n1,id_n2)
        n2.ajoute_arc_entrant(a)
        n1.ajoute_arc_sortant(a)
        self.updateProbas()

    def updateProbas(self):
        """ on parcourt tous les noeuds et incremente a partir des arcs entrants"""
        for i in range(0,self.nombreSommet):
            n = self.listeSommet[i]
            #le noeud n'a aucun arc
            if len(n.arcSortant) == 0:
                self.matriceProba[i][i] = 1
            #si il a un nouvelle arc, on supprime l'arc pointant vers lui meme
            if len(n.arcSortant) == 1 and self.matriceProba[i][i] == 1:
                self.matriceProba[i][i] = 0
            for arc in n.arcSortant:
                head = arc.head
                tail = arc.tail
                arc.proba = 1 / (len(n.arcSortant)*1.0)
                self.matriceProba[tail][head] = arc.proba

    def __str__(self):
        s =  "MatriceProba : {} \n".format(self.matriceProba)
        for i in range(self.nombreSommet):
            n = self.listeSommet[i]
            if not(n.arcSortant_vide()):
                s += n.__str__()
        return s
    
    def writeGraph(self, fichier):
        ''' fichier : nom du fichier dans le repertoire courant '''
        graph = gv.Dot(graph_type='digraph')
        for node in self.listeSommet:
            graph.add_node(gv.Node(node.id_node))
        for node in self.listeSommet:
            for arc in node.arcSortant:
                graph.add_edge(gv.Edge(node.id_node, arc.head, label=arc.proba))
        graph.write_png(fichier)

    def nextStep(self,pi_t):
        """ np.array -> np.array"""
        return np.dot(pi_t,self.matriceProba)

    def convergence_p(self, iterMax, seuil):
        """ p : matriceProba"""
        matricePuissante = self.matriceProba
        cpt = 0
        epsilon = 1
        while epsilon > seuil and cpt < iterMax:
            newPuissance = np.dot(matricePuissante, matricePuissante)
            dif = abs(matricePuissante - newPuissance)
            epsilon = np.amax(dif)
            if self.nb_pas != None and self.fichier != None:
                if cpt % self.nb_pas == 0 and cpt != 0:
                    self.ecrit(cpt, epsilon)
                    #print("epsilon : {}".format(epsilon))
            matricePuissante = newPuissance
            cpt += 1
            
        #print("\n------- PUISSANCES -------")
        #print("iterations : {}".format(cpt))
        #print("epsilon : {}\n".format(epsilon))
        return matricePuissante

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
        
class Node(object):
    def __init__(self,id_node):
        """ int * Arc[] * Arc[] -> void  
        si un noeud n'a pas d'arc sortant, on place un arc vers lui meme avec une proba 1 """
        self.arcSortant = []
        self.arcEntrant = []
        self.id_node = id_node

    def arcSortant_vide(self):
        if self.arcSortant == []:
            return True
        return False

    def ajoute_arc_sortant(self,arc):
        self.arcSortant.append(arc)

    def ajoute_arc_entrant(self,arc):
        self.arcEntrant.append(arc)

    def __str__(self):
        s =  "Noeud numero : {} \n ".format(self.id_node)
        #print("liste des arc sortant : ",self.arcSortant)
        if self.arcSortant != []:
            s += "Arc sortant : \n"
            for arc in self.arcSortant:
                s += '\t' + arc.__str__() + '\n'
        return s

class Arc(object):
    def __init__(self,tail, head, proba=0):
        self.tail = tail
        self.head = head
        self.proba = proba

    def __str__(self):
        return "Arc du noeud : {} vers le noeud {} avec une probabilité : {}".format(self.tail, self.head,self.proba)
