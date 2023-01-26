from settings import *
from Tile import *
from Player import *


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "#":
                Tile("brick", x, y, obstacle_sprites)
            elif level[y][x] == ".":
                Tile("stone", x, y)
            elif level[y][x] == "@":
                Tile("stone", x, y)
                sx, sy = x, y
    new_player = Player(sx, sy)
    return new_player, x, y