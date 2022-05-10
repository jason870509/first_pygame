import random
import pygame
import os

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

class Power(pygame.sprite.Sprite):
    def __init__(self, center, imgs):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = imgs[self.type]
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect() # 框起來並定位
        # 設定屬性(物件初始位置)
        self.rect.center = center
        self.speedY = 3


    def update(self):
        self.rect.y += self.speedY

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()