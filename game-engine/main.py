import sys
import time
import json
from characters.player import Player
from characters.character import Character
from locations.location import Location
from items.item import Item
from items.weapon import Weapon
from quests.quest import Quest
from openai import OpenAI

def load_api_key(filepath):
    try:
        with open(filepath, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: API key file '{filepath}' not found.")
        sys.stdout.flush()
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the API key file: {e}")
        sys.stdout.flush()
        sys.exit(1)

api_key_file = "../api_key.txt"
api_key = load_api_key(api_key_file)

client = OpenAI(api_key=api_key)

class Game():
    def __init__(self, player, items, characters, locations, quests):
        self.player = player
        self.items = items
        self.characters = characters
        self.locations = locations
        self.quests = quests

        # blocks
        self.blocked_paths = {
            "the castle gate watch tower": {
                "down": {"location_name": "the city square of tridica", "quest": "Convince the Guard"}
            },
            "the city square of tridica": {
                "right": {"location_name": "the marketplace", "quest": "Defeat the Executioner"},
                "down": {"location_name": "the castle hall", "quest": "Defeat the Executioner"}
            },
            "the dining hall": {
                "down": {"location_name": "the dungeon", "quest": "Unlock the Storage Room"}
            },
            "the dragon statue shrine": {
                "right": {"location_name": "the alchemist's laboratory", "quest": "Unlock the Dragon"}
            }
        }

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
        self.send_map_update()

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
        self.send_message({"type": "system-message", "message": f"From here you can go: {', '.join([f'{direction} to {loc.name}' for direction, loc in self.player.location.connecting_locations.items()])}"})

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

                self.send_message({"type": "system-message", "message": f"From here you can go: {', '.join([f'{direction} to {loc.name}' for direction, loc in self.player.location.connecting_locations.items()])}"})

            # move
            elif action.split()[0] == "move" and len(action.split()) > 1:
                direction = action.split()[1]
                current_location = self.locations[self.player.location.name.lower()]

                # check for blocks
                if not self.is_path_available(current_location, direction):
                    self.send_message({"type": "system-message", "message": "That way is blocked."})
                else:
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
                item_name = " ".join(action.split()[1:])
                if item_name in self.items:
                    item = self.items[item_name]
                    self.player.add_item(item)
                else:
                    self.send_message({"type": "system-message", "message": f"The item '{item_name}' is not here."})

            # talk
            elif action.split()[0] == "talk" and len(action.split()) > 1:
                character_name = " ".join(action.split()[1:])
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
                character_name = " ".join(action.split()[1:action.split().index("with")]).lower() if "with" in action else " ".join(action.split()[1:]).lower()
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
            elif action.split()[0] == "give" and len(action.split()) > 1:
                item_name = " ".join(action.split()[1:action.split().index("to")])
                character_name = " ".join(action.split()[action.split().index("to")+1:])

                if item_name in self.items:
                    item = self.items[item_name]
                    if character_name in self.characters:
                        character = self.characters[character_name]
                        self.player.give_item(item, character)
                    else:
                        self.send_message({"type": "system-message", "message": f"The character '{character_name}' is not here."})
                else:
                    self.send_message({"type": "system-message", "message": f"The item '{item_name}' is not in your inventory."})

            # unknown command
            else:
                self.send_message({"type": "system-message", "message": "That's not a valid command."})

            # check quest statuses after stdin
            self.check_all_quests()

            # send map update after stdin
            self.send_map_update()

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

    def send_map_update(self):
        locations = {key.lower(): {"name": loc.name} for key, loc in self.locations.items()}
        connections = [
            {"source": loc.name.lower(), "target": target.name.lower()}
            for loc in self.locations.values()
            for direction, target in loc.connecting_locations.items()
        ]
        player_location = self.player.location.name.lower()
        self.send_message({
            "type": "map-update",
            "locations": locations,
            "connections": connections,
            "player_location": player_location
        })

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

        self.update_blocked_paths()

    def update_blocked_paths(self):
        for location_name, directions in self.blocked_paths.items():
            loc = self.locations[location_name]
            for direction, data in directions.items():
                quest_name = data["quest"]
                target_location_name = data["location_name"]
                if quest_name.lower() in [q.lower() for q in self.quests.keys()] and self.quests[quest_name].is_completed:
                    target_loc = self.locations[target_location_name]
                    if direction not in loc.connecting_locations or loc.connecting_locations[direction].name.lower() != target_location_name:
                        loc.add_connection(direction, target_loc)

                        # add reverse direction
                        reverse_dir = self.get_reverse_direction(direction)
                        if reverse_dir and reverse_dir not in target_loc.connecting_locations:
                            target_loc.add_connection(reverse_dir, loc)

    def get_reverse_direction(self, direction):
        reverse_map = {"up": "down", "down": "up", "left": "right", "right": "left"}
        return reverse_map.get(direction, None)

    def is_path_available(self, current_location, direction):
        loc_name = current_location.name.lower()
        if direction in current_location.connecting_locations:
            return True
        else:
            if loc_name in self.blocked_paths and direction in self.blocked_paths[loc_name]:
                quest_name = self.blocked_paths[loc_name][direction]["quest"]
                if self.quests[quest_name].is_completed:
                    return True
            return False

    def get_available_directions(self, location):
        directions = []
        for d in location.connecting_locations.keys():
            directions.append(d)

        loc_name = location.name.lower()
        if loc_name in self.blocked_paths:
            for d, data in self.blocked_paths[loc_name].items():
                quest_name = data["quest"]
                if self.quests[quest_name].is_completed:
                    if d not in directions:
                        directions.append(d)

        return directions

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

            if player_input == "[END]":
                self.send_message({"type": "dialogue-window", "status": "end-dialogue"})
                self.send_message({"type": "system-message", "message": f"You end the conversation with {character.name}."})
                break

            character.messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "[\""+player_input+"\", "+str(character.standing)+", \""+character.description+"\"]"
                    }
                ]
            })
            ##send model the conversation and the character info
            response = client.chat.completions.create(
                model = "gpt-4o",
                messages = character.messages,
                response_format={"type":"text"},
                temperature = 1,
                max_tokens = 2048,
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0
            )
            #break up and update all the information
            response_arr = response.choices[0].message.content
            response_arr = response_arr.split('$')
            if not len(response_arr) == 3:
                #the model will sometimes not set the delimiters
                self.send_message({"type": "dialogue-window", "message": "The model did not format it's response properly."})
                self.send_message({"type": "dialogue-window", "status": "end-dialogue"})
                self.send_message({"type": "system-message", "message": f"You end the conversation with {character.name}."})
                break
            character_output = response_arr[0] 
            character.standing = response_arr[1]
            character.description = response_arr[2]
            #model should append [END] to it's last message 
            last_message = "[END]" in response_arr[0]
            if last_message:
                character_output = character_output.replace("[END]", "")
            # print model output
            self.send_message({"type": "dialogue-message", "message": character_output})

            # end dialogue - model outputs special token [END]
            if last_message or player_input == "[END]":
                time.sleep(6)
                self.send_message({"type": "dialogue-window", "status": "end-dialogue"})
                self.send_message({"type": "system-message", "message": f"You end the conversation with {character.name}."})
                break



