class Player:
    def __init__(self):
        self.__coins = 100

    @property
    def get_coins(self):
        return self.__coins

    def increase_coins(self, amount):
        self.__coins += amount

    def decrease_coins(self, amount):
        self.__coins -= amount
