import pygame
import sys
from main_menu import MainMenu

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    main_menu = MainMenu((1280, 720))
    main_menu.run()
    pygame.quit()
    sys.exit()
