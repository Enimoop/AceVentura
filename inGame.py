import math
import random
import pygame as py
from pygame.sprite import spritecollideany

from Perso import Perso
from Rock import Rock
from Coin import Coin


def generate_random_objects(group, class_type, image_path, width, height):
    if random.randint(1, 100) < 50:
        new_object = class_type(image_path, width, height)
        #while spritecollideany(new_object,ennemy_group):
            #new_object.rect.x += new_object.rect.width
        if not spritecollideany(new_object,ennemy_group):
            group.add(new_object)
            ennemy_group.add(new_object)
            all_sprites_group.add(new_object)

py.init()

clock = py.time.Clock()
run = True

FrameHeight = 720
FrameWidth = 1280

dt = 0
player_pos = 2

rock_spawn_timer = 0
rock_spawn_interval = 10

coin_spawn_timer = 0
coin_spawn_interval = 10

spawn_timer = 0
spawn_interval = 10

recent_rock_positions = []
recent_coin_positions = []

font = py.font.SysFont(None, 36)
text_color = (255, 255, 255)

# PYGAME FRAME WINDOW 
py.display.set_caption("AceVentura")
screen = py.display.set_mode((FrameWidth, FrameHeight))

# IMAGE 
bg = py.image.load("include/Fond.png").convert()

# CREATE INSTANCE OF OBJECT CLASS
perso = Perso("include/AceVentura.png", 100, 100)
caillou = Rock("include/pierre.png", 50, 50)
coin = Coin("include/coin.png", 50, 50)

# CREATE GROUPS
all_sprites_group = py.sprite.Group()
caillou_group = py.sprite.Group()
coin_group = py.sprite.Group()
ennemy_group = py.sprite.Group()



# ADD SPRITES TO GROUP
all_sprites_group.add(perso)

caillou_group.add(caillou)
all_sprites_group.add(caillou)

coin_group.add(coin)
all_sprites_group.add(coin)


pause_duration = 200
last_move_time = py.time.get_ticks()

scroll = 0

# CHANGE THE BELOW 1 TO UPPER NUMBER IF
# YOU GET BUFFERING OF THE IMAGE
# HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth / bg.get_width()) + 1


# MAIN LOOP
while run:
    # speed du scrolling
    clock.tick(30)

    # APPENDING THE IMAGE TO THE BACK
    # OF THE SAME IMAGE
    i = 0
    while (i < tiles):
        screen.blit(bg, (bg.get_width() * i + scroll, 0))
        i += 1
    # FRAME FOR SCROLLING
    scroll -= 6

    # RESET THE SCROLL FRAME
    if abs(scroll) > bg.get_width():
        scroll = 0

    # CLOSING THE FRAME OF SCROLLING
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False


    #GESTION ENTREE FLECHE ET POSITION PERSO
    keys = py.key.get_pressed()
    current_time = py.time.get_ticks()
    if keys[py.K_z] and player_pos > 1 and current_time - last_move_time > pause_duration:
        player_pos -= 1
        last_move_time = current_time
    if keys[py.K_s] and player_pos < 3 and current_time - last_move_time > pause_duration:
        player_pos += 1
        last_move_time = current_time

    if player_pos == 1:
        perso.rect.topleft = (100,280)
    if player_pos == 2:
        perso.rect.topleft = (100,400)
    if player_pos == 3:
        perso.rect.topleft = (100,550)

    screen.blit(perso.image, perso.rect)

    # UPDATE ALL SPRITES
    perso.update()
    ennemy_group.update()

    # DRAW ALL SPRITES
    ennemy_group.draw(screen)

    # GÉNÉRATION DE NOUVEAUX OBJETS À INTERVALLES RÉGULIERS
    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        while True:
                choice = random.randint(1, 3)
                if choice == 1:
                    generate_random_objects(caillou_group, Rock, "include/pierre.png", 50, 50)
                    spawn_timer = 0
                if choice == 2:
                    generate_random_objects(coin_group, Coin, "include/coin.png", 50, 50)
                    spawn_timer = 0
                if choice == 3:
                    pass
                break




    #generate_random_objects(caillou_group, Rock, "include/pierre.png", 50, 50)
    #generate_random_objects(coin_group, Coin, "include/coin.png", 50, 50)


    #CAILLOU
    #rock_spawn_timer += dt
    #if rock_spawn_timer >= rock_spawn_interval:
        #while True:
            #if random.randint(1, 100) < 30:
                #new_caillou = Rock("include/pierre.png", 50, 50)
                #caillou_group.add(new_caillou)
                #all_sprites_group.add(new_caillou)
                #rock_spawn_timer = 0
                #recent_rock_positions.append(new_caillou.rect.y)
                #recent_rock_positions = recent_rock_positions[-3:]
                #break

    for caillou in caillou_group:
        if perso.rect.colliderect(caillou.rect):
            print("Collision with rock! Game Over!")
            perso.lives -= 1
            if perso.lives <= 0:
                print("Game Over! You ran out of lives.")
                run = False
                py.quit()

            caillou.rect.x = -1000

    #COIN
    #coin_spawn_timer += dt
    #if coin_spawn_timer >= coin_spawn_interval:
        #while True:
            #if random.randint(1, 100) < 30:
                #new_coin = Coin("include/coin.png", 50, 50)
                #coin_group.add(new_coin)
                #all_sprites_group.add(new_coin)
                #coin_spawn_timer = 0
                #recent_coin_positions.append(new_coin.rect.y)
                #recent_coin_positions = recent_coin_positions[-3:]
                #break

    for coin in coin_group:
        if perso.rect.colliderect(coin.rect):
            print("+1 point")
            perso.points += 1

            coin.rect.x = -1000

    lives_text = font.render(f"Lives: {perso.lives}", True, text_color)
    screen.blit(lives_text, (FrameWidth - 150, 20))

    points_text = font.render(f"Points: {perso.points}", True, text_color)
    screen.blit(points_text, (FrameWidth - 150, 50))

    # LIMITS FPS TO 60
    dt = clock.tick(60)

    py.display.flip()
    py.display.update()

py.quit()
