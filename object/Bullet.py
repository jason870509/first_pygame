import pygame
import os

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        bullet_img = pygame.image.load(os.path.join("images/img", "bullet.png")).convert()
        self.image = bullet_img
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect() # 框起來並定位
        # 設定屬性(物件初始位置)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedY = - 10


    def update(self):
        self.rect.y += self.speedY

        if self.rect.bottom < 0:
            self.kill()