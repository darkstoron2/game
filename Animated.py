import pygame

from load_image import load_image
from settings import *


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        # Нарезаем кадры для анимации
        self.frames = {}
        for name, sheet in frames.items():
            self.frames[name] = []
            self.cut_sheet(name, sheet[0], sheet[1])
        # Long_Anim_Status Для Прыжка, стрельбы, перезарядки и смерти. Чтобы нужные анимации проигрывались до конца
        # Status Для бега и idle
        # Long_Anim_Time Нужен чтобы смотреть сколько кадров длинной анимации осталось
        self.status = "idle"
        self.long_anim_status = ""
        self.long_anim_time = 0
        self.anim_speed = 4 / FPS
        self.cur_frame = 0
        self.direction_sprite = "r"
        self.new_frame(None, True)

    # Нарезчик спрайтов
    def cut_sheet(self, key, sheet, columns):
        self.rect = pygame.Rect(0, 0, int(sheet.get_width() / columns),
                                int(sheet.get_height()))
        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            img_rect = pygame.Rect(frame_location, self.rect.size)
            new_img = sheet.subsurface(img_rect)
            self.frames.get(key).append(new_img)

    # Поворачиваем спрайт взависимости от движения
    def rotate(self, direction):
        if direction.x > 0 and self.direction_sprite == "l":
            self.direction_sprite = "r"
        elif direction.x < 0 and self.direction_sprite == "r":
            self.direction_sprite = "l"
        if self.direction_sprite == "l":
            self.image = pygame.transform.flip(self.image, True, False)

    # Проверяем обновился ли кадр длинной анимации
    def long_animate(self):
        if int((self.cur_frame + self.anim_speed) % len(self.frames.get(self.long_anim_status))) > self.cur_frame:
            self.long_anim_time -= 1
            if self.long_anim_time == 0:
                self.long_anim_status = ""

    # Обновляем и ставим новый кадр из длинной анимации
    def new_frame(self, direction=None, start=False):
        if start:
            self.cur_frame = (self.cur_frame + self.anim_speed) % len(self.frames.get(self.status))
            self.image = self.frames.get(self.status)[int(self.cur_frame)]
        else:
            if self.long_anim_status != "":
                self.long_animate()
            self.cur_frame = (self.cur_frame + self.anim_speed) % len(self.frames.get(self.status))
            self.image = self.frames.get(self.status)[int(self.cur_frame)]
            self.rotate(direction)
