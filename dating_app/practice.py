from abc import ABC, abstractmethod
from collections import UserList


class User():
    def __init__(self,id,name,age,interests,location):
        self.id =id
        self.name= name
        self.age = age
        self.interests = interests
        self.location = location

        self.likes = set()
        self.matches = set()

    def swipe_right(self,other_user):
        self.likes.add(other_user.id)

    def swipe_left(self,other_user):
        print(f"{self.name} skipped {other_user.name}")
    
    def add_match(self,other_user):
        self.matches.add(other_user.id)



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

    

class matching_strategy(ABC):
    @abstractmethod
    def match(self,user, users):
        pass

class normal_matching(matching_strategy):
    def match(self,user,users):
        for u in users:
             return [u for u in users if users.id != user.id]

class location_matching(matching_strategy):
    def match(self,user,users):
        for u in users:
             return [u for u in users if users.location == user.location and users.id != user.id]

class interest_matching(matching_strategy):
    
    def match(self,user,users):
        result =[]

        for others in users:
            if other.id == user.id:
                continue
            common = set(user.interests) & set(other.interests)

            if len(common)>=2:
                result.append(other)
        
        return result


        
        