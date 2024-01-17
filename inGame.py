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
        if not spritecollideany(new_object, all_sprites_group):
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


font = py.font.SysFont(None, 36)
text_color = (255, 255, 255)

# PYGAME FRAME WINDOW 
py.display.set_caption("AceVentura")
screen = py.display.set_mode((FrameWidth, FrameHeight))

# IMAGE 
bg = py.image.load("assets/Fond.png").convert()

# CREATE INSTANCE OF OBJECT CLASS
perso = Perso(["assets/AceVenturaCharacterRaft_big.png", "assets/AceVenturaCharacter_2.png",
               "assets/AceVenturaCharacter_3.png"], 200, 200)



# CREATE GROUPS
all_sprites_group = py.sprite.Group()
caillou_group = py.sprite.Group()
coin_group = py.sprite.Group()
ennemy_group = py.sprite.Group()

frame_index = 0

# ADD SPRITES TO GROUP
all_sprites_group.add(perso)



pause_duration = 200
last_move_time = py.time.get_ticks()

scroll = 0

# CHANGE THE BELOW 1 TO UPPER NUMBER IF
# YOU GET BUFFERING OF THE IMAGE
# HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING
tiles = math.ceil(FrameWidth / bg.get_width()) + 3


# MAIN LOOP
while run:
    # speed du scrolling
    clock.tick(40)

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
        perso.rect.topleft = (100,200)
    if player_pos == 2:
        perso.rect.topleft = (100,350)
    if player_pos == 3:
        perso.rect.topleft = (100,480)


    # UPDATE ALL SPRITES
    perso.update()
    ennemy_group.update()
    screen.blit(perso.image, perso.rect)


    # GÉNÉRATION DE NOUVEAUX OBJETS À INTERVALLES RÉGULIERS
    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        while True:
                choice = random.randint(1, 5)
                if choice == 1 or choice == 2 or choice == 3:
                    type_rock = random.randint(1,3)
                    if type_rock == 1:
                        generate_random_objects(caillou_group, Rock, "assets/rocks (1).PNG", 50, 50)
                    elif type_rock == 2:
                        generate_random_objects(caillou_group, Rock, "assets/rocks (2).PNG", 50, 50)
                    else:
                        generate_random_objects(caillou_group, Rock, "assets/rocks (3).PNG", 50, 50)
                    spawn_timer = 0

                if choice == 4:
                    if random.randint(1,2) == 1:
                        path = "assets/coin.png"
                    else:
                        path = "assets/strawberry.png"
                    generate_random_objects(coin_group, Coin, path, 50, 50)
                    spawn_timer = 0

                if choice == 5:
                    pass
                break




    for caillou in caillou_group:
        if perso.rect.colliderect(caillou.rect):
            print("Collision!")
            perso.lives -= 1
            if perso.lives <= 0:
                print("Game Over! You ran out of lives.")
                perso.game_over = True
                ennemy_group.empty()
            else:
                perso.image.set_alpha(158)
                perso.start_blinking()

            caillou.rect.x = -1000

    for coin in coin_group:
        if perso.rect.colliderect(coin.rect):
            print("+1 point")
            perso.points += 1

            coin.rect.x = -1000

    if perso.lives > 0:
        lives_text = font.render(f"Lives: {perso.lives}", True, text_color)
        screen.blit(lives_text, (FrameWidth - 150, 20))

        points_text = font.render(f"Points: {perso.points}", True, text_color)
        screen.blit(points_text, (FrameWidth - 150, 50))



    # DRAW ALL SPRITES
    ennemy_group.draw(screen)

    # LIMITS FPS TO 50
    dt = clock.tick(50)

    py.display.flip()
    py.display.update()

py.quit()
