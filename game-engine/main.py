import sys
import json

class Game():
    def __init__(self):
        # send the intro dialogue messages
        pass

    def main_loop(self):
        while True:
            # get user input, feed into parser model
            command = sys.stdin.readline().strip()
            action = self.parse_command(command)

            # determine which predefined action based on output parse
            if action == "test":
                self.send_message({"type": "message", "message": f"System echoing: {command}"})
                sys.stdout.flush()
                
    def parse_command(self, command):
        return "test"
    
    def send_message(self, message):
        print(json.dumps(message))
        sys.stdout.flush()

            

if __name__ == "__main__":
    game = Game()
    game.main_loop()