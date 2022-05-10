import os
import random
import pygame
from tools import *
from object.Rock import Rock
from object.Power import Power
from object.Player import Player
from object.Explosion import Explosion


FPS = 60
WINDOW_COLOR = (50, 50, 50)

WINDOW_WIDTH = 600
WINDOW_HEIGHT= 800


if __name__ == '__main__':
    # 遊戲初始化 & 創建視窗
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("太空生存戰!")
    
    clock = pygame.time.Clock()

    # 載入圖片 -----------------------------------------------------------
    background_img = pygame.image.load(os.path.join("images/img", "background.png")).convert()
    background_img = pygame.transform.scale(background_img, (600, 800))

    player_mini_img = pygame.image.load(os.path.join("images/img", "player.png")).convert()
    player_mini_img = pygame.transform.scale(player_mini_img, (25, 19))
    player_mini_img.set_colorkey((0,0,0)) 
    pygame.display.set_icon(player_mini_img)
    explosion_animate = {}
    explosion_animate['large'] = []
    explosion_animate['small'] = []
    explosion_animate['player'] = []
    for i in range(8):
        explosion_img = pygame.image.load(os.path.join("images/img", f"expl{i}.png")).convert()
        explosion_img.set_colorkey((0,0,0))
        explosion_animate['large'].append(pygame.transform.scale(explosion_img, (75, 75)))
        explosion_animate['small'].append(pygame.transform.scale(explosion_img, (30, 30)))

        player_explosion_img = pygame.image.load(os.path.join("images/img", f"player_expl{i}.png")).convert()
        player_explosion_img.set_colorkey((0,0,0))       
        explosion_animate['player'].append(player_explosion_img) 

    power_imgs = {}
    power_imgs['shield'] = pygame.image.load(os.path.join("images/img", "shield.png")).convert()
    power_imgs['gun'] = pygame.image.load(os.path.join("images/img", "gun.png")).convert()
   
    # 載入音樂 -----------------------------------------------------------
    shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
    shoot_sound.set_volume(0.1)
    player_die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
    # player_die_sound.set_volume(0.1)

    explosion_sound = [pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
                       pygame.mixer.Sound(os.path.join("sound", "expl1.wav")),]
    explosion_sound[0].set_volume(0.3)
    explosion_sound[1].set_volume(0.3)
    # pygame.mixer.music.load(os.path.join("sound", "scream.wav"))
    pygame.mixer.music.load(os.path.join("sound", "background.ogg"))

    gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
    gun_sound.set_volume(0.5)

    shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
    shield_sound.set_volume(0.5)


    # 加入群組 -----------------------------------------------------------
    # all_sprites = pygame.sprite.Group()
    # rocks = pygame.sprite.Group()
    # bullets = pygame.sprite.Group()
    # powers = pygame.sprite.Group()
    # player = Player()
    # all_sprites.add(player)

    # for num in range(8):
    #     rock = Rock()
    #     all_sprites.add(rock)
    #     rocks.add(rock)

    # 遊戲迴圈 -----------------------------------------------------------
    show_init = True
    running = True
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    past_time = 0

    while running:
        if show_init:
            close = draw_init(window, clock, background_img)
            if close:
                break
            score = 0
            all_sprites = pygame.sprite.Group()
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powers = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)

            for num in range(8):
                rock = Rock()
                all_sprites.add(rock)
                rocks.add(rock)        
            show_init = False

        clock.tick(FPS) # 1 秒鐘最多只能執行 FPS 次
        past_time += clock.get_time()
        # 取得輸入 -----------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # elif event.type == pygame.KEYDOWN:  
            #     if event.key == pygame.K_SPACE:
            #         bullet = player.shoot()
            #         all_sprites.add(bullet)
            #         bullets.add(bullet)

        key_pressed = pygame.key.get_pressed()
        bullet_delay = 200
        if key_pressed[pygame.K_SPACE] and past_time > bullet_delay:
            past_time = 0
            if not(player.hidden):
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()  

        # 更新遊戲 -----------------------------------------------------------
        all_sprites.update()
        
        # 石頭&子彈 碰撞判斷
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # return {key(rock): value(bullet)}
        for hit in hits:
            score += int(hit.radius) # rock 的 radius
            explosion = Explosion(explosion_animate, hit.rect.center, 'large')
            all_sprites.add(explosion)
            create_rock(all_sprites, rocks)
            random.choice(explosion_sound).play()

            if random.random() < 0.05:
                power = Power(hit.rect.center, power_imgs)
                all_sprites.add(power)
                powers.add(power)
        
        # 石頭&飛機 碰撞判斷
        hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
        for hit in hits:
            create_rock(all_sprites, rocks)
            explosion = Explosion(explosion_animate, hit.rect.center, 'small')
            all_sprites.add(explosion)
            player.health -= hit.radius
            if player.health <= 0:
                player_die = Explosion(explosion_animate, player.rect.center, 'player')
                all_sprites.add(player_die)
                player_die_sound.play()
                player.lives -= 3
                player.health = 100
                player.hide()

        # 寶物&飛機 碰撞判斷
        hits = pygame.sprite.spritecollide(player, powers, True)
        for hit in hits:
            if hit.type == 'shield':
                shield_sound.play()
                player.health += 20
                if player.health > 100:
                    player.health = 100
            elif hit.type == 'gun':
                gun_sound.play()
                player.gunUp()
            
        if player.lives == 0 and not(player_die.alive( )):
            show_init = True
            
        # 畫面顯示 -----------------------------------------------------------
        window.fill(color=WINDOW_COLOR)
        window.blit(background_img, (0,0))
        all_sprites.draw(window)
        draw_test(window, "Score: "+str(score), 18, WINDOW_WIDTH / 2, 10)
        draw_health(window, player.health, 5, 15)
        draw_lives(window, player.lives, player_mini_img, WINDOW_WIDTH-100, 15)
        pygame.display.update()

    pygame.quit()