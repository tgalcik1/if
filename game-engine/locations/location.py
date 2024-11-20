# base location class
class Location:
    def __init__(self, name, description, items, characters):
        self.name = name
        self.description = description
        self.items = items
        self.characters = characters
        self.connecting_locations = {} 

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def add_character(self, character):
        self.characters.append(character)

    def remove_character(self, character):
        self.characters.remove(character)

    def add_connection(self, location, path):
        self.connecting_locations[location] = path

    def remove_connection(self, location):
        del self.connecting_locations[location]