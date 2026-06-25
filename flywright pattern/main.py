class Tree:
    def __init__(self,name,colour,texture):
        self.name = name
        self.colour = colour
        self.texture = texture

trees=[]

for i in range(100000):
    trees.append(Tree("Oak", "Green", "Rough"))