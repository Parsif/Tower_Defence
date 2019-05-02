class Player:
    def __init__(self):
        self.__coins = 100

    @property
    def get_coins(self):
        return self.__coins

    def set_coins_default(self):
        self.__coins = 500

    def increase_coins(self, amount):
        self.__coins += amount

    def decrease_coins(self, amount):
        self.__coins -= amount
