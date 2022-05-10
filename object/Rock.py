import pygame
import os
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rock_imgs = []
        for i in range(7):
            rock_imgs.append(pygame.image.load(os.path.join("images/img", f"rock{i}.png")).convert())
        # rock_img = pygame.image.load(os.path.join("images/img", "rock.png")).convert()
        self.origin_image = random.choice(rock_imgs)
        self.origin_image.set_colorkey((0,0,0)) # 把某個顏色變透明
        self.image = self.origin_image.copy()

        self.rect = self.image.get_rect() # 框起來並定位
        self.radius = self.rect.width / 2 * 0.8
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        # 設定屬性(物件初始位置)
        self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedX = random.randrange(-3, 3)
        self.speedY = random.randrange(2, 10)
        self.total_rotation = 0
        self.rotate_degree = random.randrange(-3, 3)

    def rotate(self):
        # 紀錄總旋轉量，每次旋轉都是對最原始的圖片進行旋轉
        self.total_rotation += self.rotate_degree
        self.total_rotation = self.total_rotation % 360
        self.image = pygame.transform.rotate(self.origin_image, self.total_rotation)

        # 旋轉後重新定位
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedY
        self.rect.x += self.speedX

        if self.rect.top > WINDOW_HEIGHT or self.rect.left > WINDOW_WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedX = random.randrange(-3, 3)
            self.speedY = random.randrange(2, 10)