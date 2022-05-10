import pygame
import os
from object.Bullet import Bullet

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

# player_img = pygame.transform.scale(background_img, (600, 800))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(os.path.join("images/img", "player.png")).convert()
        self.image = pygame.transform.scale(player_img, (60, 50))
        self.image.set_colorkey((0,0,0)) # 把某個顏色變透明
        # self.image = pygame.Surface((50, 40))
        # self.image.fill(color=(0, 255, 0))

        self.rect = self.image.get_rect() # 框起來並定位
        self.radius = 25
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        # 設定屬性(物件初始位置)
        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDOW_HEIGHT - 10 
        self.speedX = 10
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hidden_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
            self.gun = 1
            self.gun_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hidden_time > 1000:
            self.hidden = False
            self.rect.centerx = WINDOW_WIDTH / 2
            self.rect.bottom = WINDOW_HEIGHT - 10 
        # 鍵盤控制
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.rect.x += self.speedX
        elif key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.rect.x -= self.speedX
        
        # 設定 x 軸邊界
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if self.gun == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            return bullet
        elif self.gun >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            return [bullet1, bullet2]
        

    def hide(self):
        self.hidden = True
        self.hidden_time = pygame.time.get_ticks()
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT + 500)

    def gunUp(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
