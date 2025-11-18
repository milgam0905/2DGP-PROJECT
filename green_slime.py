from pico2d import *
import game_framework

class GreenSlime:
    image = None

    def __init__(self):
        if GreenSlime.image is None:
            GreenSlime.image = load_image('Green_slime.png')
        self.x, self.y = 1200, 300
        self.frame = 0
        self.dir = 1
        self.speed = 100  # pixels per second

    def update(self):
        self.x += self.dir * self.speed * game_framework.frame_time
        if self.x > 1600 - 50:
            self.dir = -1
        elif self.x < 50:
            self.dir = 1
        self.frame = (self.frame + 10 * game_framework.frame_time) % 4

    def draw(self):
        if self.dir == 1:
            GreenSlime.image.clip_draw(int(self.frame) * 32, 0, 32, 32, self.x, self.y)
        else:
            GreenSlime.image.clip_composite_draw(int(self.frame) * 32, 0, 32, 32, 0, 'h', self.x, self.y, 32, 32)