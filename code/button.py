import pygame
from config import *

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
        self.horizontal_offset = 0  # Nouvel attribut pour le décalage horizontal

        
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
        self.x = SCREEN_SIZE[0] / 2 - self.w / 2 - self.horizontal_offset + self.x_offset

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