import pygame
from settings import *
from load_image import *
from Animated import *
from Text import *


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.ammo_bar_rect = pygame.Rect(30, 30, 140, 20)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, "BLACK", bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)

    # Выводим полоски здоровья и патронов и счет
    def display(self, player):
        self.show_bar(player.health, player.stats.get("health"), self.health_bar_rect, "RED")
        self.show_bar(player.clip, player.stats.get("clip"), self.ammo_bar_rect, "YELLOW")
        Text(str(player.score), 15, "white", 20, 20, (50, 50), all_sprites)

