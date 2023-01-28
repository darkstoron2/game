from settings import *
from random import randint
from Enemy import *
import pygame


def create_enemy(player, spawn_enemy_cooldown):
    seconds = pygame.time.get_ticks() // 1000
    if (spawn_enemy_cooldown - seconds) == 0:
        enemy = Enemy(player.rect.center[0] // tile_width + randint(1, 3),
                      player.rect.center[1] // tile_height + randint(1, 3), player)
        while pygame.sprite.spritecollideany(enemy, obstacle_sprites):
            enemy.kill()
            enemy = Enemy(player.rect.center[0] // tile_width + randint(1, 3),
                          player.rect.center[1] // tile_height + randint(1, 3), player)
        return True
    return False
