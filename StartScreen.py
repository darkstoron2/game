from load_image import *
import sys
import pygame
from settings import *
from Text import *


def start_screen(screen):
    def terminate():
        pygame.quit()
        sys.exit()

    class StartScreen(pygame.sprite.Sprite):
        image = load_image("startscreen.jpg")

        def __init__(self, *group):
            super().__init__(*group)
            self.image = StartScreen.image
            self.rect = self.image.get_rect()

    StartScreen(start_screen_group)
    start_screen_group.draw(screen)
    running = True
    # Текст
    map1 = Text("Играть на первой карте", 50, "white", 500, 100, (700, 400), buttons_group)
    map2 = Text("Играть на второй карте", 50, "white", 700, 100, (700, 500), buttons_group)
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверяем выбор карты игрока
                for s in buttons_group:
                    if s.check_click(event.pos):
                        if s.text == "Играть на первой карте":
                            return "map.txt"
                        return "map2.txt"
