#-*- coding: utf-8 -*-

from sys import path
path.append('.')

from datastructures import SimpleWeb
from generation import Generateur
from internautes import Internaute
from simulation import Simulation
from random import randint
import timeit
import numpy as np
import matplotlib.pyplot as plt

def creeNanoWeb1():
    n = SimpleWeb(10)
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
    return n

def creeNanoWeb2():
    n = SimpleWeb(10)
    n.addArc(1, 0)
    n.addArc(1, 5)
    n.addArc(0, 9)
    n.addArc(9, 8)
    n.addArc(8, 7)
    n.addArc(7, 6)
    n.addArc(6, 5)
    n.addArc(5, 4)
    n.addArc(4, 3)
    n.addArc(3, 2)
    n.addArc(2, 4)
    n.addArc(9, 2)
    n.addArc(3, 7)
    n.addArc(2, 1)
    n.updateProbas()
    return n

def creeNanoWeb3():
    n = SimpleWeb(10)
    n.addArc(2, 0)
    n.addArc(2, 3)
    n.addArc(1, 2)
    n.addArc(1, 3)
    n.addArc(9, 1)
    n.addArc(6, 7)
    n.addArc(7, 6)
    n.addArc(7, 8)
    n.addArc(4, 5)
    n.addArc(5, 4)
    n.updateProbas()
    return n

def calcule_temps(nb_sommets):
    print("Nombre de sommets : {}".format(nb_sommets))
    res = []
    generator = Generateur(nb_sommets)
    graph = generator.genere()
    graph.trace(100, "epsilons_puissance")

    #### Internaute
    naute = Internaute(graph)
    pos = randint(0, nb_sommets-1)
    naute.trace(100, "epsilons_internaute")

    start = timeit.default_timer()
    naute.goTo(pos)
    naute.walk(1000, 0.001)
    end = timeit.default_timer()
    res.append(end-start)
    

    #### Simulation
    pi0 = np.zeros(nb_sommets)
    pi0[pos] = 1
    simu = Simulation(graph, pi0)
    simu.trace(100, "epsilons_simulation")

    start = timeit.default_timer();
    simu.calcule_piT(1000, 0.001)
    end = timeit.default_timer();
    res.append(end-start)

    
    #### Puissance
    start = timeit.default_timer();
    puissance = graph.convergence_p(1000, 0.001)
    end = timeit.default_timer()
    res.append(end-start)
    return res

def plot_calc(nb_max, step):
    res = []
    for i in range(10, nb_max, step):
        res.append(calcule_temps(i))

    res_internaute = []
    res_simulation = []
    res_puissances = []
    for r in res:
        res_internaute.append(r[0])
        res_simulation.append(r[1])
        res_puissances.append(r[2])
    x = np.arange(10, nb_max, step)
    plt.plot(x, res_internaute, label='internaute')
    plt.plot(x, res_simulation, label='simulation')
    plt.plot(x, res_puissances, label='puissances')
    plt.xlabel('Nombre de noeuds')
    plt.ylabel('Secondes')
    plt.title('Temps de calcul de l\'estimation de la distribution stationnaire')
    plt.legend(loc='best')
    plt.show()
    
if __name__== "__main__":
    '''
    n1=creeNanoWeb1()
    print(n1) #affichelarepresentationtexte
    n1.writeGraph("nano1.png") #creelarepresentationimag
    '''

    #n2=creeNanoWeb2()
    #print(n2) #affichelarepresentationtexte
    #n2.writeGraph("nano2.png") #creelarepresentationimag

    n3 = creeNanoWeb3()
    print(n3)
    n3.writeGraph("nano3.png")
    #plot_calc(1011, 10)
    #res = calcule_temps(1000)
    #print(res)
