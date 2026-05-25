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
        
        