
from pympler import asizeof
class Tree:
    def __init__(self,name,colour,texture):
        self.name = name
        self.colour = colour
        self.texture = texture

trees=[]

for i in range(100000):
    trees.append(Tree("Oak", "Green", "Rough"))



class TreeType:
    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

class Trees:
    def __init__(self, x, y, tree_type):
        self.x = x
        self.y = y
        self.tree_type = tree_type



oak = TreeType("Oak", "Green", "Rough")

forest = []

for i in range(100000):
    forest.append(Trees(i, i+5, oak))