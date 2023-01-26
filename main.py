import pygame

pygame.init()
size = width, height = 1200, 720
screen = pygame.display.set_mode(size)


import os
import sys
from load_image import *
from Level import *
from settings import *
from Camera import *
from Animated import *
from Enemy import *
from UI import *
from StartScreen import *
from DeathScreen import *


def game():
    # Узнаем выбранные уровень и загружаем
    level = start_screen(screen)
    screen.fill("black")
    player, level_x, level_y = generate_level(load_level(level))
    ui = UI()
    running = True
    camera = Camera()
    Enemy(5, 4, player)
    Enemy(6, 5, player)
    while running:  # главный игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill("white")
        all_sprites.update()
        all_sprites.draw(screen)
        ui.display(player)
        pygame.display.flip()
        clock.tick(FPS)
        # Если умер то выводим экран смерти
        if player.status == "death" and player.long_anim_time == 0:
            name = death_screen(screen)
            with open("scores.txt", "w") as f:
                f.write(f"{name}: {player.score}")
            pygame.quit()
            sys.exit(0)


while True:
    game()

