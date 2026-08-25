class User:
    def __init__(self, name, money):
        self.__name = name
        self.__money = money

    @property
    def name(self):
        return self.__name
    
    def add_money(self, money):
        self.__money += money


user1 = User("Gabriel", 43)
user2 = None

users = list(filter(None, [user1, user2]))

print(user1.name)
