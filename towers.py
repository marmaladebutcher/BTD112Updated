import pygame
from data import towerTypes, player, Coord
from bullet import Bullet
import math
import time


class Tower(pygame.sprite.Sprite):

    #towers are the monkeys that shoot bloons
    def __init__(self, name):
        super(Tower, self).__init__()

        #basic info
        self.name = name
        self.image = pygame.image.load('images/%s.png' % name)
        self.rect = self.image.get_rect()
        self.rect.center = [0,0]
        self.selected = False
        self.upgraded = False

        #load and draw images
        self.originalImage = pygame.image.load('images/%s.png' % name)
        self.originalImageRect = self.originalImage.get_rect()
        self.sellButton = pygame.image.load('images/sell.png')
        self.sellButtonRect = self.sellButton.get_rect()
        self.upgradeButton = pygame.image.load('images/upgrade.png')
        self.upgradeButtonRect = self.upgradeButton.get_rect()

        font = pygame.font.SysFont("myriadpro", 20)
        self.drawUpgradePrice = font.render("$%d" % 
                towerTypes[self.name]["upgrade_price"], 1, (255,255,255))
        self.drawUpgradePriceRect = self.drawUpgradePrice.get_rect()

        #monkey stats
        self.price = towerTypes[self.name]["price"]
        self.cooldown = towerTypes[self.name]["cooldown"]
        self.damage = towerTypes[self.name]["damage"]
        self.slow = towerTypes[self.name]["slow"]
        self.range = towerTypes[self.name]["range"]

        #used for shooting bullets
        self.timer = 0.0
        self.ready = True
        self.angle = 0

    def __str__(self):
        return self.name

    #some hard coded values of the monkey sidebar
    def clickedMonkeys(x, y):
        if x > 825 and x < 885 and y > 140 and y < 215:
            return "dartmonkey"
        elif x > 890 and x < 950 and y > 140 and y < 215:
            return "ninjamonkey"
        elif x > 825 and x < 885 and y > 225 and y < 300:
            return "gluegunner"
        elif x > 890 and x < 950 and y > 225 and y < 300:
            return "sniper"
        elif x > 825 and x < 885 and y > 310 and y < 380:
            return "boat"
        elif x > 890 and x < 950 and y > 310 and y < 380:
            return "supermonkey"
        else:
            return None

    def upgrade(self):
        self.name = self.name + "_upgraded"
        self.image = pygame.image.load('images/%s.png' % self.name)
        self.originalImage = pygame.image.load('images/%s.png' % self.name)
        self.price = towerTypes[self.name]["price"]
        self.cooldown = towerTypes[self.name]["cooldown"]
        self.damage = towerTypes[self.name]["damage"]
        self.slow = towerTypes[self.name]["slow"]
        self.range = towerTypes[self.name]["range"]
        self.upgraded = True
        player.money -= towerTypes[self.name]["upgrade_price"]

    def legalPlacements(self, x, y):
        if self.name == "boat":
            #can only be placed in water
            if player.game != "map2":
                coordinates = Coord.boatValues
            else:
                coordinates = Coord.boatValues2
            x1, x2 = coordinates[0][0], coordinates[1][0]
            y1, y2 = coordinates[0][1], coordinates[1][1]
            if x > x1 and x < x2:
                if y > y1 and y < y2:
                    return True
        else:
            if player.game != "map2":
                nonTrackValues = Coord.nonTrackValues
            else:
                nonTrackValues = Coord.nonTrackValues2
            #cannot place monkeys on track, sidebar, or water
            for coordinates in nonTrackValues:
                x1, x2 = coordinates[0][0], coordinates[1][0]
                y1, y2 = coordinates[0][1], coordinates[1][1]
                if x > x1 and x < x2:
                    if y > y1 and y < y2:
                        return True
            return False

    def draw(self, surface):
        #draws monkey on the surface
        surface.blit(self.image, self.rect)
        player.towers.add(self)

    def removeUpgradeButton(self):
        #remove the upgrade button and price from screen
        self.drawUpgradePriceRect.center = [-50, -50]
        self.upgradeButtonRect.center = [-50, -50]

    #draw green range around monkey if legal placement
    #otherwise, draw red range
    def drawMonkeyAndRange(self, legal, x, y):
        green = (141,192,55)
        red = (204,0,0)
        color = green if legal else red
        self.rect.center = [x,y]
        width = 4

        player.screen.blit(self.image, self.rect)
        if self.name == "sniper" or self.name == "sniper_upgraded":
            #since sniper has unlimited range, we cannot draw the usual circle
            #therefore we just draw a small circle of radius 40 around it
            radius = 40
            pygame.draw.circle(player.screen, color, 
            self.rect.center, radius, width)
        else:
            pygame.draw.circle(player.screen, color, 
            self.rect.center, self.range, width)

    #do this when you click on a monkey
    def drawRangeAndSell(self, surface):
        #draws the range and sell/upgrade button for monkey
        width = 4
        range = 40
        green = (141,192,55)
        if self.name == "sniper" or self.name == "sniper_upgraded":
            pygame.draw.circle(surface, green, self.rect.center, range, width)
        else:
            pygame.draw.circle(surface, green, self.rect.center, 
                self.range, width)
        player.screen.blit(self.sellButton, self.sellButtonRect)
        player.screen.blit(self.upgradeButton, self.upgradeButtonRect)
        player.screen.blit(self.drawUpgradePrice, self.drawUpgradePriceRect)

    #sell monkey
    def sell(self):
        moneyBack = 0.75
        #you only get 75% of your money back if you sell
        player.money += int(towerTypes[self.name]["price"] * moneyBack)
        self.kill()

    #calculates bloon that is the closest to the end of the map
    def furthestBloon(group):
        maxDistance, furthest = 0, None
        for bloon in group:
            if bloon.distance > maxDistance:
                furthest = bloon
                maxDistance = bloon.distance
        return furthest

    #monkey shoots bloons
    def shootBloons(self):
        now = time.time()
        group = pygame.sprite.Group()

        #ready to fire
        if self.ready:
            for bloon in player.spriteBloons:

                if "gluegunner" in self.name:
                #gluegunner only wants to shoot bloons that aren't already slow
                    if (Tower.distance(bloon.rect.center, self.rect.center) <
                            self.range) and bloon.slowed == False:
                        group.add(bloon)
                else:
                #everything else will target bloons in its range
                    if (Tower.distance(bloon.rect.center, self.rect.center) <
                                self.range):
                        group.add(bloon)

            furthest = Tower.furthestBloon(group)
            #calculate which bloon is closest to the end of the map in group

            if furthest != None:
                if self.name != "sniper" and self.name != "sniper_upgraded":
                    if player.game != "map2":
                        if furthest.rect.centery >= 0:
                            player.bullets.add(Bullet(self, furthest))
                    else:
                        if furthest.rect.centerx >= 0:
                            player.bullets.add(Bullet(self, furthest))

                #calculate rotation of monkey to face the bloon it's shooting
                deltay = self.originalImageRect.centery - furthest.rect.centery
                deltax = self.originalImageRect.centerx - furthest.rect.centerx
                self.angle = math.degrees(math.atan2(deltax, deltay))

            self.ready = False
            self.timer = now
            self.image = pygame.transform.rotozoom(self.originalImage, 
                self.angle, 1)

        else:
            if (now - self.timer) > self.cooldown:
                self.ready = True

    #returns distance between two points a and b
    def distance(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
