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
        self.send_message({"type": "header-message", "message": "Introduction"})
        with open("../game-engine/data/txt/intro.txt", "r") as f:
            for line in f:
                self.send_message({"type": "story-message", "message": line.strip()})
        self.send_message({"type": "header-message", "message": "Chapter 1"})

        # print overview of starting area
        self.send_message({"type": "system-message", "message": f"You are at {self.player.location.name}."})
        self.send_message({"type": "system-message", "message": f"{self.player.location.description}"})
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
                self.send_message({"type": "system-message", "message": f"From here you can go: {', '.join(self.player.location.connecting_locations.keys())}"})
                
            # move
            elif action.split()[0] == "move" and len(action.split()) > 1:
                direction = action.split()[1]
                current_location = self.locations[self.player.location.name]
                self.player.move(current_location, direction)

            # unknown command
            else:
                self.send_message({"type": "system-message", "message": f"System echoing: {command}"})
                
    def parse_command(self, command):
        # to-do: parse command using parser model - return predefined action (get, look, etc.)

        # placeholder "move/go" command for testing
        tokens = command.lower().split()
        if tokens[0] in ["move", "go"] and len(tokens) > 1:
            return f"move {tokens[1]}"

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
        "the starting location": Location(name="the starting location", description="There's not much to do here, but it's certainly some kind of starting location.", items=[all_items["sword"]], characters=[]),
        "the end location": Location(name="the end location", description="There also isn't much to do here yet. The walls have two-toned scrolling checkerboard patterns covering them.", items=[], characters=[])
    }

    # define location connections
    all_locations["the starting location"].add_connection("north", all_locations["the end location"])
    all_locations["the end location"].add_connection("south", all_locations["the starting location"])

    # define player and initialize
    player = Player(name="Player", description="A wandering traveler", inventory=[all_items["amulet"]], location=all_locations["the starting location"], max_health=100)
    all_locations["the starting location"].add_character(player)

    # start game
    game = Game(player=player, items=all_items, characters=all_characters, locations=all_locations)
    game.intro()
    game.main_loop()