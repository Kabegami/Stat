*Jeudi 09/03/2017*

**Q3.1.3**

A partir de k = 6, il commence à y avoir des motifs qui n'apparaissent pas dans la séquence. On peut donc avoir `len(attendu) > len(observe)`.

* *Modification de `nb_occurences()`*

  	Prend en paramètre le tableau des mots possibles pour prendre en compte le fait l'absence dans la séquence. Dans ce cas, on ajoute 0 au dictionnaire d'occurences pour ce mot.

* *Renommage de `construit_tabk()` en `mots_possibles()`*