from generation import *
from datastructures import *
from nanowebs import creeNanoWeb1
from simulation import *
from internautes import Internaute

#---------------------------------------
# INTERNAUTE
#---------------------------------------

# creation du SimpleWeb
nanoweb = creeNanoWeb1()

# Bob se balade dans le nanoweb
bob = Internaute(nanoweb)

# bob est dans le noeud 3
bob.goTo(3)

bob.trace(10, "epsilons_internaute.txt")
bob.walk(1000, 0.001)
bob.showFrequencies()
print("\n")


#---------------------------------------
# SIMULATION
#---------------------------------------

pi0 = np.array([0,0,1,0,0,0,0,0,0,0])
print("etat initial : {}".format(pi0))
billy = Simulation(nanoweb,pi0)
billy.trace(10, "epsilons_simulation.txt")
v = billy.calcule_piT(1000, 0.001)
print(v)
print("\n")


#---------------------------------------
# PUISSANCES
#---------------------------------------

nanoweb.trace(1, "epsilons_puissance.txt")
puissance = nanoweb.convergence_p(1000, 0.001)
print(puissance)
print("\n")

#---------------------------------------
# GENERATEUR
#---------------------------------------

'''
generator = Generateur(6)
g = generator.genere()
g.writeGraph("test.png")
'''
