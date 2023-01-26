from math import atan2, pi, degrees

from settings import *
from Tile import *
from load_image import *
from Animated import *
from ProjectTile import *
import pygame


class Player(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__({"idle": (load_image("idle.png"), 1),
                          "run": (load_image("run.png"), 3),
                          "jump": (load_image("jump.png"), 4),
                          "shoot": (load_image("shoot.png"), 2),
                          "reload": (load_image("reload.png"), 2),
                          "death": (load_image("death.png"), 5)})
        # Харрактеристики героя
        self.score = 0
        self.stats = {"health": 100, "clip": 10, "speed": 7}
        player_group.add(self)
        all_sprites.add(self)
        self.rect = self.image.get_rect(topleft=(pos_x * tile_width, pos_y * tile_height))
        self.direction = pygame.math.Vector2()
        self.new_move = ""
        self.clip = self.stats.get("clip")
        self.speed = self.stats.get("speed")
        self.health = self.stats.get("health")

    def update(self):
        # Проверяем на смерть
        if self.status != "death":
            self.move()
            self.change_status()
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
        self.new_frame(direction=self.direction)

    # Меняем цвет и уменьшаем хп при ударе
    def get_damage(self):
        self.health -= 10
        color = pygame.Color(255, 0, 0)
        image = self.image.copy()
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                color.a = image.get_at((x, y)).a
                image.set_at((x, y), color)
        self.image = image

    # Изменяем статус
    def change_status(self):
        # Если есть длинная анимация, то она состояние
        if self.long_anim_status != "":
            self.status = self.long_anim_status
        # Если нет длинной анимации, но есть новое действие, то состояние заменяется на новое действие
        elif self.long_anim_status == "" and self.new_move != "":
            self.long_anim_status = self.new_move
            self.status = self.new_move
            self.long_anim_time = len(self.frames.get(self.long_anim_status))
            self.cur_frame = 0
            if self.long_anim_status == "shoot":
                self.shoot()
            elif self.long_anim_status == "reload":
                self.clip = 10
        # Если нет нового действие задействующее долгую анимацию то ставим обычное состояние
        elif self.status != "idle" and self.direction.x == 0 and self.direction.y == 0:
            self.status = "idle"
            self.cur_frame = 0
        elif self.status != "run" and (self.direction.x != 0 or self.direction.y != 0):
            self.status = "run"
            self.cur_frame = 0

    # Выстрел
    def shoot(self):
        # Проверяем есть ли в обойме патроны
        if self.clip != 0:
            self.clip -= 1
            # Вычисляем направление движения пули
            mouse_pos = pygame.mouse.get_pos()
            enemy_vac = pygame.math.Vector2(self.rect.center)
            player_vac = pygame.math.Vector2(mouse_pos)
            direction = (player_vac - enemy_vac).normalize()
            dx = mouse_pos[0] - self.rect.center[0]
            dy = mouse_pos[1] - self.rect.center[1]
            # Вычисляем угол под которым летит пуля относительно стартовой позиции
            rads = atan2(-dy, dx)
            rads %= 2 * pi
            angle = degrees(rads)
            ProjectTile(self.rect.center, direction, angle)

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == "vertical":
            for sprite in obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def move(self):
        keys = pygame.key.get_pressed()
        # Проверяем на новое движение
        if self.health <= 0:
            self.new_move = "death"
        elif keys[pygame.K_SPACE]:
            self.new_move = "jump"
        elif pygame.mouse.get_pressed()[0]:
            self.new_move = "shoot"
        elif keys[pygame.K_r]:
            self.new_move = "reload"
        else:
            self.new_move = ""
        # Выбираем направление движения
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # Проверяем столкновение по вертикали и горизонтали
        self.rect.x += self.direction.x * self.speed
        self.collision("horizontal")
        self.rect.y += self.direction.y * self.speed
        self.collision("vertical")