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
        # "sword": Weapon(name="Sword", description="A sharp sword", image_filename="sword.png", damage=10),
        "Sycthe": Weapon(name="Sycthe", description="A sharp sycthe that can be used to harvest crops or enemies.", image_filename="sycthe.png", damage=10),
        "AurumFlower": Item(name="Aurum Flower", description="A rare golden flower that only blooms in the meadow.", image_filename="flower.png"),
        "HolyWaterVial": Item(name="Holy Water Vial", description="A vial of holy water that be thrown at enemies for massive damage.", image_filename="vial.png"),
        "StorageRoomKey": Item(name="Storage Room Key", description="A key that unlocks the storage room in the castle.", image_filename="key.png"),
        "RedAmulet": Item(name="Red Amulet", description="A ruby red amulet that glows with ominous power.", image_filename="amulet.png"),
        "EmptyAmulet": Item(name="Empty Amulet", description="An amulet with an empty socket, waiting to be filled with a corrupt soul.", image_filename="empty_amulet.png"),
        "JarOfPickles": Item(name="Jar of Pickles", description="A jar filled with pickles, surprisingly well-preserved and tasty.", image_filename="pickles.png"),
        "QueensPendant": Item(name="The Queen's Pendant", description="A holy relic pendant that once belonged to the late queen with the power to cleanse the wicked.", image_filename="pendant.png"),
        "AlchemistLogs": Item(name="Alchemist's Logs", description="Logs and notes from an nefarious alchemist, detailing various experiments.", image_filename="notebook.png")
    }

    # define locations
    all_locations = {
        # "EndLocation": Location(name="the end location", description="There also isn't much to do here yet. The walls have two-toned scrolling checkerboard patterns covering them.", items=[all_items["sword"]], characters=[]),
        "StartLocation": Location(name="Graveyard", description="Behind your farmshed are two graves marked by crosses and an empty ditch that you crawled out of.", items=[all_items("Sycthe")], characters=[]),
        "CorruptedForest": Location(name="Corrupted Forest", description="The forest, once a lush and verdant sanctuary teeming with life, is now a nightmarish tableau of decay. Twisted trees claw at the overcast sky, their leaves a sickly brown. A pervasive, unnatural fog slithers between gnarled roots and choking vines. Glimpses of the castle loom distantly through the mist, its spires a haunting silhouette against the grey light. The silence is oppressive; no birdsong or rustle of small creatures disturbs the air. The earth is littered with fallen branches, swords, and shields half-buried in the muck. You see an obscured path on the left and the main road leading out the forest on the right.", items=[], characters=[QueenElianora]),
        "Meadow": Location(name="Peaceful Meadow", description="A small hidden meadow gently lit by sunlight with a running creek. There's a small patch of golden flowers next to it.", items=[AurumFlower], characters=[]),
        "ChurchOfLenia": Location(name="The Church of Lenia", description="The ruins of the Church of Lenia stand solemnly amidst the desolation, a once-hallowed ground now defiled by tragedy. Tarnished spires reach toward a heavy sky, the grand facade is pockmarked with the scars of battle, and the once vibrant stained-glass windows lay shattered. Dark bloodstains mar the altar stone, a chilling reminder of the brutal massacre that has tainted this sanctuary and the heavy price of a king's wrath. You see the Head Priest Callum mortally wounded and lying bleeding at the foot of the altar.", items=[all_items("HolyWaterVial")], characters=[HeadPriestCallum, HellishGhouls]),
        "WatchTower": Location(name="Castle Gate Watch Tower", description="The watchtower stands forlorn, its stones crumbling and weathered from years of neglect. A palpable sense of unease clings to the cold stones, and faded bloodstains are a grim testament to the tower's violent past. The ominous castle looms in the near distance. You see a lone restless guard at the top who shouts at you.", items=[all_items("StorageRoomKey")], characters=[RestlessGuard]),
        "CitySquare": Location(name="The City Square of Tridica", description="The city once buzzed with the vibrancy of Tridica's heart, but now it stands as a desolate testament to the kingdom's doom. Buildings that were once elegant and proud are now crumbling facades, their stones eroded and scorched. The streets, once filled with the chatter and laughter of a busy populace, now echo with an eerie silence, occasionally broken by the distant shrieks of lurking ghouls. Sunlight rarely pierces the gloomy overcast. The once-celebrated fountain sit at the center of the town square now supports an executioner's platform, and a 7-foot tall clad in black armor Executioner wielding a mighty Axe stops you from advancing.", items=[all_items("RedAmulet")], characters=[Executioner]),
        "Marketplace": Location(name="Marketplace", description="The Marketplace is once-bustling area that has now fallen into chaos. Stalls that once sold a variety of goods are overturned and looted. The forge, once the heart of the marketplace, is now cold and abandoned. Ruined Knights are ransacking the area, searching for anything of value.", items=[all_items("CrestedShield")], characters=["RuinedKnights"]),
        "Castle Hall": Location(name="Castle Hall", description="The Castle Hall is a vast, echoing chamber with high ceilings and grand chandeliers that once sparkled with light. Now, the chandeliers and portraits of long-dead royalty along the walls hang dark and faded. The floor is covered in a thick layer of dust, and the air is heavy with the scent of decay. At the far end of the hall, a grand staircase leads up to the upper levels of the castle. The left door leads to the Dining Hall and the right leads to an ominous presence.", items=[], characters=[]),
        "Dining Hall": Location(name="Dining Hall", description="The Dining Hall is a long, narrow room with a massive wooden table running down the center. The table could hold extravagant feasts fit for a king, but now it is covered in dust and cobwebs. Giant rats eat away at rotting food strewn across the room. At the far end of the hall there's a locked storage room.", items=[all_items("JarOfPickles")], characters=[GiantRats]),
        "Dungeon": Location(name="Dungeon", description="The storage room has been converted into a Dungeon - a dark, damp place, with narrow corridors and small, cramped cells. The only light comes from flickering torches mounted on the walls. The cells are empty now, but the heavy iron doors and rusted chains hint at the horrors that once took place here. Chained to the wall is the former Advisor to the King, Allan. He's bruised and emaciated but still lucid.", items=[all_items("QueensPendant")], characters=[AdvisorAllan]),
        "DragonStatue": Location(name="Dragon Statue", description="The Dragon Statue is a massive, imposing figure carved from dark stone. It stands at the end of the hall, its wings spread wide and its mouth open in a silent roar. Its right eye is a ruby-like amulet that glow like the one found on the Executioner, and its left is hollow. The ground around it is cracked and uneven.", items=[], characters=["DragonStatue"]), 
        "Castle Laboratory": Location(name="Castle Laboratory", description="The castle laboratory is a cavernous, stone-walled room filled with instruments of alchemy and ancient tomes of forbidden knowledge are piled across workbenches. At the center stands a grand, alchemical apparatus - an Empty Amulet. In the far corner, is a black and red leather-bound notebook, the Alchemist's Logs", items=[all_items("EmptyAmulet", "AlchemistLogs")], characters=[]),
        "ThroneRoom": Location(name="Throne Room", description="The Throne Room, a grand hall that once echoed with regal proclamations and praises of Lenia, now lies in grim disarray. The once magnificent tapestries that adorned the walls have become moth-eaten and hang in tatters, their vibrant colors faded into a melancholic grayness. On the throne sits King Alderic, but he's transformed as a monstrous husk of his former self. He wears a crown holding a glowing green amulet, and his eyes have glazed over white. 'Come then Chosen! Let us see whose will is stronger — your false god or the greatest dynasty to ever be. Meet thy fate upon my blade and join your silent congregation!'", items=[], characters=[KingAlderic]),
    }

    # define location connections
    all_locations["the starting location"].add_connection("north", all_locations["the end location"])
    all_locations["the end location"].add_connection("south", all_locations["the starting location"])

    # define NPCs - keep all keys lowercase
    # all_characters = {
    #     "john": Character(name="John", description="A friendly villager", inventory=[all_items["key"]], location=all_locations["the starting location"], max_health=50),
    # }

    # define NPCs - keep all keys lowercase
    all_characters = {
        "john": Character(name="John", description="A friendly villager", inventory=[all_items["ham"]], location=all_locations["StartLocation"], max_health=50),
        "queen_elianora": Character(name="Queen Elianora", description="A fallen queen, turned into a vengeful spirit.", inventory=[], location=all_locations["CorruptedForest"], max_health=200),
        "head_priest_callum": Character(name="Head Priest Callum", description="The head priest of the Church of Lenia, now mortally wounded.", inventory=[], location=all_locations["ChurchOfLenia"], max_health=30),
        "hellish_ghouls": Character(name="Hellish Ghouls", description="Ghouls that haunt the Church of Lenia.", inventory=[], location=all_locations["ChurchOfLenia"], max_health=100),
        "restless_guard": Character(name="Restless Guard", description="A guard who still stands vigilant at the watchtower.", inventory=[], location=all_locations["WatchTower"], max_health=70),
        "executioner": Character(name="Executioner", description="A tall executioner wielding a mighty axe.", inventory=[all_items["RedAmulet"]], location=all_locations["CitySquare"], max_health=150),
        "ruined_knights": Character(name="Ruined Knights", description="Knights that have fallen to ruin, scavenging the marketplace.", inventory=[], location=all_locations["Marketplace"], max_health=80),
        "giant_rats": Character(name="Giant Rats", description="Rats that have grown to an enormous size, feasting on rotting food.", inventory=[], location=all_locations["DiningHall"], max_health=20),
        "advisor_allan": Character(name="Advisor Allan", description="The former advisor to the king, now imprisoned and emaciated.", inventory=[], location=all_locations["Dungeon"], max_health=40),
        "king_alderic": Character(name="King Alderic", description="The former king, now a monstrous husk.", inventory=[], location=all_locations["ThroneRoom"], max_health=250),
        "dragon_statue": Character(name="Dragon Statue", description="A massive, imposing figure carved from dark stone.", inventory=[], location=all_locations["DragonStatue"], max_health=200),
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