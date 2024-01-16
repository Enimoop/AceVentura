import pygame
import sys

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
SCREEN_SIZE = (1280, 720)
ecran = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Menu Principal Ace Ventura - The Game")

# Définir les couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
BUTTON = (0, 0, 0,0)
COULEUR_PRESSE = (20, 200, 200)

# Definir le fond d'écran
background_image = pygame.image.load('asset/backGroundMainMenue.png')

# Définir les polices
mainMenuFont = 'font/Crang.ttf'
font = pygame.font.Font(mainMenuFont, 55)

# Texte du menu
menu_items = ["Jouer", "Paramètres", "Quitter"]

# Fonction pour dessiner le bouton
def draw_button(text, font, color, surface, x, y, w, h, zoom, presse):
    # Dessiner le rectangle du bouton (pas de zoom appliqué ici)
    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)  # SRCALPHA pour la transparence
    button_surface.fill(BUTTON)  # Remplir avec la couleur désirée
    surface.blit(button_surface, (x, y))

    # Appliquer l'effet de zoom seulement sur le texte
    zoom_factor = 1.1 if zoom else 1
    text_color = COULEUR_PRESSE if presse else color

    # Créer un texte zoomé
    font_size = int(55 * zoom_factor)
    zoomed_font = pygame.font.Font(mainMenuFont, font_size)
    textobj = zoomed_font.render(text, True, text_color)

    # Ajuster la position du texte pour le centrer
    textrect = textobj.get_rect()
    textrect.center = (x + w / 2, y + h / 2)
    surface.blit(textobj, textrect)

# Fonction pour vérifier si la souris est sur le bouton
def mouse_over_button(mouse_x, mouse_y, x, y, w, h):
    return x <= mouse_x <= x + w and y <= mouse_y <= y + h

def calculer_largeur_bouton(text, font):
    textobj = font.render(text, True, BLANC)
    return textobj.get_rect().width + 40

# Boucle principale
while True:
    ecran.fill(NOIR)
    ecran.blit(background_image, (0, 0))

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si le clic est sur l'un des boutons
            if event.button == 1:  # Bouton gauche de la souris
                for i, item in enumerate(menu_items):
                    bouton_x = SCREEN_SIZE[0] / 2 - bouton_largeur / 2
                    bouton_y = SCREEN_SIZE[1] / 2 - 30 + 60 * i - bouton_hauteur / 2
                    if mouse_over_button(event.pos[0], event.pos[1], bouton_x, bouton_y, bouton_largeur, bouton_hauteur):
                        print(f"Bouton cliqué: {item}")

    # Obtenir la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Dessiner les boutons du menu
    bouton_largeur = 200
    bouton_hauteur = 50
    espace_entre_boutons = 80
    bouton_presse = None
    if pygame.mouse.get_pressed()[0]:  # Bouton gauche de la souris enfoncé
        for i, item in enumerate(menu_items):
            bouton_largeur = calculer_largeur_bouton(item, font)  # Calculer la largeur du bouton en fonction du texte
            bouton_x = SCREEN_SIZE[0] / 2 - bouton_largeur / 2  # Centrer le bouton
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

    
    # Mettre à jour l'écran
    pygame.display.update()


