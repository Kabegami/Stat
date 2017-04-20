from sys import path
path.append('.')

from nanowebs import *
from simulation import *


nanoweb1 = creeNanoWeb1()
pi0 = np.array([0,0,1,0,0,0,0,0,0,0])
print("etat initial : {}".format(pi0))
billy = Simulation(nanoweb1,pi0)
billy.trace(10, "epsilons_simu1.txt")
v = billy.calcule_piT(1000, 0.01)
print(v)

print("")
nanoweb2 = creeNanoWeb2()
pi0 = np.array([1,0,0,0,0,0,0,0,0,0])
print("etat initial : {}".format(pi0))
billy = Simulation(nanoweb2,pi0)
billy.trace(10, "epsilons_simu2.txt")
v = billy.calcule_piT(1000, 0.01)
print(v)

print("")
nanoweb3 = creeNanoWeb3()
pi0 = np.array([0,0,0,0,0,0,0,0,0,1])
print("etat initial : {}".format(pi0))
billy = Simulation(nanoweb3,pi0)
billy.trace(1, "epsilons_simu3.txt")
v = billy.calcule_piT(1000, 0.01)
print(v)


