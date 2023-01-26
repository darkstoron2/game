import pygame
from settings import *
from load_image import *


class ProjectTile(pygame.sprite.Sprite):
    def __init__(self, center, direction, angle):
        super().__init__()
        all_sprites.add(self)
        projectile_sprites.add(self)
        self.direction = direction
        self.speed = 20
        self.image = load_image("bullet.png")
        self.rect = self.image.get_rect(center=center)
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        # Двигаем пулю
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        self.collision()

    def collision(self):
        # Проверяем столкновение пули
        if pygame.sprite.spritecollideany(self, obstacle_sprites):
            self.kill()
        for sprite in enemy_sprites:
            if sprite.rect.colliderect(self.rect):
                sprite.get_damage()
                projectile_sprites.remove(self)
                self.kill()