import sys
import json
from characters.player import Player
from characters.character import Character
from locations.location import Location
from items.item import Item
from items.weapon import Weapon
from quests.quest import Quest
from openai import OpenAI
client = OpenAI(api_key="")

class Game():
    def __init__(self, player, items, characters, locations, quests):
        self.player = player
        self.items = items
        self.characters = characters
        self.locations = locations
        self.quests = quests

        with open("../game-engine/data/txt/parser_prompt_template.txt", "r") as file:
            self.prompt_template = file.read()

    def intro(self):
        # initalize inventory
        image_filenames = [item.image_filename for item in self.player.inventory]
        print(json.dumps({"type": "inventory-update", "inventory": image_filenames}))
        sys.stdout.flush()

        # load intro dialogue txt
        self.send_message({"type": "header-message", "message": "Introduction"})
        with open("../game-engine/data/txt/intro.txt", "r") as f:
            for line in f:
                self.send_message({"type": "story-message", "message": line.strip()})
        self.check_all_quests()  # unlocks the first quest

        # print overview of starting area
        self.send_message({"type": "system-message", "message": f"You are at {self.player.location.name}."})
        self.send_message({"type": "system-message", "message": f"{self.player.location.description}"})
        if self.player.location.characters:
            character_names = [character.name for character in self.player.location.characters if character != self.player]
            if character_names:
                self.send_message({"type": "system-message", "message": f"Characters in this location: {', '.join(character_names)}"})
        if self.player.location.items:
            item_names = [item.name for item in self.player.location.items]
            if item_names:
                self.send_message({"type": "system-message", "message": f"Items in this location: {', '.join(item_names)}"})
        self.send_message({"type": "system-message", "message": f"From here you can go: {', '.join(self.player.location.connecting_locations.keys())}"})

    def main_loop(self):
        while True:
            # get user input, feed into parser model
            command = sys.stdin.readline().strip()
            action = self.parse_command(command)

            # determine which predefined action based on output parse
            # look
            if action == "look":
                self.send_message({"type": "system-message", "message": f"You look around {self.player.location.name}."})
                self.send_message({"type": "system-message", "message": f"{self.player.location.description}"})

                if self.player.location.characters:
                    character_names = [character.name for character in self.player.location.characters if character != self.player]
                    if character_names:
                        self.send_message({"type": "system-message", "message": f"Characters in this location: {', '.join(character_names)}"})

                if self.player.location.items:
                    item_names = [item.name for item in self.player.location.items]
                    if item_names:
                        self.send_message({"type": "system-message", "message": f"Items in this location: {', '.join(item_names)}"})

                self.send_message({"type": "system-message", "message": f"From here you can go: {', '.join(self.player.location.connecting_locations.keys())}"})

            # move
            elif action.split()[0] == "move" and len(action.split()) > 1:
                direction = action.split()[1]
                current_location = self.locations[self.player.location.name]
                self.player.move(current_location, direction)

            # inventory
            elif action == "inventory":
                if self.player.inventory:
                    item_names = [item.name for item in self.player.inventory]
                    self.send_message({"type": "system-message", "message": f"Inventory: {', '.join(item_names)}"})
                else:
                    self.send_message({"type": "system-message", "message": "Your inventory is empty."})

            # get
            elif action.split()[0] == "get" and len(action.split()) > 1:
                item_name = action.split()[1]
                if item_name in self.items:
                    item = self.items[item_name]
                    self.player.add_item(item)
                else:
                    self.send_message({"type": "system-message", "message": f"The item '{item_name}' is not here."})

            # talk
            elif action.split()[0] == "talk" and len(action.split()) > 1:
                character_name = action.split()[1]
                if character_name.lower() in self.characters:
                    character = self.characters[character_name.lower()]
                    if character.location == self.player.location:

                        # initiate dialogue loop
                        if not character.dead:
                            self.send_message({"type": "system-message", "message": f"You speak with {character.name}."})
                            self.send_message({"type": "dialogue-window", "status": "initiate-dialogue", "character": character.name})
                            self.dialogue_loop(character)

                        else:
                            self.send_message({"type": "system-message", "message": f"{character.name} is dead."})
                    else:
                        self.send_message({"type": "system-message", "message": f"The character '{character_name}' is not here."})
                else:
                    self.send_message({"type": "system-message", "message": f"The character '{character_name}' is not here."})

            # attack
            elif action.split()[0] == "attack" and len(action.split()) > 1:
                character_name = action.split()[1].lower()
                weapon_name = action.split("with")[1].strip().lower() if "with" in action else None

                if character_name in self.characters:
                    character = self.characters[character_name]
                    if weapon_name:
                        if weapon_name in self.items and self.items[weapon_name] in self.player.inventory:
                            weapon = self.items[weapon_name]
                            self.player.attack(character, weapon)
                        else:
                            self.send_message({"type": "system-message", "message": f"The weapon '{weapon_name}' is not valid or not in your inventory."})
                    else:
                        self.player.attack(character)
                else:
                    self.send_message({"type": "system-message", "message": f"The character '{character_name}' is not here."})

            # use item

            # give item

            # unknown command
            else:
                self.send_message({"type": "system-message", "message": "That's not a valid command."})

            # check quest statuses after stdin
            self.check_all_quests()

    def parse_command(self, command):
        # parse command using parser model - return predefined action (get, look, etc.)
        prompt = self.prompt_template + f"\n\n{command}"

        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        parse = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                parse += chunk.choices[0].delta.content

        parse = (parse.strip().replace('`', '').replace('\n', ''))
        return parse or "null"

    def send_message(self, message):
        print(json.dumps(message))
        sys.stdout.flush()

    def check_all_quests(self):
        for quest in self.quests.values():
            # complete quest
            if quest.is_unlocked and not quest.is_completed and quest.check_conditions(self.quests, self.player, self.characters, "complete"):
                quest.complete()
                self.send_message({"type": "quest-complete", "name": f"{quest.name}", "description": f"{quest.description}"})
            # unlock quest
            if not quest.is_unlocked and quest.check_conditions(self.quests, self.player, self.characters, "unlock"):
                quest.unlock()
                self.send_message({"type": "quest-unlock", "name": f"{quest.name}", "description": f"{quest.description}"})

    def dialogue_loop(self, character):
        # initialize dialogue model with character prompt template, read from file
        #with open(f"../game-engine/data/txt/{character.name.lower()}_prompt_template.txt", "r") as file:
        #    character_prompt_template = file.read()

        # add additional game information to the character prompt template
        # to-do

        # continue speaking to character until dialogue window is closed by player or player ends conversation
        while True:
            # get user input, feed into dialogue model
            player_input = sys.stdin.readline().strip()

            # send player input to dialogue model and get output
            character_output = None #to-do

            # print model output
            #self.send_message({"type": "dialogue-message", "message": character_output})
            self.send_message({"type": "dialogue-message", "message": f"System echoing: {player_input}"}) # echo for testing

            # end dialogue - model outputs special token [END]
            if character_output == "[END]" or player_input == "[END]":
                self.send_message({"type": "dialogue-window", "status": "end-dialogue"})
                self.send_message({"type": "system-message", "message": f"You end the conversation with {character.name}."})
                break



