import pygame
from settings import *
from load_image import *


tile_images = {
    'stone': load_image('Stone.png'),
    'brick': load_image('Brick.png')
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *group):
        super().__init__(all_sprites, *group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect(topleft=(pos_x * tile_width, pos_y * tile_height))