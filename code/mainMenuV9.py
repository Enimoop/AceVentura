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

class MainMenu:
    def __init__(self, screen_size):
        # Initialisation de Pygame et des paramètres de base
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Menu Principal Ace Ventura - The Game")

        # Définition des attributs de la classe
        self.font_path = 'font/Crang.ttf'
        self.background_menu_image_path = 'asset/backGroudMenu.png'
        self.logo_image_path = 'asset/logo32x32.png'
        self.background_image_path = 'asset/backGroundMainMenue.png'
        self.logo_ventura_image_path = 'asset/logoVentura.png'
        self.menu_music_path = 'music/MenuMusic.mp3'

        # Charger et configurer les ressources
        self.load_resources()
        self.create_ui_elements(screen_size)
        self.create_buttons()

    def load_resources(self):
        self.background_menu = pygame.image.load(self.background_menu_image_path)
        self.background_menu = pygame.transform.scale(self.background_menu, (700, 600))

        self.logo_image = pygame.image.load(self.logo_image_path)
        pygame.display.set_icon(self.logo_image)

        self.background_image = pygame.image.load(self.background_image_path)
        self.logo_ventura_image = pygame.image.load(self.logo_ventura_image_path)

        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.play(-1)

    def create_ui_elements(self, screen_size):
        self.ui_manager = pygame_gui.UIManager(screen_size)
        self.volume_slider_rect = pygame.Rect((screen_size[0] / 2 + 650, screen_size[1] / 2 + 22), (300, 30))
        self.volume_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=self.volume_slider_rect,
            start_value=pygame.mixer.music.get_volume(),
            value_range=(0.0, 1.0),
            manager=self.ui_manager
        )

    def create_buttons(self):
        self.menu_items = [
            Button("Jouer", self.screen.get_height() / 2 - 60, self.font_path, self.jouer),
            Button("Paramètres", self.screen.get_height() / 2.5 + MESSAGE_SPACING, self.font_path, self.parametres),
            Button("Quitter", self.screen.get_height() / 2.4 + MESSAGE_SPACING * 2, self.font_path, self.quitter),
            Button("Retour", self.screen.get_height() / 1.9 + MESSAGE_SPACING, self.font_path, self.retour, x_offset=800),
            Button("Son", self.screen.get_height() / 2 - MESSAGE_SPACING, self.font_path, self.Son, x_offset=800)
        ]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.background_menu, (290, 100))
        self.screen.blit(self.logo_ventura_image, (220, -10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for button in self.menu_items:
            button.draw(self.screen, mouse_x, mouse_y, pygame.mouse.get_pressed()[0])

        self.ui_manager.draw_ui(self.screen)
        pygame.display.update()

    def update(self, time_delta):
        for event in pygame.event.get():
            self.ui_manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Bouton gauche de la souris
                    for button in self.menu_items:
                        if button.mouse_over_button(event.pos[0], event.pos[1]):
                            button.click()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.volume_slider:
                        pygame.mixer.music.set_volume(event.value)

        self.ui_manager.update(time_delta)
    
    def run(self):
        while True:
            time_delta = pygame.time.get_ticks() / 1000.0
            self.update(time_delta)
            self.draw()

    def shift_buttons_left(self):
        global button_offset
        button_offset = 800
        self.volume_slider.set_relative_position((self.volume_slider_rect.x - button_offset, self.volume_slider_rect.y))


    def shift_buttons_right(self):
        global button_offset
        button_offset = 0
        # Remettre le slider à sa position d'origine
        self.volume_slider.set_relative_position((self.volume_slider_rect.x, self.volume_slider_rect.y))

    def jouer(self):
        print("Jouer")

    def parametres(self):
        print("Paramètres")
        self.shift_buttons_left()

    def quitter(self):
        print("Quitter")
        pygame.quit()
        sys.exit()

    def retour(self):
        print("Retour")
        self.shift_buttons_right()

    def Son(self):
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

# Utilisation de la classe MainMenu
if __name__ == "__main__":
    main_menu = MainMenu((1280, 720))
    main_menu.run()