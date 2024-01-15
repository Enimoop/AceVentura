import pygame
import sys

pygame.init()

SCREEN_SIZE = (1280, 720)
ecran = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Menu Principal Ace Ventura - The Game")

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BUTTON = (0, 0, 0,0)
COULEUR_PRESSE = (20, 200, 200)

background_image = pygame.image.load('asset/backGroundMainMenue.png')

mainMenuFont = 'font/Crang.ttf'
font = pygame.font.Font(mainMenuFont, 55)

menu_items = ["Jouer", "Paramètres", "Quitter"]

def draw_button(text, font, color, surface, x, y, w, h, zoom, presse):
    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)  
    button_surface.fill(BUTTON)  
    surface.blit(button_surface, (x, y))

    zoom_factor = 1.1 if zoom else 1
    text_color = COULEUR_PRESSE if presse else color

    font_size = int(55 * zoom_factor)
    zoomed_font = pygame.font.Font(mainMenuFont, font_size)
    textobj = zoomed_font.render(text, True, text_color)

    textrect = textobj.get_rect()
    textrect.center = (x + w / 2, y + h / 2)
    surface.blit(textobj, textrect)

def mouse_over_button(mouse_x, mouse_y, x, y, w, h):
    return x <= mouse_x <= x + w and y <= mouse_y <= y + h

def calculer_largeur_bouton(text, font):
    textobj = font.render(text, True, BLANC)
    return textobj.get_rect().width + 40

while True:
    ecran.fill(NOIR)
    ecran.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                for i, item in enumerate(menu_items):
                    bouton_x = SCREEN_SIZE[0] / 2 - bouton_largeur / 2
                    bouton_y = SCREEN_SIZE[1] / 2 - 30 + 60 * i - bouton_hauteur / 2
                    if mouse_over_button(event.pos[0], event.pos[1], bouton_x, bouton_y, bouton_largeur, bouton_hauteur):
                        print(f"Bouton cliqué: {item}")

    mouse_x, mouse_y = pygame.mouse.get_pos()

    bouton_largeur = 200
    bouton_hauteur = 50
    espace_entre_boutons = 80
    bouton_presse = None
    if pygame.mouse.get_pressed()[0]:  
        for i, item in enumerate(menu_items):
            bouton_largeur = calculer_largeur_bouton(item, font)  
            bouton_x = SCREEN_SIZE[0] / 2 - bouton_largeur / 2  
            bouton_y = SCREEN_SIZE[1] / 2 - 65 + espace_entre_boutons * i - bouton_hauteur / 2
            if mouse_over_button(mouse_x, mouse_y, bouton_x, bouton_y, bouton_largeur, bouton_hauteur):
                bouton_presse = i
                break
            
    for i, item in enumerate(menu_items):
        bouton_x = SCREEN_SIZE[0] / 2 - bouton_largeur / 2
        bouton_y = SCREEN_SIZE[1] / 2 - 65 + espace_entre_boutons * i - bouton_hauteur / 2
        zoom = mouse_over_button(mouse_x, mouse_y, bouton_x, bouton_y, bouton_largeur, bouton_hauteur)
        presse = (i == bouton_presse)
        draw_button(item, font, BLANC, ecran, bouton_x, bouton_y, bouton_largeur, bouton_hauteur, zoom, presse)

    pygame.display.update()
