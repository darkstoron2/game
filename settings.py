import pygame

clock = pygame.time.Clock()
tile_width = tile_height = 128
size = width, height = 1200, 720
FPS = 30
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
projectile_sprites = pygame.sprite.Group()
start_screen_group = pygame.sprite.Group()
text_group = pygame.sprite.Group()
buttons_group = pygame.sprite.Group()
