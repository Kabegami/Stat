import random
import matplotlib.pyplot as plt

def paquet():
    L = []
    motif = ["C","K","P","T"]
    for i in range(1,14):
        for j in motif:
            L.append((i,j))
    random.shuffle(L)
    return L

def meme_position(p,q):
    L = []
    for i in range(0,len(p)):
        if p[i] == q[i]:
            L.append(i)
    return L

def experience():
    print("debut experience")
    s = 0
    for i in range(0,100):
        L = paquet()
        L2 = paquet()
        L3 = meme_position(L,L2)
        s += len(L3)
    res = s / (100 * 52.0)
    print("resultat experience : {}".format(res))

def experience2():
    print("debut experience")
    s = 0
    R1 = []
    R2 = []
    for i in range(0,1000):
        L = paquet()
        L2 = paquet()
        L3 = meme_position(L,L2)
        R1.append(i)
        R2.append(len(L3)/52.0)
    return (R1,R2)

L = paquet()
L2 = paquet()
L3 = meme_position(L,L2)
#print(L)
#print(len(L))
print(L3)
experience()
x,y = experience2()
plt.plot(x,y,'bs')
plt.show()
