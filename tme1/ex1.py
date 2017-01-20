def moyenne(l):
    s = 0
    for i in l:
        s += i
    s = (float)(s)
    return (s/len(l))

def histo(l):
    dico = dict()
    for i in l:
        if i not in dico:
            dico[i] = 1
        else:
            dico[i] += 1
    return dico

def histo_trie(l):
    dico = histo(l)
    R = []
    L = dico.keys()
    L.sort()
    print(L)
    for i in L:
        print(i)
        print(dico[i])
        R.append((dico[i],i))
    return R

def histo_trie2(l):
    d = histo(l)
    rev_d = [(value, key) for key, value in d.items()]
    sorted_list = sorted(rev_d)
    return sorted_list

#main
L = [1,2,2,2,3,4,4]
d = histo(L)
L2 = histo_trie(L)
print(moyenne(L))
print(d)
print("L2 : {}".format(L2))
