import random
from pico2d import *

import game_framework
import game_world
from boy import Boy


from game_world import add_object

boy = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy
    global balls

    boy = Boy()
    add_object(boy)


def update():
    game_world.update()
    game_world.handle_collisions()



def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

