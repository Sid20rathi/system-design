## we are building a lld of dating app



from abc import ABC , abstractmethod

class User:
    def __init__(self,id,name,age,interests,location):
        self.user_id =id
        self.name= name
        self.age = age
        self.interests = interests
        self.location = location

        self.likes = set()
        self.matches = set()

    def swipe_right(self, other_user):
        self.likes.add(other_user.user_id)

    def swipe_left(self, other_user):
        print(f"{self.name} skipped {other_user.name}")

    def add_match(self, other_user):
        self.matches.add(other_user.user_id)

    def __repr__(self):
        return f"User({self.name})"





class Observer(ABC):

    @abstractmethod
    def update(self, message):
        pass



class UserNotificationObserver(Observer):

    def __init__(self, user):
        self.user = user

    def update(self, message):
        print(f"[Notification to {self.user.name}] {message}")
    

class NotificationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.observers = {}
        return cls._instance

    def subscribe(self, user_id, observer):
        self.observers[user_id] = observer

    def notify(self, user_id, message):
        if user_id in self.observers:
            self.observers[user_id].update(message)



class MatchingStrategy(ABC):

    @abstractmethod
    def match(self, user, users):
        pass


class BasicMatchingStrategy(MatchingStrategy):

    def match(self, user, users):
        return [u for u in users if u.user_id != user.user_id]


class InterestBasedStrategy(MatchingStrategy):

    def match(self, user, users):

        result = []

        for other in users:
            if other.user_id == user.user_id:
                continue

            common = set(user.interests) & set(other.interests)

            if len(common) >= 2:
                result.append(other)

        return result


class LocationBasedStrategy(MatchingStrategy):

    def match(self, user, users):

        result = []

        for other in users:

            if other.user_id == user.user_id:
                continue

            if user.location == other.location:
                result.append(other)

        return result



class MatchStrategyFactory:

    @staticmethod
    def create_strategy(strategy_type):

        if strategy_type == "basic":
            return BasicMatchingStrategy()

        elif strategy_type == "interest":
            return InterestBasedStrategy()

        elif strategy_type == "location":
            return LocationBasedStrategy()

        raise ValueError("Invalid strategy")



class MatchEngine:

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def find_matches(self, user, users):
        return self.strategy.match(user, users)


class Message:

    def __init__(self, sender, receiver, text):
        self.sender = sender
        self.receiver = receiver
        self.text = text


class ChatRoom:

    def __init__(self, user1, user2):
        self.users = {user1.user_id, user2.user_id}
        self.messages = []

    def send_message(self, sender, receiver, text):

        message = Message(sender, receiver, text)
        self.messages.append(message)

        print(f"{sender.name} -> {receiver.name}: {text}")




class DatingApp:

    def __init__(self):

        self.users = {}

        self.notification_service = NotificationService()

        strategy = MatchStrategyFactory.create_strategy("interest")

        self.match_engine = MatchEngine(strategy)

        self.chat_rooms = {}

    def register_user(self, user):

        self.users[user.user_id] = user

        observer = UserNotificationObserver(user)

        self.notification_service.subscribe(user.user_id, observer)

    def discover_matches(self, user_id):

        user = self.users[user_id]

        return self.match_engine.find_matches(
            user,
            list(self.users.values())
        )

    def swipe_right(self, user_id, target_id):

        user = self.users[user_id]
        target = self.users[target_id]

        user.swipe_right(target)

        self.notification_service.notify(
            target.user_id,
            f"{user.name} liked your profile!"
        )

        # Mutual Like = Match
        if user.user_id in target.likes:

            user.add_match(target)
            target.add_match(user)

            self.notification_service.notify(
                user.user_id,
                f"You matched with {target.name}"
            )

            self.notification_service.notify(
                target.user_id,
                f"You matched with {user.name}"
            )

            room_key = tuple(sorted([user.user_id, target.user_id]))

            self.chat_rooms[room_key] = ChatRoom(user, target)

    def send_message(self, sender_id, receiver_id, text):

        room_key = tuple(sorted([sender_id, receiver_id]))

        if room_key not in self.chat_rooms:
            raise Exception("Users are not matched")

        sender = self.users[sender_id]
        receiver = self.users[receiver_id]

        room = self.chat_rooms[room_key]

        room.send_message(sender, receiver, text)

        self.notification_service.notify(
            receiver.user_id,
            f"New message from {sender.name}"
        )



if __name__ == "__main__":

    app = DatingApp()

    u1 = User(
        1,
        "Siddhant",
        24,
        ["music", "coding", "travel"],
        "Delhi"
    )

    u2 = User(
        2,
        "Riya",
        23,
        ["coding", "travel", "movies"],
        "Delhi"
    )

    u3 = User(
        3,
        "Ananya",
        25,
        ["fitness", "music"],
        "Mumbai"
    )

    app.register_user(u1)
    app.register_user(u2)
    app.register_user(u3)

    matches = app.discover_matches(1)

    print(matches)

    app.swipe_right(1, 2)
    app.swipe_right(2, 1)

    app.send_message(1, 2, "Hey there!")