import pygame
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_ESCAPE
from pygame import mixer
import random
import time



pygame.init()
mixer.init()

clock = pygame.time.Clock()
screen = width, heigth = 1366, 768
FPS = 60
IMG_PATH = 'goose'

mixer.music.load('bg.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()

BLUE = (0, 0, 255)
BLACK = (0, 0 ,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

main_surface = pygame.display.set_mode(screen)


player_imgs = [pygame.image.load(IMG_PATH + '/' + file).convert_alpha() for file in listdir(IMG_PATH)]
player = pygame.transform.scale_by((player_imgs[0]), 0.7)
player_rect = player.get_rect()
player_speed = 5

lifes = 3
scores = 0

bg = pygame.transform.scale((pygame.image.load('background.png').convert()), screen)
bg_x = 0
bg_x2 = bg.get_width()
bg_speed = 2


def create_enemy():
    enemy = pygame.transform.scale_by((pygame.image.load('enemy.png').convert_alpha()), 0.5)
    enemy_rect = pygame.Rect(width + enemy.get_width(), random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(3,6)
    return [enemy, enemy_rect , enemy_speed]


def create_bonus():
    bonus = pygame.transform.scale_by((pygame.image.load('bonus.png').convert_alpha()), 0.4)
    bonus_rect = pygame.Rect(random.randint(0 + int(bonus.get_width() / 2), width - int(bonus.get_width()/2)), -bonus.get_height(), *bonus.get_size())
    bonus_speed = 3
    return [bonus, bonus_rect , bonus_speed]


def create_life_bonus():
    life_bonus = pygame.transform.scale_by((pygame.image.load('life.png').convert_alpha()), 0.05)
    life_bonus_rect = pygame.Rect(random.randint(0 + int(life_bonus.get_width()/2), width - int(life_bonus.get_width()/2)), -life_bonus.get_height(), *life_bonus.get_size())
    life_bonus_speed = 3
    return [life_bonus, life_bonus_rect , life_bonus_speed]


def create_bullet():
    bullet = pygame.transform.scale_by((pygame.image.load('bullet.png').convert_alpha()), 0.04)
    bullet_rect = pygame.Rect(player_rect[0] + player.get_width() / 2 , player_rect[1] + player.get_height() / 2, *bullet.get_size())
    bullet_speed = 10
    return [bullet, bullet_rect , bullet_speed]



font1 = pygame.font.SysFont('Helvetika', 36)
font2 = pygame.font.SysFont('Helvetika', 100)
died_ind = font2.render("YOU DIED", 1, (180, 0, 0))
win_ind = font2.render("YOU WIN", 1, (0, 180, 0))


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY,1000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 225)

CREATE_LIFE_BONUS = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_LIFE_BONUS, 15000)

enemys = []
bonuses = []
bullets = []
life_bonuses = []

image_index = 0

is_working = True

while is_working:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemys.append(create_enemy())
        
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        if event.type == CREATE_LIFE_BONUS:
            life_bonuses.append(create_life_bonus())
        
        if event.type == CHANGE_IMAGE:
            image_index += 1
            if image_index == len(player_imgs):
                image_index = 0
            player = player_imgs[image_index]

        if event.type == pygame.KEYDOWN: 
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if len(bullets) <= 5:
                    bullets.append(create_bullet())

    
    pressed_keys = pygame.key.get_pressed()


    bg_x -= bg_speed
    bg_x2 -= bg_speed

    if bg_x < -bg.get_width():
        bg_x = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_surface.blit(bg,(bg_x,0))
    main_surface.blit(bg,(bg_x2,0))
    main_surface.blit(player,player_rect)

    for enemy in enemys:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0],enemy[1])
        
        if enemy[1].right <= 0 :
            enemys.pop(enemys.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            enemys.pop(enemys.index(enemy))
            lifes -= 1
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0],bonus[1])
        
        if bonus[1].top >= heigth :
            bonuses.pop(bonuses.index(bonus))
        
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 10
    
    for life_bonus in life_bonuses:
        life_bonus[1] = life_bonus[1].move(0, life_bonus[2])
        main_surface.blit(life_bonus[0],life_bonus[1])
        
        if life_bonus[1].top >= heigth :
            life_bonuses.pop(life_bonuses.index(life_bonus))
        
        if player_rect.colliderect(life_bonus[1]):
            life_bonuses.pop(life_bonuses.index(life_bonus))
            lifes += 1


    for bullet in bullets:
        bullet[1] = bullet[1].move(bullet[2],0)
        main_surface.blit(bullet[0],bullet[1])
        
        if bullet[1].left >= width :
            bullets.pop(bullets.index(bullet))
        
        for enemy in enemys: 
            if bullet[1].colliderect(enemy[1]):
                bullets.pop(bullets.index(bullet))
                enemys.pop(enemys.index(enemy))
                scores += 5



    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move((0, player_speed))

    if pressed_keys[K_UP] and not player_rect.top <= 0 :
        player_rect = player_rect.move((0, -player_speed))

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move((-player_speed,0))

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move((player_speed,0))
    
    if pressed_keys[K_ESCAPE]:
        is_working = False
       

    if lifes < 0:
        mixer.music.pause()
        mixer.music.load('loose.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play()
        main_surface.fill(BLACK)
        main_surface.blit(died_ind, (width/2 - win_ind.get_width()/2 ,  heigth/2 - win_ind.get_height()/2))
        pygame.display.flip()
        time.sleep(5)
        is_working = False

    if scores >= 100:
        mixer.music.pause()
        mixer.music.load('victory.mp3')
        mixer.music.set_volume(0.2)
        mixer.music.play()
        main_surface.fill(BLACK)
        main_surface.blit(win_ind, (width/2 - win_ind.get_width()/2 ,  heigth/2 - win_ind.get_height()/2))
        pygame.display.flip()
        time.sleep(5)
        is_working = False


    score_ind = font1.render('score: ' + str(scores), 1, (0, 250, 125))
    main_surface.blit(score_ind, (10, 10))

    life_ind = font1.render('life: ' + str(lifes), 1, (250, 0, 125))
    main_surface.blit(life_ind, (width-100, 10))
    
    pygame.display.flip()

    

