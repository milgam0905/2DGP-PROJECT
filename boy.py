from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
import game_world
import game_framework


from state_machine import StateMachine


def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

class Idle:
    def __init__(self, boy):
        self.boy = boy
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 6
        delay(0.2)
    def draw(self):
        self.boy.idle_image.clip_draw(self.boy.frame * 128, 0, 128, 128, self.boy.x, self.boy.y)

class Walk:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        delay(0.2)
    def draw(self):
        self.boy.walk_image.clip_draw(self.boy.frame * 128, 0, 128, 128, self.boy.x, self.boy.y)

class Boy:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.walk_image = load_image('character_Walk.png')
        self.idle_image = load_image('character_Idle.png')
        self.frame = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.WALK},
                self.WALK : {space_down: self.IDLE}
            }
        )

    def draw(self):
        self.state_machine.draw()
    def update(self):
        self.state_machine.update()

    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50
    def handle_collision(self, group, other):
        pass
    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))