# base item class
class Item:
    def __init__(self, name, description, image_filename):
        self.name = name
        self.description = description
        self.image_filename = image_filename