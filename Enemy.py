from settings import *
from Tile import *
from load_image import *
from Animated import *
import pygame


# Наследуем от анимированного спрайта
class Enemy(AnimatedSprite):
    def __init__(self, pos_x, pos_y, player):
        super().__init__({"idle": (load_image("idle_enemy.png"), 1),
                          "run": (load_image("run_enemy.png"), 8),
                          "attack": (load_image("attack_enemy.png"), 6),
                          "death": (load_image("death_enemy.png"), 2)})
        # Харрактеристики врага
        self.stats = {"health": 50, "speed": 5, "damage_radiuce": 25}
        enemy_sprites.add(self)
        all_sprites.add(self)
        # Добавляем игрока
        self.player = player
        self.rect = self.image.get_rect(topleft=(pos_x * tile_width, pos_y * tile_height))
        self.direction = pygame.math.Vector2()
        self.new_move = ""
        self.speed = self.stats.get("speed")
        self.damage_radiuce = self.stats.get("damage_radiuce")
        self.health = self.stats.get("health")

    def update(self):
        # Проверяем на смерть
        if self.status != "death":
            self.move()
            self.change_status()
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
        self.new_frame(direction=self.direction)
        # Если умер и анимация смерти закончилась, то добавляем счет и убиваем класс
        if self.status == "death" and self.long_anim_time == 0:
            self.player.score += 10
            self.kill()

    # Меняем цвет и уменьшаем хп, если нанесли урон
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
        # Если нет нового действие задействующее долгую анимацию то ставим обычное состояние
        elif self.status != "idle" and self.direction.x == 0 and self.direction.y == 0:
            self.status = "idle"
            self.cur_frame = 0
        elif self.status != "run" and (self.direction.x != 0 or self.direction.y != 0):
            self.status = "run"
            self.cur_frame = 0

    # Проверяем на столкновение
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

    # Находим вектор движения и проверяем может ли монстр атаковать
    def get_distance_direction(self):
        enemy_vac = pygame.math.Vector2(self.rect.center)
        player_vac = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vac - enemy_vac).magnitude()
        # Если дистанция от игрока до врага меньше радиуса атаки, то враг атакует
        if distance > self.damage_radiuce:
            self.direction = (player_vac - enemy_vac).normalize()
            self.new_move = ""
        elif self.long_anim_status != "attack" and distance < self.damage_radiuce:
            self.player.get_damage()
            self.new_move = "attack"

    def move(self):
        # Выбираем новое движение и вектор движения
        self.get_distance_direction()
        if self.health <= 0:
            self.new_move = "death"
        if self.long_anim_status == "":
            # Проверяем столкновение по вертикали и горизонтали
            self.rect.x += self.direction.x * self.speed
            self.collision("horizontal")
            self.rect.y += self.direction.y * self.speed
            self.collision("vertical")