if __name__ == "__main__":
    # define items - keep all keys lowercase
    all_items = {
        "amulet": Item(name="Amulet", description="A shiny amulet passed down from your ancestors", image_filename="amulet.png"),
        "sword": Weapon(name="Sword", description="A sharp sword", image_filename="sword.png", damage=10),
        "key": Item(name="Key", description="A key that unlocks a door", image_filename="key.png")
    }

    # define locations
    all_locations = {
        "the starting location": Location(name="the starting location", description="There's not much to do here, but it's certainly some kind of starting location.", items=[], characters=[]),
        "the end location": Location(name="the end location", description="There also isn't much to do here yet. The walls have two-toned scrolling checkerboard patterns covering them.", items=[all_items["sword"]], characters=[])
    }

    # define location connections
    all_locations["the starting location"].add_connection("north", all_locations["the end location"])
    all_locations["the end location"].add_connection("south", all_locations["the starting location"])

    # define NPCs - keep all keys lowercase
    all_characters = {
        "john": Character(name="John", description="A friendly villager", inventory=[all_items["key"]], location=all_locations["the starting location"], max_health=50),
    }

    # add NPCs to locations
    all_locations["the starting location"].add_character(all_characters["john"])

    # define player and initialize
    player = Player(name="Player", description="A wandering traveler", inventory=[all_items["amulet"]], location=all_locations["the starting location"], max_health=100)
    all_locations["the starting location"].add_character(player)

    # define quests
    all_quests = {
        "Defeat John": Quest(name="Defeat John", description="Defeat John", unlock_conditions={}, complete_conditions={"characters_dead": ["john"]}),
        #"Go North": Quest(name="Go North", description="This is a test quest", unlock_conditions={}, complete_conditions={"at_location": "the end location"}),
        #"Get Sword": Quest(name="Get Sword", description="This is another test quest", unlock_conditions={"completed_quests": ["Go North"]}, complete_conditions={"has_items": [all_items["sword"]]})
    }

    # start game
    game = Game(player=player, items=all_items, characters=all_characters, locations=all_locations, quests=all_quests)
    game.intro()
    game.main_loop()