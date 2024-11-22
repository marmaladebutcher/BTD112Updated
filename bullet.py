import pygame
import math
from bloons import Bloon #SZ: imports bloons from bloon module 
from data import towerTypes #SZ: imports towerType data from data module 

class Bullet(pygame.sprite.Sprite): #SZ: creates a bullet class 

    def __init__(self, tower, bloon): #SZ: initializes object with parameters of tower and bloon 
        super(Bullet, self).__init__() #SZ: Initializes self by inheriting self from the parent class of tower
        self.tower = tower 
        self.bloon = bloon
        self.damage = towerTypes[self.tower.name]["damage"] #SZ: sets damage by finding the damage associated with the naem of the tower in the towerTypes dictionary
        self.speed = 30 #SZ: speed of bullet 
        self.slow = towerTypes[self.tower.name]["slow"] #SZ: sets slow value by finding the slow associated with the name of the tower in the towerTypes dictionary 
        self.image = pygame.image.load('images/%s.png' % 
            towerTypes[self.tower.name]["bullet"]) #SZ: loads the image based on the bullet associated with the tower in the dictionary 
        self.rect = self.image.get_rect(center=tower.rect.center) #SZ: sets the center of bullet to the center of the tower, creates a rectangular object based on image 

    def update(self, surface): #SZ: This function updates the screen
        if not self.bloon.alive(): #SZ: if the bloon targeted isn't alive 
            #if bloon dead already then stop hitting it
            self.kill() #SZ: gets rid of bullet object 

        if pygame.sprite.collide_rect(self, self.bloon): #SZ: if the bullet collides with the bloon
            self.kill() #if bullet hits a bloon, remove bullet from screen
            Bloon.updateDamage(self.bloon, self.damage, self.slow, surface) #SZ: updates bloon health with the damage associated with the bloon

        else: #SZ: bloon is still alive, hasn't collided yet
            #continue to pursue the bloon
            bloonCenterX = self.bloon.rect.centerx #SZ: gets x position of center of bloon
            bloonCenterY = self.bloon.rect.centery #SZ: gets y position of center of bloon
            bulletCenterX, bulletCenterY = self.rect.centerx, self.rect.centery #SZ: gets x,y position of center of bullet 
            bulletSpeed = self.speed #SZ: gets bullet speed 

            if bloonCenterX <= bulletCenterX: #SZ: bloon x position is less than or equal bullet x position 
                dx = - bulletSpeed #SZ: sets change in x to negative bullet speed 
            elif bloonCenterX > bulletCenterX: #SZ: bloon x position greater than bullet x position 
                dx = bulletSpeed #SZ: sets change in x to bullet speed 

            if bloonCenterY <= bulletCenterY: #SZ: bloon y position is less than or equal bullet y position 
                dy = - bulletSpeed #SZ: sets change in y to negative bullet speed 
            elif bloonCenterY > bulletCenterY: #SZ: bloon y position greater than bullet y position 
                dy = bulletSpeed #SZ: sets change in y to bullet speed

            if (abs(bloonCenterX - bulletCenterX) <
                abs(bloonCenterY - bulletCenterY)): #SZ: if absolute value of (bloon x - bullet x) is less than absolute value of  (bloon y - bullet y)
                dx = dx / 2 #SZ: divides change in x by 2, since the distance between the two x values is less than the two y values 
            else:
                dy = dy / 2

            self.rect.x += dx #SZ: updates x position of bullet 
            self.rect.y += dy #SZ: updates y position of bullet 
