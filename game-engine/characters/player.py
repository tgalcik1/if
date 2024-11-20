from characters.character import Character

class Player(Character):
    def __init__(self, name, description, inventory, location, max_health):
        super().__init__(name, description, inventory, location, max_health)
        self.experience = 0
        self.level = 1
        self.gold = 0
        