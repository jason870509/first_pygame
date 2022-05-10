from xmlrpc.client import NOT_WELLFORMED_ERROR
import pygame
import os

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

class Explosion(pygame.sprite.Sprite):
    def __init__(self, explosion, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.explosion = explosion
        self.image = self.explosion[self.size][0]
        self.rect = self.image.get_rect() # 框起來並定位
        # 設定屬性(物件初始位置)
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion[self.size]):
                self.kill()
            else:
                self.image = self.explosion[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center