import pygame
import os
from object.Player import Player
from object.Rock import Rock
from object.Power import Power
from object.Explosion import Explosion

FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800

def draw_test(surface, text, size, x, y):
    # font_name = pygame.font.match_font('arial')
    font_name = os.path.join("font.ttf")
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surface.blit(text_surface, text_rect)

def create_rock(all_sprites, rocks):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surface, health, x, y):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (health / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, (0,255,0), fill_rect) # 血量內部矩形
    pygame.draw.rect(surface, (255,255,255), outline_rect, 2) # 血量外框

def draw_lives(surface, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32 * i
        img_rect.y = y
        surface.blit(img, img_rect)


def draw_init(window, clock, background_img):
    window.blit(background_img, (0,0)) 
    draw_test(window, '太空生存戰!', 64, WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
    draw_test(window, '← →移動飛船 空白鍵發射子彈~', 22, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    draw_test(window, '案任意鍵開始遊戲', 18, WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4)  
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:  
                waiting = False
                return False