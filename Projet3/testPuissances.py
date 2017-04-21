from nanowebs import *

nanoweb1 = creeNanoWeb1()
nanoweb1.trace(1, "epsilons_puissance1.txt")
puissance = nanoweb1.convergence_p(1000, 0.01)
print(puissance)

print("")
nanoweb2 = creeNanoWeb2()
nanoweb2.trace(1, "epsilons_puissance2.txt")
puissance = nanoweb2.convergence_p(50, 0.01)
print(puissance)

print("")
nanoweb3 = creeNanoWeb3()
nanoweb3.trace(1, "epsilons_puissance3.txt")
puissance = nanoweb3.convergence_p(1000, 0.01)
print(puissance)
