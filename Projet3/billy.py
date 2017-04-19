from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from simulation import *

nanoweb = creeNanoWeb1()
pi0 = np.array([0,0,1,0,0,0,0,0,0,0])
print("etat initial : {}".format(pi0))
billy = Simulation(nanoweb,pi0)
billy.trace(100, "epsilons_piT")
v = billy.calcule_piT(1000, 0.001)
print(v)

nanoweb.trace(1, "epsilons_puissance")
puissance = nanoweb.convergence_p(100, 0.01)
print(puissance)
