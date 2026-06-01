class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.location = None

    def __str__(self):
        return f"User(name={self.name}, age={self.age}, location={self.location})"



class UserBuilder():
    def __init__(self):
        self.user = User()
    
    def set_name(self,name):
        self.user.name= name
        return self
    
    def set_age(self,age):
        self.user.age = age
        return self
    
    def set_location(self,location):
        self.user.location = location
        return self

    
    def build(self):
        return self.user


builder = UserBuilder()
user = builder.set_name("Siddhant").set_age(25).set_location("New York").build()
print(user)
    
        
