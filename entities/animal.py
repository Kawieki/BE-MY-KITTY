class Animal:
    def __init__(self, static_asset, animated_asset=None, name="none", age=0):
        self.static_asset = static_asset
        self.animated_asset = animated_asset
        self.current_asset = static_asset
        self.name = name
        self.age = age
        self.hunger_level = 100.0
        self.boredom_level = 100.0

    def use_static_asset(self):
        self.current_asset = self.static_asset

    def use_animated_asset(self):
        if self.animated_asset:
            self.current_asset = self.animated_asset

    def make_sound(self):
        pass

    def move(self):
        pass

    def special_secret_ability(self):
        pass

class HelloKitty(Animal):
    pass

class Kuromi(Animal):
    pass

class Cinnamoroll(Animal):
    pass

class Melody(Animal):
    pass