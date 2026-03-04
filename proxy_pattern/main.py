from abc import ABC , abstractmethod


#1 virtual proxy 


class Image(ABC):
    @abstractmethod
    def display(self):
        pass

class RealImage(Image):
    def __init__(self,name):
        self.image_name = name
        self.load_disk()

    def load_disk(self):
        print(f"Loading {self.image_name} from disk")

    def display(self):
        print(f"displaying the Imgae:{self.image_name}")


class proxy_image(Image):
    def __init__(self,name):
        self.real_image = None
        self.name = name
    

    def display(self):
        if self.real_image is None:
            self.real_image = RealImage(self.name)
        
        self.real_image.display()



siddhant = proxy_image("new pic")

siddhant.display()

print("------------------")

siddhant.display()
