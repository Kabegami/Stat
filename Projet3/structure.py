import numpy as np

class SimpleWeb(object):
    def __init__(self, nombreSommet):
        """ on crée des noeuds lors de l'initialisation"""
        self.nombreSommet = nombreSommet
        self.listeSommet = []
        for i in range(0,nombreSommet):
            n = Node(i)
            self.listeSommet.append(n)
        self.matriceProba = np.zeros((nombreSommet, nombreSommet))

        
    def addArc(self,id_n1,id_n2):
        """ id_n1(tail) : int, id_n2(head) : int -> ajoute les arc aux sommets référencés"""
        if id_n1 == id_n2:
            raise Exception("meme noeud")
        n1 = self.listeSommet[id_n1]
        n2 = self.listeSommet[id_n2]
        #print("on ajoute un arc de {} vers {}".format(n1,n2))
        a = Arc(id_n1,id_n2)
        n2.ajoute_arc_entrant(a)
        n1.ajoute_arc_sortant(a)
        self.updateProbas()

    def updateProbas(self):
        """ on parcours tout les noeuds et incremente a partir des arc_entrant"""
        for i in range(0,self.nombreSommet):
            n = self.listeSommet[i]
            for arc in n.arcSortant:
                head = arc.head
                tail = arc.tail
                arc.p = 1 / (len(n.arcSortant)*1.0)
                self.matriceProba[tail][head] = arc.p

    def __str__(self):
        s =  "MatriceProba : {} \n".format(self.matriceProba)
        for i in range(self.nombreSommet):
            n = self.listeSommet[i]
            if not(n.arcSortant_vide()):
                s += n.__str__()
        return s
    
    def writeGraph(fichier,g):
        """ g est un graphe de la classe graphviz qu'on va appelé pour la construction"""
        g.node("bla bla bla")
        
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
    def __init__(self,tail, head,p=0):
        self.tail = tail
        self.head = head
        self.p = p

    def __str__(self):
        return "Arc du noeud : {} vers le noeud {} avec une probabilité : {}".format(self.tail, self.head,self.p)
        

G = SimpleWeb(10)
G.addArc(0,1)
G.addArc(0,2)
G.addArc(1,3)
G.addArc(5,4)
G.addArc(2,6)
G.addArc(6,4)
G.addArc(4,2)
G.addArc(9,4)
#G.updateProbas()
print(G)
