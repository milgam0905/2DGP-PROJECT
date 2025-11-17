from pico2d import *

class Boy:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.image = load_image('character_Walk.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass
    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50
    def handle_collision(self, group, other):
        pass
    def handle_event(self, event):
        pass