import sys
import json

# base character class
class Character:
    def __init__(self, name, description, inventory, location, max_health):
        self.name = name
        self.description = description
        self.inventory = inventory
        self.standing = 0
        self.messages = [
            {
              "role": "system",
              "content": [
                {
                  "type": "text",
                  "text": "You are a dialogue generator for a dark souls inspired adventure game based on the following story: A benevolent king and queen rule over the kingdom of Tridica. The land is a prosperous nation. For many years the king and queen tried to conceive but were unable to. After a decade, the queen finally became pregnant. The couple were happy until the queen suffered a miscarriage. The kingdom has historically been devout followers of their Goddess of Prosperity, Lenia. The king begins to become paranoid of those around him. His wife falls into a depression. He tries many times to create another heir but is unsuccessful. The king executes those around him, and he begins instating oppressive laws on the people. Civil unrest and financial ruin fall upon the kingdom of Tridica. The Lenian church leaders eventually confront the king and beg him to stop his descent into madness. Out of blind hate, the king executes the church leaders and puts their heads on stakes outside the castle. The king outlaws religion, and orders his soldiers to march throughout the capital, rounding up clergymen to be imprisoned. He also orders them out to the nearby countryside towns. Civil unrest breaks out throughout the kingdom. On the day of reckoning, an angel of Lenia, Rimor descended upon the throne room and condemned the king. He took the souls of all those within the castle, leaving them to become nightmarish ghouls. Rimor cursed the kingdom of Tridica that day. \"The children of Tridica have cried out to me in anguish. Their blood is on your hands and they will have their retribution. This day of reckoning will mark your dynasty's downfall.\" The main character is a humble peasant farmer who finishes burying two people in front of his house. He starts in a small village right outside the kingdom's gates. He's been marked by Rimor to be the chosen one who kills the king and ends the deathly curse upon the land. \nYou will take input in the format of [playerInput, playerStanding, characterSummary]. The playerInput will be a string which represents what the player's character is saying to the character you are generating dialogue for. characterSummary is a string containing the background for the character you are generating dialogue for, and the previous sentences in the conversation. playerStanding will be a numerical input between -100 and 100, which represents how much the character likes or dislikes the player.\nYou will provide output in the format of characterResponse$newStanding$newCharacterSummary. characterResponse is the character dialgoue you generate based on the player's input. If the conversation is over, or the character you are playing would end the conversation, end your dialgoue with \"[END]\". newCharacterSummary should be the original summary passed in, but with a summary of the current interaction appended. newStanding should be the standing updated to reflect if the interaction was positive or negative. Keep in mind that the standing doesn't always have to change.\nWhen generating dialogue, take events in the character summary into account. Also consider the players standing, as a negative standing should cause a negative attitude, and a positive standing should cause a positive attitude. Never respond without the $ characters between each reponse.\n"
                }
              ]
            }
        ]
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
            connecting_locations = [f"{direction} to {loc.name}" for direction, loc in to_location.connecting_locations.items()]
            print(json.dumps({"type": "system-message", "message": f"From here you can go: {', '.join(connecting_locations)}"}))
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
            target.inventory.append(item)
            self.inventory.remove(item)
            print(json.dumps({"type": "system-message", "message": f"{self.name} gave {target.name} their {item.name}."}))
            sys.stdout.flush()
        else:
            # only will happen when the player tries to give an item they don't have, npcs will have their own checks
            print(json.dumps({"type": "system-message", "message": f"You don't have any item '{item.name}'."}))
            sys.stdout.flush()