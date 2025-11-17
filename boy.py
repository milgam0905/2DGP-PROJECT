from pico2d import *

class Boy:
    def __init__(self):
        self.x = 800
        self.y = 300
        self.image = load_image('character_Walk.png')
        self.frame = 0

    def draw(self):
        # frame은 인덱스(0..7) 이므로, 실제 픽셀 좌표로 변환해서 전달해야 합니다.
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 8
        delay(0.2)

    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50
    def handle_collision(self, group, other):
        pass
    def handle_event(self, event):
        pass