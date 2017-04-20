from sys import path
path.append('.')

from nanowebs import *
from internautes import Internaute

# creation du SimpleWeb
nanoweb1 = creeNanoWeb1()

# Bob se balade dans le nanoweb
bob = Internaute(nanoweb1)

# bob est dans le noeud 3
bob.goTo(3)

bob.trace(1, "epsilons_internaute1.txt")
bob.walk(1000, 0.01)
bob.showFrequencies()

print("")
nanoweb2 = creeNanoWeb2()
bob = Internaute(nanoweb2)
bob.trace(1, "epsilons_internaute2.txt")
bob.goTo(0)
bob.walk(1000, 0.01)
bob.showFrequencies()

print("")
nanoweb3 = creeNanoWeb3()
bob = Internaute(nanoweb3)
bob.trace(1, "epsilons_internaute3.txt")
bob.goTo(9)
bob.walk(1000, 0.01)
bob.showFrequencies()
