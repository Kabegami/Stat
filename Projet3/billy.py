from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from simulation import *

nanoweb = creeNanoWeb1()
#pi0 = nanoweb.matriceProba[0]
pi0 = np.array([1,0,0,0,0,0,0,0,0,0])
print(pi0)
billy = Simulation(nanoweb,pi0)
v = billy.calcule_piT(0.01,1000)
print(v)
puissance = nanoweb.convergence_p(0.01,1000)
print("pupupissance : {}".format(puissance))
