from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from internautes import Internaute

# creation du SimpleWeb
nanoweb = creeNanoWeb1()

# Bob se balade dans le nanoweb
bob = Internaute(nanoweb)

# bob est dans le noeud 3
bob.goTo(3)

bob.trace(10, "epsilons.txt")
bob.walk(10000, 0.01)
bob.showFrequencies()

# question 6
# epsilon = d(pi,pi+1)
# notre epsilon prend la valeur absolue 
