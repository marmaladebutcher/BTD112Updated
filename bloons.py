import pygame
from data import levels, bloons, bloonColors, player


class Bloon(pygame.sprite.Sprite):

    #bloons are the enemies that appear on the map
    def __init__(self, color):
        super(Bloon, self).__init__()
        self.color = color
        self.image = pygame.image.load('images/%s.png' % color)
        self.rect = self.image.get_rect()
        self.rect.center = [738,-50]
        self.pop = pygame.image.load('images/pop.png') #pop animation

        self.strength = bloons[self.color]["strength"]
        self.slowed = False
        self.speed = bloons[self.color]["speed"]
        self.distance = 0

        #monkeys give $5 multiplied by their strength
        self.originalPrice = self.strength * 5

        self.waypoint = 0
        if player.game == "map1":
            self.direction = 'down'
            self.rect.center = [738,-50] #starting point
        elif player.game == "map2":
            self.direction = 'right'
            self.rect.center = [-50,38] #starting point

    def __str__(self):
        return "%s" % (self.color)

    #move a bloon
    def move(self, x, y):
        self.rect.centerx += x
        self.rect.centery += y
        if player.game != "map2":
            if self.rect.centery > 0:
                #we keep track of distance moved to see which bloon moved 
                #furthest; very important for Towers.furthestBloon function
                self.distance += (abs(x) + abs(y))
        else:
            if self.rect.centerx > 0:
                self.distance += (abs(x) + abs(y))

    #do this every time the bloon is hit
    def updateDamage(self, damage, slow, surface):
        self.strength -= damage

        #draw popping animation
        if damage != 0:
            surface.blit(self.pop,(self.rect))

        #bloon has died
        if self.strength <= 0: 
            player.money += self.originalPrice
            self.kill()
            return

        #there is a slow on the bloon
        if slow != 0:
            if self.speed // 2 != 0:
                self.speed /= 2
                self.slowed = True

        else:
            #update the type of bloon after it has been popped
            if self.strength <= bloons["pink"]["strength"]:
                self.color = bloonColors[self.strength]
            if self.strength > bloons["pink"]["strength"]:
                if self.strength <= bloons["ceramic"]["strength"]:
                    self.color = "ceramic"
                elif self.strength <= bloons["moab"]["strength"]:
                    self.color = "moab"
            self.image = pygame.image.load('images/%s.png' % self.color)

            if self.slowed != True:
                #we only want to update the speed if the bloon is not slowed
                self.speed = bloons[self.color]["speed"]

class Levels(object):

    #creates group of all bloons in the level
    def runLevel(levelNumber):
        level = levels[levelNumber]
        bloonCount = 0
        spaceBetweenBloons = 50
        spriteBloons = pygame.sprite.Group()
        for bloonBlock in level:
            for bloon in range(bloonBlock[0]):
                newBloon = Bloon(bloonBlock[1])
                if player.game == "map2":
                    newBloon.rect.centerx -= spaceBetweenBloons*bloonCount
                else:
                    newBloon.rect.centery -= spaceBetweenBloons*bloonCount
                #we want to space out the bloons as they come into the map,
                #otherwise they'll just bunch up in one location
                spriteBloons.add(newBloon)
                bloonCount += 1
        return spriteBloons

    def testRunLevel(self):
        print("Testing runLevel...")
        assert(len(Levels.runLevel(0)) == 0)
        print("Done.")
