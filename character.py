from pico2d import *

class Character:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.image = load_image('character_Walk.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass