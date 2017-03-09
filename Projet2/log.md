*Jeudi 09/03/2017*

**Q3.1.3**

A partir de k = 6, il commence à y avoir des motifs qui n'apparaissent pas dans la séquence. On peut donc avoir `len(attendu) > len(observe)`.

* *Modification de `nb_occurences()`*

Passage en paramètre du tableau d'occurences des mots possibles, et renvoie le dictionnaire dont les clés sont les entiers-mot.

* *Renommage de `construit_tabk()` en `mots_possibles()`*

La fonction retourne un tableau d'entiers, un entier correspondant à un mot (donc dans l'intervalle [0, 4^k - 1]).