import math
import random
import pygame as py
from pygame.sprite import spritecollideany

from Perso import Perso
from Rock import Rock
from Coin import Coin

class InGame():
    def __init__(self):
        py.init()

        self.clock = py.time.Clock()
        self.run = True

        self.FrameHeight = 720
        self.FrameWidth = 1280

        self.dt = 0
        self.player_pos = 2

        self.spawn_timer = 0
        self.spawn_interval = 10

        self.font = py.font.SysFont(None, 36)
        self.text_color = (255, 255, 255)

        # PYGAME FRAME WINDOW
        py.display.set_caption("AceVentura")
        self.screen = py.display.set_mode((self.FrameWidth, self.FrameHeight))

        # IMAGE
        self.bg = py.image.load("assets/Fond_Final.png").convert()

        # CREATE INSTANCE OF OBJECT CLASS
        self.perso = Perso(["assets/AceVenturaCharacterRaft_big.png", "assets/AceVenturaCharacter_2.png",
                       "assets/AceVenturaCharacter_3.png"], 200, 200)

        # CREATE GROUPS
        self.all_sprites_group = py.sprite.Group()
        self.caillou_group = py.sprite.Group()
        self.coin_group = py.sprite.Group()
        self.ennemy_group = py.sprite.Group()

        self.frame_index = 0

        # ADD SPRITES TO GROUP
        self.all_sprites_group.add(self.perso)

        self.pause_duration = 200
        self.last_move_time = py.time.get_ticks()

        self.scroll = 0

        # CHANGE THE BELOW 1 TO UPPER NUMBER IF
        # YOU GET BUFFERING OF THE IMAGE
        # HERE 1 IS THE CONSTANT FOR REMOVING BUFFERING
        self.tiles = math.ceil(self.FrameWidth / self.bg.get_width()) + 3

    def generate_random_objects(self,group, class_type, image_path, width, height):
        if random.randint(1, 100) < 50:
            new_object = class_type(image_path, width, height)
            if not spritecollideany(new_object, self.all_sprites_group):
                group.add(new_object)
                self.ennemy_group.add(new_object)
                self.all_sprites_group.add(new_object)

    def update(self):
        self.clock.tick(50)

        # APPENDING THE IMAGE TO THE BACK
        # OF THE SAME IMAGE
        i = 0
        while (i < self.tiles):
            self.screen.blit(self.bg, (self.bg.get_width() * i + self.scroll, 0))
            i += 1
        # FRAME FOR SCROLLING
        self.scroll -= 6

        # RESET THE SCROLL FRAME
        if abs(self.scroll) > self.bg.get_width():
            scroll = 0

        # CLOSING THE FRAME OF SCROLLING
        for event in py.event.get():
            if event.type == py.QUIT:
                self.run = False

        # GESTION ENTREE FLECHE ET POSITION PERSO
        keys = py.key.get_pressed()
        current_time = py.time.get_ticks()
        if keys[py.K_z] and self.player_pos > 1 and current_time - self.last_move_time > self.pause_duration:
            self.player_pos -= 1
            self.last_move_time = current_time

        if keys[py.K_s] and self.player_pos < 3 and current_time - self.last_move_time > self.pause_duration:
            self.player_pos += 1
            self.last_move_time = current_time

        if self.player_pos == 1:
            self.perso.rect.topleft = (100, 200)
        if self.player_pos == 2:
            self.perso.rect.topleft = (100, 350)
        if self.player_pos == 3:
            self.perso.rect.topleft = (100, 480)

        # UPDATE ALL SPRITES
        self.perso.update()
        self.ennemy_group.update()
        self.screen.blit(self.perso.image, self.perso.rect)

        # GÉNÉRATION DE NOUVEAUX OBJETS À INTERVALLES RÉGULIERS
        self.spawn_timer += self.dt
        if self.spawn_timer >= self.spawn_interval:
            while True:
                choice = random.randint(1, 10)
                if choice >= 1 or choice <= 8:
                    type_rock = random.randint(1, 3)
                    if type_rock == 1:
                        self.generate_random_objects(self.caillou_group, Rock, "assets/rocks (1).PNG", 50, 50)
                    elif type_rock == 2:
                        self.generate_random_objects(self.caillou_group, Rock, "assets/rocks (2).PNG", 50, 50)
                    else:
                        self.generate_random_objects(self.caillou_group, Rock, "assets/rocks (3).PNG", 50, 50)
                    self.spawn_timer = 0

                if choice == 9:
                    bonus = random.randint(1, 4)
                    if bonus == 1:
                        path = "assets/BleuDiamond.png"
                    elif bonus == 2:
                        path = "assets/GreenDiamond.png"
                    elif bonus == 3:
                        path = "assets/PurpelDiamond.png"
                    else:
                        path = "assets/RedDiamond.png"
                    self.generate_random_objects(self.coin_group, Coin, path, 50, 50)
                    self.spawn_timer = 0

                if choice == 10:
                    pass
                break

        # GESTION DES COLLISIONS
        for caillou in self.caillou_group:
            if self.perso.rect.colliderect(caillou.rect):
                print("Collision!")
                self.perso.lives -= 1

                if self.perso.lives <= 0:
                    print("Game Over! You ran out of lives.")
                    self.perso.game_over = True
                    self.ennemy_group.empty()
                else:
                    self.perso.image.set_alpha(158)
                    self.perso.start_blinking()

                caillou.rect.x = -1000

        if self.perso.over:
            print("ici")
            self.run = False

        for coin in self.coin_group:
            if self.perso.rect.colliderect(coin.rect):
                print("+1 point")
                self.perso.points += 1
                coin.rect.x = -1000

        # AFFICHAGE VIE ET POINT
        if self.perso.lives > 0:
            heart = py.image.load("assets/heart.png").convert_alpha()
            heart = py.transform.scale(heart, (30, 30))
            for i in range(self.perso.lives):
                self.screen.blit(heart, (self.FrameWidth - (70 + 30 * i), 20))

            points_text = self.font.render(f"Points: {self.perso.points}", True, self.text_color)
            self.screen.blit(points_text, (self.FrameWidth - 150, 50))

        # DRAW ALL SPRITES
        self.ennemy_group.draw(self.screen)

        # LIMITS FPS TO 50
        self.dt = self.clock.tick(50)

        py.display.flip()
        py.display.update()


    def run_game(self):
        while self.run:
            self.update()
        py.quit()

game_instance = InGame()
game_instance.run_game()
