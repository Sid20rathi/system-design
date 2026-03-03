from abc import ABC ,abstractmethod


class Beverage(ABC):

    def prepare(self):
        self.boil_water()
        self.brew()
        self.pouring()
        self.add()
    
    def boil_water(self):
        print("adding water")
    
    @abstractmethod
    def brew():
        pass

    def pouring(self):
        print("pouring....")

    @abstractmethod
    def add(self):
        pass



class Tea(Beverage):

    def brew(self):
        print("brewiing tea")

    def add(self):
        print("adding tea leaves")


class Coffee(Beverage):
    def brew(self):
        print("brewing coffeeee..........")

    def add(self):
        print("adding coffe beans and milk")


Tea = Tea()
Tea.prepare()

print("==================================")


Coffe = Coffee()
Coffe.prepare()

