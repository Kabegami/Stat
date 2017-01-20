import random
def de():
    return random.randint(1,6)

def proba_somme(k,n):
    L = []
    dico = dict()
    som = 0
    for i in range(n):
        for j in range(k):
            som += de()
        if som in dico:
            dico[som] += 1
        else:
            dico[som] = 1
        som = 0
    h = (float)(n)
    L = [(key,value/h) for key,value in dico.items()]
    return L 

L = proba_somme(1,1000)
print(L)
