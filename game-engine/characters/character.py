# base character class
class Character:
    def __init__(self, name, description, inventory, location, max_health):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.location = location
        self.max_health = max_health
        self.current_health = max_health
    
    def move(self, from_location, to_location):
        # to-do: check if there is a valid path between from_location and to_location; if so:
        self.location = to_location
        from_location.remove_character(self)
        to_location.add_character(self)

    def attack(self, target):
        # to-do: attack target
        pass

    def take_damage(self, damage):
        # to-do: take damage
        pass

    def heal(self, amount):
        # to-do: heal character
        pass

    def die(self):
        # to-do: character death
        pass

    def add_item(self, item):
        # to-do: add item to inventory
        pass

    def drop_item(self, item):
        # to-do: drop item from inventory, add to location's items
        pass

    def give_item(self, item, target):
        # to-do: give item from inventory to target
        pass