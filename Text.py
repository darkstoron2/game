from settings import *
import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height, coords, *group):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self, *group)
        screen = pygame.display.get_surface()
        self.text = text
        self.font = pygame.font.SysFont("Arial", size)
        self.textSurf = self.font.render(text, True, color)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        screen.blit(self.textSurf, coords)
        self.rect = self.rect.move(coords)

    # Проверяем нажатие
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            return self.text