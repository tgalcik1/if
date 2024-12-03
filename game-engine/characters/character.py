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
        self.base_damage = 1
        self.dead = False
    
    def move(self, from_location, direction):
        # only the player will be moving for now, so these messages are ok to refer to the player
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
            if self.location.items:
                item_names = [item.name for item in self.location.items]
                if item_names:
                    print(json.dumps({"type": "system-message", "message": f"Items in this location: {', '.join(item_names)}"}))
            if self.location.characters:
                character_names = [character.name for character in self.location.characters if character != self]
                if character_names:
                    print(json.dumps({"type": "system-message", "message": f"Characters in this location: {', '.join(character_names)}"}))

            # print connecting locations
            print(json.dumps({"type": "system-message", "message": f"From here you can go: {', '.join(to_location.connecting_locations.keys())}"}))
            sys.stdout.flush()

        else:
            print(json.dumps({"type": "system-message", "message": "You can't go that way."}))
            sys.stdout.flush()


    def attack(self, target, weapon=None):
        # some of these conditions will only occur when called by the player in invalid situations
        # will handle these same checks for NPC attack behavior separately so it doesn't print the error messages
        if target in self.location.characters and not target.dead:
            if weapon is None:
                print(json.dumps({"type": "system-message", "message": f"{self.name} attacks {target.name}."}))
                sys.stdout.flush()
                target.take_damage(self.base_damage)
            else:
                print(json.dumps({"type": "system-message", "message": f"{self.name} attacks {target.name} with their {weapon.name}."}))
                sys.stdout.flush()
                target.take_damage(weapon.damage * self.base_damage)
        else:
            if target.dead:
                print(json.dumps({"type": "system-message", "message": f"{target.name} is already dead."}))
                sys.stdout.flush()
            else:
                print(json.dumps({"type": "system-message", "message": f"The character '{target.name}' is not here."}))
                sys.stdout.flush()

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health <= 0:
            self.die()
        else:
            print(json.dumps({"type": "system-message", "message": f"{self.name} takes {damage} damage."}))
            sys.stdout.flush()

    def heal(self, amount):
        # to-do: heal character
        pass

    def die(self):
        self.dead = True
        print(json.dumps({"type": "system-message", "message": f"{self.name} has died."}))
        sys.stdout.flush()

        # drop all items
        for item in self.inventory:
            self.drop_item(item)

        self.location.remove_character(self)

    def add_item(self, item):
        if item in self.location.items:
            self.inventory.append(item)
            self.location.items.remove(item)
            print(json.dumps({"type": "system-message", "message": f"You picked up {item.name}."}))
            sys.stdout.flush()

            # if the player was the one who picked up the item, print the new inventory
            if self.name == "Player":
                image_filenames = [item.image_filename for item in self.inventory]
                print(json.dumps({"type": "inventory-update", "inventory": image_filenames}))
                sys.stdout.flush()
        else:
            print(json.dumps({"type": "system-message", "message": f"The item '{item.name}' is not here."}))
            sys.stdout.flush()

    def drop_item(self, item):
        self.inventory.remove(item)
        self.location.add_item(item)
        print(json.dumps({"type": "system-message", "message": f"{self.name} dropped their {item.name}."}))
        sys.stdout.flush()

    def give_item(self, item, target):
        if item in self.inventory:
            target.add_item(item)
            self.inventory.remove(item)
            print(json.dumps({"type": "system-message", "message": f"{self.name} gave {target.name} their {item.name}."}))
            sys.stdout.flush()
        else:
            # only will happen when the player tries to give an item they don't have, npcs will have their own checks
            print(json.dumps({"type": "system-message", "message": f"You don't have any item '{item.name}'."}))
            sys.stdout.flush()