import sys
import json

class Game():
    def __init__(self):
        pass

    def intro(self):
        # load intro dialogue txt
        with open("../game-engine/intro.txt", "r") as f:
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
        # parse command using parser model - return predefined action (get, look, etc.)
        return command
    
    def send_message(self, message):
        print(json.dumps(message))
        sys.stdout.flush()


if __name__ == "__main__":
    game = Game()
    game.intro()
    game.main_loop()