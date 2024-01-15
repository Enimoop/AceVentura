import pygame
import sys

# Initialiser Pygame
pygame.init()
# Initialiser le mixer
pygame.mixer.init()

# Définir les dimensions de la fenêtre
SCREEN_SIZE = (1280, 720)
ecran = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Menu Principal Ace Ventura - The Game")

# Définir les tailles de police
FONT_SIZE_NORMAL = 40
FONT_SIZE_ZOOMED = 50

# Définir l'espace entre chaque message
MESSAGE_SPACING = 60

# Définir la couleur/opacité du texte et du rectangle
TEXT_COLOR = (22, 69, 62)
RECTANGLE_COLOR = (0, 0, 0)
COULEUR_PRESSE = (20, 200, 200)
RECTANGLE_COLOR = (0, 0, 0)

# Définir l'opacité
BUTTON_OPACITY = 0  # Set to 0% opacity

# Définir la couleur du texte pressé
PRESSED_TEXT_COLOR = (28, 71, 77)

# Définir la taille de l'image de fond du menu
BACKGROUND_MENU_SIZE = (700, 600)

# Définir la position de l'image de fond du menu
BACKGROUND_MENU_POSITION = (290, 100)

# Charger l'image d'arrière-plan
bbackground_menu = pygame.image.load('asset/backGroudMenu.png')
bbackground_menu = pygame.transform.scale(bbackground_menu, BACKGROUND_MENU_SIZE)

# Charger la musique
pygame.mixer.music.load('music/MenuMusic.mp3')
# Jouer la musique en boucle
pygame.mixer.music.play(-1)

# Charger l'image du logo
logo_image = pygame.image.load('asset/logo32x32.png')
# Définir l'icône de la fenêtre
pygame.display.set_icon(logo_image)

# Definir le fond d'écran
background_image = pygame.image.load('asset/backGroundMainMenue.png')

# Définir les polices
mainMenuFont = 'font/Crang.ttf'
font = pygame.font.Font(mainMenuFont, 55)

class Button:
    def __init__(self, text, y, font_path, action=None):
        self.text = text
        self.y = y
        self.action = action
        self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
        self.font_zoomed = pygame.font.Font(font_path, FONT_SIZE_ZOOMED)
        text_surface = self.font_normal.render(self.text, True, TEXT_COLOR)
        self.w, self.h = text_surface.get_size()  # Get the size of the text
        self.w += 20  # Add some padding
        self.h += 20  # Add some padding
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2  # Center the button

    def draw(self, surface, mouse_x, mouse_y, pressed):
        zoom = self.mouse_over_button(mouse_x, mouse_y)
        press = (pressed and zoom)
        
        if zoom:
            font = self.font_zoomed
        else:
            font = self.font_normal

        text_surface = font.render(self.text, True, TEXT_COLOR)
        self.w, self.h = text_surface.get_size()  # Get the size of the text
        self.w += 20  # Add some padding
        self.h += 20  # Add some padding
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2  # Center the button

        def draw_button(text, font, color, surface, x, y, w, h, press):
            # Create a new surface with the same size as the button
            button_surface = pygame.Surface((w, h))
            
            # Set the opacity of the surface
            button_surface.set_alpha(BUTTON_OPACITY)
            
            # Draw the rectangle on the new surface
            pygame.draw.rect(button_surface, RECTANGLE_COLOR, (0, 0, w, h))
            
            # Draw the new surface on the screen
            surface.blit(button_surface, (x, y))
            
            # Change the color of the text if the button is pressed
            if press:
                text_surface = font.render(text, True, PRESSED_TEXT_COLOR)
            else:
                text_surface = font.render(text, True, color)
            
            text_rect = text_surface.get_rect()
            text_rect.center = (x + w / 2, y + h / 2)
            surface.blit(text_surface, text_rect)
        
        draw_button(self.text, font, TEXT_COLOR, surface, self.x, self.y, self.w, self.h, press)

    def mouse_over_button(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h

    def click(self):
        if self.action:
            self.action()     
            
def jouer():
    print("Jouer")

def parametres():
    print("Paramètres")

def quitter():
    print("Quitter")
    pygame.quit()
    sys.exit()

# Texte du menu
menu_items = [
    Button("Jouer", SCREEN_SIZE[1] / 2 - MESSAGE_SPACING, mainMenuFont, jouer),
    Button("Paramètres", SCREEN_SIZE[1] / 2 , mainMenuFont, parametres),
    Button("Quitter", SCREEN_SIZE[1] / 1.9 + MESSAGE_SPACING, mainMenuFont, quitter)
]

# Boucle principale
while True:
    ecran.fill(RECTANGLE_COLOR)
    ecran.blit(background_image, (0, 0))
    ecran.blit(bbackground_menu, BACKGROUND_MENU_POSITION)

    # Obtenir la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for button in menu_items:
        button.draw(ecran, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bouton gauche de la souris
                for button in menu_items:
                    if button.mouse_over_button(event.pos[0], event.pos[1]):
                        button.click()

    # Mettre à jour l'écran
    pygame.display.update()