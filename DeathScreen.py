from load_image import *
import sys
import pygame as pg
from settings import *
from Text import *


def death_screen(screen):
    font = pg.font.Font(None, 32)
    input_box = pg.Rect(600, 360, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    text_death = Text("Введите имя", 50, "white", 500, 100, (500, 360))

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return text
            if event.type == pg.MOUSEBUTTONDOWN:
                # Если нажали на строку
                if input_box.collidepoint(event.pos):
                    # Строка активна
                    active = not active
                else:
                    active = False
                # Сменить цвет есвли строка активна
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        return text
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Рендер текста
        txt_surface = font.render(text, True, color)
        # Изменения размеров окна если текст слишком большой
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Вывод текста
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Вывод окна ввода текста
        pg.draw.rect(screen, color, input_box, 2)
        pg.display.flip()
        text_death = Text("Введите имя", 25, "white", 500, 100, (400, 360))
        pg.display.update()
        clock.tick(30)