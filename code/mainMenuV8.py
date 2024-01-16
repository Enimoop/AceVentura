import pygame
import sys
import pygame_gui

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

VOLUME_SLIDER_EVENT = pygame.USEREVENT + 1



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

# Charger l'image du logo Ventura
logo_ventura_image = pygame.image.load('asset/logoVentura.png')

# Définir les polices
mainMenuFont = 'font/Crang.ttf'
font = pygame.font.Font(mainMenuFont, 55)

# Variable pour stocker le décalage des boutons
button_offset = 0

volume_slider_rect = pygame.Rect((SCREEN_SIZE[0] / 2 + 650, SCREEN_SIZE[1] / 2 + 22), (300, 30))

class Button:
    def __init__(self, text, y, font_path, action=None, x_offset=0):
        self.text = text
        self.y = y
        self.action = action
        self.font_normal = pygame.font.Font(font_path, FONT_SIZE_NORMAL)
        self.font_zoomed = pygame.font.Font(font_path, FONT_SIZE_ZOOMED)
        text_surface = self.font_normal.render(self.text, True, TEXT_COLOR)
        self.w, self.h = text_surface.get_size()
        self.w += 20
        self.h += 20
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2
        self.x_offset = x_offset  # Définir le décalage supplémentaire en x

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
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2 - button_offset + self.x_offset

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

def shift_buttons_left():
    global button_offset
    button_offset = 800
    # Mettre à jour la position du slider
    volume_slider.set_relative_position((volume_slider_rect.x - button_offset, volume_slider_rect.y))

def shift_buttons_right():
    global button_offset
    button_offset = 0
    # Remettre le slider à sa position d'origine
    volume_slider.set_relative_position((volume_slider_rect.x, volume_slider_rect.y))

def jouer():
    print("Jouer")

def parametres():
    print("Paramètres")
    shift_buttons_left()

def quitter():
    print("Quitter")
    pygame.quit()
    sys.exit()

def retour():
    print("Retour")
    shift_buttons_right()

def Son():
    print("Son")

# Créer un UIManager
ui_manager = pygame_gui.UIManager(SCREEN_SIZE)

volume_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=volume_slider_rect,
    start_value=pygame.mixer.music.get_volume(),
    value_range=(0.0, 1.0),
    manager=ui_manager
)

def volume_slider_callback(value):
    pygame.event.post(pygame.event.Event(VOLUME_SLIDER_EVENT, value=value))

# Texte du menu
menu_items = [
    Button("Jouer", SCREEN_SIZE[1] / 2 - MESSAGE_SPACING, mainMenuFont, jouer),
    Button("Paramètres", SCREEN_SIZE[1] / 2, mainMenuFont, parametres),
    Button("Quitter", SCREEN_SIZE[1] / 1.9 + MESSAGE_SPACING, mainMenuFont, quitter),
    Button("Retour", SCREEN_SIZE[1] / 1.9 + MESSAGE_SPACING, mainMenuFont, retour, x_offset=800),
    Button("Son", SCREEN_SIZE[1] / 2 - MESSAGE_SPACING, mainMenuFont, Son, x_offset=800)

]

while True:
    time_delta = pygame.time.get_ticks() / 1000.0
    ecran.fill(RECTANGLE_COLOR)
    ecran.blit(background_image, (0, 0))
    ecran.blit(bbackground_menu, BACKGROUND_MENU_POSITION)
    ecran.blit(logo_ventura_image, (220, -10))
    
    # Obtenir la position de la souris
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for button in menu_items:
        button.draw(ecran, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

    # Gérer les événements
    for event in pygame.event.get():
        # Mettre à jour l'interface utilisateur avec les événements
        ui_manager.process_events(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bouton gauche de la souris
                for button in menu_items:
                    if button.mouse_over_button(event.pos[0], event.pos[1]):
                        button.click()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == volume_slider:
                    pygame.mixer.music.set_volume(event.value)

    # Mettre à jour l'interface utilisateur
    ui_manager.update(time_delta)

    # Dessiner l'interface utilisateur
    ui_manager.draw_ui(ecran)

    # Mettre à jour l'écran
    pygame.display.update()