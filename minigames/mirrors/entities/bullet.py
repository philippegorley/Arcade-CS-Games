from math import *
import pygame


class Bullet:
    SCALE = 3
    BASE_SPEED = 0.6
    BULLET_SPRITES = [ "minigames/mirrors/images/bullet1.png",
                       "minigames/mirrors/images/bullet2.png" ]
    def __init__(self, player, initial_x, initial_y, angle, power):
        self.gfx = pygame.image.load(Bullet.BULLET_SPRITES[player])
        self.gfx = pygame.transform.scale(self.gfx, (self.gfx.get_width() * Bullet.SCALE, self.gfx.get_height() * Bullet.SCALE))
        self.gfx = pygame.transform.rotate(self.gfx, angle)
        self.owner = player

        self._d = 0
        self._x = initial_x
        self._y = initial_y
        self._a = angle
        self._v = power * Bullet.BASE_SPEED

    def collides_with(self, mirror):
        return self.gfx.get_rect(center=(self._x, self._y)).colliderect(mirror.gfx.get_rect(topleft=mirror.position))

    def display(self, screen):
        self._x -= self._v * sin(radians(self._a))
        self._y -= self._v * cos(radians(self._a))
        rect = self.gfx.get_rect(center=(self._x, self._y))

        screen.blit(self.gfx, rect)