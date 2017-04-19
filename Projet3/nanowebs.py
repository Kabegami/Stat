#-*- coding: utf-8 -*-

from sys import path
path.append('.')

from datastructures import SimpleWeb
from generation import Generateur
from internautes import Internaute
from random import randint


def creeNanoWeb1():
    n=SimpleWeb(10)
    n.addArc(0,1)
    n.addArc(0,4)
    n.addArc(1,2)
    n.addArc(2,3)
    n.addArc(2,4)
    n.addArc(3,9)
    n.addArc(4,2)
    n.addArc(4,5)
    n.addArc(4,7)
    n.addArc(5,6)
    n.addArc(6,5)
    n.addArc(6,7)
    n.addArc(7,8)
    n.addArc(8,7)
    n.addArc(9,2)
    n.updateProbas()
    return n;

def calcule_temps():
    generator = Generateur(20)
    graph = generator.genere()

    #### Internaute
    naute = Internaute(graph)
    pos = randint(0, 20)
    naute.goTo(pos)
    

if __name__== "__main__":
    n1=creeNanoWeb1()
    print(n1) #affichelarepresentationtexte
    n1.writeGraph("nano1.png") #creelarepresentationimag
