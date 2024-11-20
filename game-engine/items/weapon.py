from items.item import Item

class Weapon(Item):
    def __init__(self, name, description, image_filename, damage):
        super().__init__(name, description, image_filename)
        self.damage = damage