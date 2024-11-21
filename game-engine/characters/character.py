import sys
import json

# base character class
class Character:
    def __init__(self, name, description, inventory, location, max_health):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.location = location
        self.max_health = max_health
        self.current_health = max_health
    
    def move(self, from_location, direction):
        if direction in from_location.connecting_locations:
            to_location = from_location.connecting_locations[direction]
            from_location.remove_character(self)
            to_location.add_character(self)
            self.location = to_location

            print(json.dumps({"type": "system-message", "message": f"You move to {to_location.name}."}))
            sys.stdout.flush()

            # print location description
            print(json.dumps({"type": "system-message", "message": f"{to_location.description}"}))
            sys.stdout.flush()

            # print connecting locations
            print(json.dumps({"type": "system-message", "message": f"From here you can go: {', '.join(to_location.connecting_locations.keys())}"}))
            sys.stdout.flush()

        else:
            print(json.dumps({"type": "system-message", "message": "You can't go that way."}))
            sys.stdout.flush()


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