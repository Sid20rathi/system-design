from abc import ABC, abstractmethod


class User():
    def __init__(self,id,name,age,interests,location):
        self.user_id =id
        self.name= name
        self.age = age
        self.interests = interests
        self.location = location

        self.likes = set()
        self.matches = set()

    def swipe_right(self,other_user):
        self.likes.add(other_user.user_id)

    def swipe_left(self,other_user):
        print(f"{self.name} skipped {other_user.name}")
    
    def add_match(self,other_user):
        self.matches.add(other_user.user_id)



class observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class UserNotificationService(observer):
    def __init__(self, user):
        self.user = user
        
    def update(self, message):
        print(f"[Notification to {self.user.name}] {message}")
        
class notification:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls) # without this line , object will not be created
            cls._instance.observers = {}
        return cls._instance

    def subscribe(self, user_id, observer):
        self.observers[user_id] = observer

    def notify(self, user_id, message):
        if user_id in self.observers:
            self.observers[user_id].update(message)

    

    
        