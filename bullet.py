import pygame
import math
from bloons import Bloon
from data import towerTypes

class Bullet(pygame.sprite.Sprite):

    def __init__(self, tower, bloon):
        super(Bullet, self).__init__()
        self.tower = tower
        self.bloon = bloon
        self.damage = towerTypes[self.tower.name]["damage"]
        self.speed = 30
        self.slow = towerTypes[self.tower.name]["slow"]
        self.image = pygame.image.load('images/%s.png' % 
            towerTypes[self.tower.name]["bullet"])
        self.rect = self.image.get_rect(center=tower.rect.center)

    def update(self, surface):
        if not self.bloon.alive():
            #if bloon dead already then stop hitting it
            self.kill()

        if pygame.sprite.collide_rect(self, self.bloon):
            self.kill() #if bullet hits a bloon, remove bullet from screen
            Bloon.updateDamage(self.bloon, self.damage, self.slow, surface)

        else:
            #continue to pursue the bloon
            bloonCenterX = self.bloon.rect.centerx
            bloonCenterY = self.bloon.rect.centery
            bulletCenterX, bulletCenterY = self.rect.centerx, self.rect.centery
            bulletSpeed = self.speed

            if bloonCenterX <= bulletCenterX:
                dx = - bulletSpeed
            elif bloonCenterX > bulletCenterX:
                dx = bulletSpeed

            if bloonCenterY <= bulletCenterY:
                dy = - bulletSpeed
            elif bloonCenterY > bulletCenterY:
                dy = bulletSpeed

            if (abs(bloonCenterX - bulletCenterX) <
                abs(bloonCenterY - bulletCenterY)):
                dx = dx / 2
            else:
                dy = dy / 2

            self.rect.x += dx
            self.rect.y += dy