if __name__ == "__main__":
    # define items - keep all keys lowercase
    all_items = {
        "scythe": Weapon(name="Scythe", description="A sharp scythe that can be used to harvest crops or enemies.", image_filename="scythe.png", damage=50),
        "aurum flower": Item(name="Aurum Flower", description="A rare golden flower that only blooms in the meadow.", image_filename="flower.png"),
        "holy water vial": Item(name="Holy Water Vial", description="A vial of holy water that can be thrown at enemies for massive damage.", image_filename="vial.png"),
        "storage room key": Item(name="Storage Room Key", description="A key that unlocks the storage room in the castle.", image_filename="key.png"),
        "red amulet": Item(name="Red Amulet", description="A ruby red amulet that glows with ominous power.", image_filename="amulet.png"),
        "empty amulet": Item(name="Empty Amulet", description="An amulet with an empty socket, waiting to be filled with a corrupt soul.", image_filename="empty_amulet.png"),
        "jar of pickles": Item(name="Jar of Pickles", description="A jar filled with pickles, surprisingly well-preserved and tasty.", image_filename="pickles.png"),
        "queen's pendant": Item(name="The Queen's Pendant", description="A holy relic pendant that once belonged to the late queen with the power to cleanse the wicked.", image_filename="pendant.png"),
        "alchemist's logs": Item(name="Alchemist's Logs", description="Logs and notes from a nefarious alchemist, detailing various experiments.", image_filename="notebook.png"),
        "crested shield": Item(name="Crested Shield", description="A shield emblazoned with the royal crest of Tridica.", image_filename="shield.png"),
        "ham": Item(name="Ham", description="A piece of ham.", image_filename="ham.png"),
    }

    # define locations
    all_locations = {
        "the graveyard": Location(name="The Graveyard", description="Behind your farmshed are two graves marked by crosses and an empty ditch that you crawled out of.", items=[all_items["scythe"]], characters=[]),
        "the corrupted forest": Location(name="The Corrupted Forest", description="The forest, once a lush and verdant sanctuary teeming with life, is now a nightmarish tableau of decay. Twisted trees claw at the overcast sky, their leaves a sickly brown. A pervasive, unnatural fog slithers between gnarled roots and choking vines. Glimpses of the castle loom distantly through the mist, its spires a haunting silhouette against the grey light. The silence is oppressive; no birdsong or rustle of small creatures disturbs the air. The earth is littered with fallen branches, swords, and shields half-buried in the muck. You see an obscured path on the left and the main road leading out the forest on the right.", items=[], characters=[]),
        "a peaceful meadow": Location(name="A Peaceful Meadow", description="A small hidden meadow gently lit by sunlight with a running creek. There's a small patch of golden flowers next to it.", items=[all_items["aurum flower"]], characters=[]),
        "the church of lenia": Location(name="The Church of Lenia", description="The ruins of the Church of Lenia stand solemnly amidst the desolation, a once-hallowed ground now defiled by tragedy. Tarnished spires reach toward a heavy sky, the grand facade is pockmarked with the scars of battle, and the once vibrant stained-glass windows lay shattered. Dark bloodstains mar the altar stone, a chilling reminder of the brutal massacre that has tainted this sanctuary and the heavy price of a king's wrath. You see the Head Priest Callum mortally wounded and lying bleeding at the foot of the altar.", items=[all_items["holy water vial"]], characters=[]),
        "the castle gate watch tower": Location(name="The Castle Gate Watch Tower", description="The watchtower stands forlorn, its stones crumbling and weathered from years of neglect. A palpable sense of unease clings to the cold stones, and faded bloodstains are a grim testament to the tower's violent past. The ominous castle looms in the near distance. You see a lone restless guard at the top who shouts at you.", items=[all_items["storage room key"]], characters=[]),
        "the city square of tridica": Location(name="The City Square of Tridica", description="The city once buzzed with the vibrancy of Tridica's heart, but now it stands as a desolate testament to the kingdom's doom. Buildings that were once elegant and proud are now crumbling facades, their stones eroded and scorched. The streets, once filled with the chatter and laughter of a busy populace, now echo with an eerie silence, occasionally broken by the distant shrieks of lurking ghouls. Sunlight rarely pierces the gloomy overcast. The once-celebrated fountain sit at the center of the town square now supports an executioner's platform, and a 7-foot tall clad in black armor Executioner wielding a mighty Axe stops you from advancing.", items=[], characters=[]),
        "the marketplace": Location(name="The Marketplace", description="The Marketplace is once-bustling area that has now fallen into chaos. Stalls that once sold a variety of goods are overturned and looted. The forge, once the heart of the marketplace, is now cold and abandoned. Ruined Knights are ransacking the area, searching for anything of value.", items=[all_items["crested shield"]], characters=[]),
        "the castle hall": Location(name="The Castle Hall", description="The Castle Hall is a vast, echoing chamber with high ceilings and grand chandeliers that once sparkled with light. Now, the chandeliers and portraits of long-dead royalty along the walls hang dark and faded. The floor is covered in a thick layer of dust, and the air is heavy with the scent of decay. At the far end of the hall, a grand staircase leads up to the upper levels of the castle. The left door leads to the Dining Hall and the right leads to an ominous presence.", items=[], characters=[]),
        "the dining hall": Location(name="The Dining Hall", description="The Dining Hall is a long, narrow room with a massive wooden table running down the center. The table could hold extravagant feasts fit for a king, but now it is covered in dust and cobwebs. Giant rats eat away at rotting food strewn across the room. At the far end of the hall there's a locked storage room.", items=[all_items["jar of pickles"]], characters=[]),
        "the dungeon": Location(name="The Dungeon", description="The storage room has been converted into a Dungeon - a dark, damp place, with narrow corridors and small, cramped cells. The only light comes from flickering torches mounted on the walls. The cells are empty now, but the heavy iron doors and rusted chains hint at the horrors that once took place here. Chained to the wall is the former Advisor to the King, Allan. He's bruised and emaciated but still lucid.", items=[all_items["queen's pendant"]], characters=[]),
        "the dragon statue shrine": Location(name="The Dragon Statue Shrine", description="The Dragon Statue is a massive, imposing figure carved from dark stone. It stands at the end of the hall, its wings spread wide and its mouth open in a silent roar. Its right eye is a ruby-like amulet that glow like the one found on the Executioner, and its left is hollow. The ground around it is cracked and uneven.", items=[], characters=[]), 
        "the alchemist's laboratory": Location(name="The Alchemist's Laboratory", description="The castle laboratory is a cavernous, stone-walled room filled with instruments of alchemy and ancient tomes of forbidden knowledge are piled across workbenches. At the center stands a grand, alchemical apparatus - an Empty Amulet. In the far corner, is a black and red leather-bound notebook, the Alchemist's Logs", items=[all_items["empty amulet"], all_items["alchemist's logs"]], characters=[]),
        "the throne room": Location(name="The Throne Room", description="The Throne Room, a grand hall that once echoed with regal proclamations and praises of Lenia, now lies in grim disarray. The once magnificent tapestries that adorned the walls have become moth-eaten and hang in tatters, their vibrant colors faded into a melancholic grayness. On the throne sits King Alderic, but he's transformed as a monstrous husk of his former self. He wears a crown holding a glowing green amulet, and his eyes have glazed over white. 'Come then Chosen! Let us see whose will is stronger — your false god or the greatest dynasty to ever be. Meet thy fate upon my blade and join your silent congregation!'", items=[], characters=[]),
    }

    # define location connections - explicitly bidirectional
    all_locations["the graveyard"].add_connection("down", all_locations["the corrupted forest"])
    all_locations["the corrupted forest"].add_connection("up", all_locations["the graveyard"])

    all_locations["the corrupted forest"].add_connection("right", all_locations["a peaceful meadow"])
    all_locations["a peaceful meadow"].add_connection("left", all_locations["the corrupted forest"])

    all_locations["the corrupted forest"].add_connection("down", all_locations["the church of lenia"])
    all_locations["the church of lenia"].add_connection("up", all_locations["the corrupted forest"])

    all_locations["the church of lenia"].add_connection("right", all_locations["the castle gate watch tower"])
    all_locations["the castle gate watch tower"].add_connection("left", all_locations["the church of lenia"])

    # blocked initially - guard quest
    # all_locations["the castle gate watch tower"].add_connection("down", all_locations["the city square of tridica"])
    # all_locations["the city square of tridica"].add_connection("up", all_locations["the castle gate watch tower"])

    # blocked initially - executioner quest
    # all_locations["the city square of tridica"].add_connection("right", all_locations["the marketplace"])
    # all_locations["the marketplace"].add_connection("left", all_locations["the city square of tridica"])

    # blocked initially - executioner quest
    # all_locations["the city square of tridica"].add_connection("down", all_locations["the castle hall"])
    # all_locations["the castle hall"].add_connection("up", all_locations["the city square of tridica"])

    all_locations["the castle hall"].add_connection("right", all_locations["the dining hall"])
    all_locations["the dining hall"].add_connection("left", all_locations["the castle hall"])

    all_locations["the castle hall"].add_connection("left", all_locations["the dragon statue shrine"])
    all_locations["the dragon statue shrine"].add_connection("left", all_locations["the castle hall"])

    all_locations["the castle hall"].add_connection("down", all_locations["the throne room"])
    all_locations["the throne room"].add_connection("up", all_locations["the castle hall"])

    # blocked initially - storage room quest
    # all_locations["the dining hall"].add_connection("down", all_locations["the dungeon"])
    # all_locations["the dungeon"].add_connection("up", all_locations["the dining hall"])

    # blocked initially - dragon quest
    # all_locations["the dragon statue shrine"].add_connection("right", all_locations["the alchemist's laboratory"])
    # all_locations["the alchemist's laboratory"].add_connection("left", all_locations["the dragon statue shrine"])

    # define NPCs - keep all keys lowercase
    all_characters = {
        "john": Character(name="John", description="A friendly villager", inventory=[all_items["ham"]], location=all_locations["the graveyard"], max_health=50),
        "rimor the angel": Character(name="Rimor the Angel", description="Lenia's messenger sent as a vengeful spirit.", inventory=[], location=all_locations["the corrupted forest"], max_health=200),
        "head priest callum": Character(name="Head Priest Callum", description="The head priest of the Church of Lenia, now mortally wounded.", inventory=[], location=all_locations["the church of lenia"], max_health=30),
        "hellish ghouls": Character(name="Hellish Ghouls", description="Ghouls that haunt the Church of Lenia.", inventory=[], location=all_locations["the church of lenia"], max_health=100),
        "restless guard": Character(name="Restless Guard", description="A guard who still stands vigilant at the watchtower.", inventory=[], location=all_locations["the castle gate watch tower"], max_health=70),
        "executioner": Character(name="Executioner", description="A tall executioner wielding a mighty axe.", inventory=[all_items["red amulet"]], location=all_locations["the city square of tridica"], max_health=150),
        "ruined knights": Character(name="Ruined Knights", description="Knights that have fallen to ruin, scavenging the marketplace.", inventory=[], location=all_locations["the marketplace"], max_health=80),
        "giant rats": Character(name="Giant Rats", description="Rats that have grown to an enormous size, feasting on rotting food.", inventory=[], location=all_locations["the dining hall"], max_health=20),
        "advisor allan": Character(name="Advisor Allan", description="The former advisor to the king, now imprisoned and emaciated.", inventory=[], location=all_locations["the dungeon"], max_health=40),
        "king alderic": Character(name="King Alderic", description="The former king, now a monstrous husk.", inventory=[], location=all_locations["the throne room"], max_health=250),
        "dragon statue": Character(name="Dragon Statue", description="A massive, imposing figure carved from dark stone.", inventory=[], location=all_locations["the dragon statue shrine"], max_health=200),
    }

    # add NPCs to locations
    all_locations["the graveyard"].add_character(all_characters["john"])
    all_locations["the corrupted forest"].add_character(all_characters["rimor the angel"])
    all_locations["the church of lenia"].add_character(all_characters["head priest callum"])
    all_locations["the church of lenia"].add_character(all_characters["hellish ghouls"])
    all_locations["the castle gate watch tower"].add_character(all_characters["restless guard"])
    all_locations["the city square of tridica"].add_character(all_characters["executioner"])
    all_locations["the marketplace"].add_character(all_characters["ruined knights"])
    all_locations["the dining hall"].add_character(all_characters["giant rats"])
    all_locations["the dungeon"].add_character(all_characters["advisor allan"])
    all_locations["the dragon statue shrine"].add_character(all_characters["dragon statue"])
    all_locations["the throne room"].add_character(all_characters["king alderic"])

    # define player and initialize
    player = Player(name="Player", description="A wandering traveler", inventory=[], location=all_locations["the graveyard"], max_health=100)
    all_locations["the graveyard"].add_character(player)

    # define quests
    all_quests = {
        "Get Equipped": Quest(name="Get Equipped", description="Find a weapon to defend yourself.", unlock_conditions={"at_location": "the graveyard"}, complete_conditions={"has_items": [all_items["scythe"]]}),

        # Standings -100, -50, 50, 100; intermediate quests like dragon; 3 endings
        # Blocks - 1. Get the guard to let you pass 2. Defeat Executioner 3. Unlock dragon statue 4. Unlock storage room/dungeon
        
        # to-do: guard standing must be reach some value to pass
        "Convince the Guard": Quest(name="Convince the Guard", description="Convince the restless guard to let you pass the watchtower.", unlock_conditions={"at_location": "the castle gate watch tower"}, complete_conditions={"standings": {"guard": 100}}),
        
        "Defeat the Executioner": Quest(name="Defeat the Executioner", description="Defeat the Executioner guarding the city square.", unlock_conditions={"at_location": "the city square of tridica"}, complete_conditions={"characters_dead": ["executioner"]}),
        
        "Unlock the Dragon": Quest(name="Defeat the Dragon", description="Defeat the dragon guarding the castle.", unlock_conditions={"has_items":[all_items["red amulet"]]}, complete_conditions={}), # give the dragon statue the red amulet
        
        "Unlock the Storage Room": Quest(name="Unlock the Storage Room", description="Unlock the storage room in the castle.", unlock_conditions={"at_location": "the dining hall"}, complete_conditions={"has_items": [all_items["storage room key"]]}),

        # 3 Endings
        # good (Spare King Alderic), bad (Imprison King Alderic), neutral (Kill King Alderic)
        "Spare King Alderic": Quest(name="Spare King Alderic", description="Spare the corrupted king and show mercy.", unlock_conditions={"at_location": "the throne room", "has_items": [all_items["queen's pendant"]]}, complete_conditions={}),
        "Defeat King Alderic": Quest(name="Defeat King Alderic", description="Defeat the corrupted king and end his reign of terror.", unlock_conditions={"at_location": "the throne room"}, complete_conditions={"characters_dead": ["king alderic"]}),
        "Imprison King Alderic": Quest(name="Imprison King Alderic", description="Imprison the corrupted king and seal him away, dooming the nation.", unlock_conditions={"has_items": [all_items["queen's pendant"]]}, complete_conditions={}),

        # "Defeat John": Quest(name="Defeat John", description="Defeat John", unlock_conditions={}, complete_conditions={"characters_dead": ["john"]}),
        #"Go North": Quest(name="Go North", description="This is a test quest", unlock_conditions={}, complete_conditions={"at_location": "the end location"}),
        #"Get Sword": Quest(name="Get Sword", description="This is another test quest", unlock_conditions={"completed_quests": ["Go North"]}, complete_conditions={"has_items": [all_items["sword"]]})
    }

    # start game
    game = Game(player=player, items=all_items, characters=all_characters, locations=all_locations, quests=all_quests)
    game.intro()
    game.main_loop()