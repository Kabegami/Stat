from generation import *
from datastructures import *

generator = Generateur(6)
g = generator.genere()
g.writeGraph("test.png")
