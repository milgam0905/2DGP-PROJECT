from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT
import game_world
import game_framework


from state_machine import StateMachine


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

time_out = lambda e: e[0] == 'TIMEOUT'

class Idle:
    def __init__(self, boy):
        self.boy = boy
    def enter(self, e):
        pass
    def exit(self, e):
        pass
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 6
    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.idle_image.clip_draw(self.boy.frame * 128, 0, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.idle_image.clip_composite_draw(self.boy.frame * 128, 0, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)

class Walk:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.update_direction()
    def exit(self, e):
        self.boy.xdir = 0
        self.boy.ydir = 0
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8
        self.boy.x = self.boy.x + self.boy.xdir * 5
        self.boy.y = self.boy.y + self.boy.ydir * 5
    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.walk_image.clip_draw(self.boy.frame * 128, 0, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.walk_image.clip_composite_draw(self.boy.frame * 128, 0, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)

class Attack1:
    def __init__(self, boy):
        self.boy = boy
    def enter(self, e):
        self.boy.frame = 0
    def exit(self, e):
        pass
    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 7
        delay(0.2)
        if self.boy.frame == 6:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))
    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.attack1_image.clip_draw(self.boy.frame * 128, 0, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.attack1_image.clip_composite_draw(self.boy.frame * 128, 0, 128, 128, 0, 'h', self.boy.x, self.boy.y, 128, 128)


class Boy:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.walk_image = load_image('character_Walk.png')
        self.idle_image = load_image('character_Idle.png')
        self.attack1_image = load_image('character_Attack_1.png')
        self.frame = 0
        self.xdir = 0
        self.ydir = 0
        self.face_dir = 1


        self.keys = set()

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.ATTACK1 = Attack1(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE : {space_down: self.ATTACK1, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, up_down: self.WALK, down_down: self.WALK, up_up: self.WALK, down_up: self.WALK},
                self.WALK : {space_down: self.ATTACK1, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, up_up: self.IDLE, down_up: self.IDLE, up_down: self.IDLE, down_down: self.IDLE},
                self.ATTACK1 : {time_out: self.IDLE}
            }
        )

    def update_direction(self):
        if 'RIGHT' in self.keys and 'LEFT' not in self.keys:
            self.xdir = 1
            self.face_dir = 1
        elif 'LEFT' in self.keys and 'RIGHT' not in self.keys:
            self.xdir = -1
            self.face_dir = -1
        else:
            self.xdir = 0

        if 'UP' in self.keys and 'DOWN' not in self.keys:
            self.ydir = 1
        elif 'DOWN' in self.keys and 'UP' not in self.keys:
            self.ydir = -1
        else:
            self.ydir = 0

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50

    def handle_collision(self, group, other):
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.keys.add('RIGHT')
            elif event.key == SDLK_LEFT:
                self.keys.add('LEFT')
            elif event.key == SDLK_UP:
                self.keys.add('UP')
            elif event.key == SDLK_DOWN:
                self.keys.add('DOWN')
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.keys.discard('RIGHT')
            elif event.key == SDLK_LEFT:
                self.keys.discard('LEFT')
            elif event.key == SDLK_UP:
                self.keys.discard('UP')
            elif event.key == SDLK_DOWN:
                self.keys.discard('DOWN')

        self.update_direction()

        self.state_machine.handle_state_event(('INPUT', event))
