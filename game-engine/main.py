import sys
import json
from characters.player import Player
from locations.location import Location
from items.item import Item
from items.weapon import Weapon

class Game():
    def __init__(self, player, items, characters, locations):
        self.player = player
        self.items = items
        self.characters = characters
        self.locations = locations

    def intro(self):
        # load intro dialogue txt
        with open("../game-engine/data/txt/intro.txt", "r") as f:
            for line in f:
                self.send_message({"type": "message", "message": line.strip()})

    def main_loop(self):
        while True:
            # get user input, feed into parser model
            command = sys.stdin.readline().strip()
            action = self.parse_command(command)

            # determine which predefined action based on output parse
            if action == "look":
                self.send_message({"type": "message", "message": "You look around the room."})
            else:
                self.send_message({"type": "message", "message": f"System echoing: {command}"})
                
    def parse_command(self, command):
        # to-do: parse command using parser model - return predefined action (get, look, etc.)
        return command
    
    def send_message(self, message):
        print(json.dumps(message))
        sys.stdout.flush()


if __name__ == "__main__":
    # define items
    all_items = {
        "amulet": Item(name="Amulet", description="A shiny amulet passed down from your ancestors", image_filename="amulet.png"), 
        "sword": Weapon(name="Sword", description="A sharp sword", image_filename="sword.png", damage=10)
    }

    # define characters
    all_characters = {}

    # define locations
    all_locations = {
        "start": Location(name="start", description="The starting location", items=[all_items["sword"]], characters=[]),
        "end": Location(name="end", description="The ending location", items=[], characters=[])
    }

    # define location connections
    all_locations["start"].add_connection("end", "north")
    all_locations["end"].add_connection("start", "south")

    # define player
    player = Player(name="Player", description="A wandering traveler", inventory=[all_items["amulet"]], location="start", max_health=100)

    # start game
    game = Game(player=player, items=all_items, characters=all_characters, locations=all_locations)
    game.intro()
    game.main_loop()