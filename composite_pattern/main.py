from abc import ABC ,abstractmethod

 
class filesystem(ABC):

    @abstractmethod
    def show(self,indent=0):
        pass


class File(filesystem):
    def __init__(self,name):
        self.name = name
    
    def show(self,indent=0):
        print(" "*indent ,f"file:{self.name}")
    
class Folder(filesystem):
    def __init__(self,name):
        self.name = name
        self.children=[]

    def add(self,component):
        self.children.append(component)\
    
    def show(self,indent=0):
        print(" "*indent+f"folder: {self.name}")
        for child in self.children:
            child.show(indent+4)

root = Folder("root")
file1 = File("file1")
file2 = File("file2")
file3 = File("file3")

sub1 = Folder("sub1")

sub1.add(file3)

root.add(file1)
root.add(file2)
root.add(sub1)

root.show()

