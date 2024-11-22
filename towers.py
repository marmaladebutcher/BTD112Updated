import pygame #SZ: imports pygame module 
from data import towerTypes, player, Coord #SZ: imports the towertypes, player and coordinates from data modujle 
from bullet import Bullet #SZ: imports the Bullet from the bullet module 
import math 
import time


class Tower(pygame.sprite.Sprite):#SZ: creates a class for the tower objects 

    #towers are the monkeys that shoot bloons
    def __init__(self, name): #SZ: Initalizes an object with parameter name
        super(Tower, self).__init__() #SZ: Initializes self by inheriting self from the parent class of tower

        #basic info
        self.name = name #SZ: sets name of Tower to the argument used to initialize name
        self.image = pygame.image.load('images/%s.png' % name) #SZ: loads the image, with name replacing the %s of the string to grab the file location
        self.rect = self.image.get_rect() #SZ: creates a rectangular object for coordinates based on the boundaries of the image
        self.rect.center = [0,0] #SZ: sets the center of the rectangle to (0,0), the top left of the screen
        self.selected = False #SZ: sets the tower being selected to False
        self.upgraded = False #SZ: sets the tower being upgraded to False 

        #load and draw images
        self.originalImage = pygame.image.load('images/%s.png' % name) #SZ: loads the image, with name replacing the %s of the string to grab the file location
        self.originalImageRect = self.originalImage.get_rect() #SZ: creates a rectangular object for coordinates on the boundaries of the original image
        self.sellButton = pygame.image.load('images/sell.png') #SZ: loads the image for the sell button
        self.sellButtonRect = self.sellButton.get_rect() #SZ: creates a rectangular object for coordinates based on the boundaries of the image
        self.upgradeButton = pygame.image.load('images/upgrade.png') #SZ: loads the image for the upgrade button (images/upgrade.png is the file path, thats where it loads from)
        self.upgradeButtonRect = self.upgradeButton.get_rect() #SZ: creates a rectangular object for coordinates based on the boundaries of the image

        font = pygame.font.SysFont("myriadpro", 20) #SZ: loads the font for the program 
        self.drawUpgradePrice = font.render("$%d" % 
                towerTypes[self.name]["upgrade_price"], 1, (255,255,255)) #SZ: renders the cost of the tower based on the name of the tower and its upgrade price from the towerTypes dictionary, 1 enables anti-aliasing, and (255,255,255) makes the text white
        self.drawUpgradePriceRect = self.drawUpgradePrice.get_rect() #SZ: creates a rectangular object for coordinates based on the dimensions of drawUpgradePrice

        #monkey stats
        self.price = towerTypes[self.name]["price"] #SZ: looks up the tower price in the towerTypes dictionary
        self.cooldown = towerTypes[self.name]["cooldown"] #SZ: looks up the tower cooldown in the towerTypes dictionary
        self.damage = towerTypes[self.name]["damage"] #SZ: looks up the tower damage in the towerTypes dictionary
        self.slow = towerTypes[self.name]["slow"] #SZ: looks up the tower slow value in the towerTypes dictionary (probably used for the gluegunner tower)
        self.range = towerTypes[self.name]["range"] #SZ: looks up the tower range in the towerTypes dictionary

        #used for shooting bullets
        self.timer = 0.0 #SZ: starts tower at 0 for the cooldown of the tower
        self.ready = True #SZ: sets ready to True for whether the tower can shoot or not 
        self.angle = 0 #SZ: initializes angle to 0, which will rotate the tower image a certain amount based on the angle 
 
    def __str__(self): #SZ: function used to get the string of the name of the tower 
        return self.name #SZ: returns the name of the tower 

    #some hard coded values of the monkey sidebar
    def clickedMonkeys(x, y): #SZ: This function is used to check what tower was selected when the mouse is clicked. 
        if x > 825 and x < 885 and y > 140 and y < 215: #SZ: Between (825,140) and (885,215), the tower selected will be a dart monkey
            return "dartmonkey"
        elif x > 890 and x < 950 and y > 140 and y < 215: #SZ: Between (890,140) and (950,215), the tower selected will be a ninja monkey
            return "ninjamonkey"
        elif x > 825 and x < 885 and y > 225 and y < 300: #SZ: Between (825,225) and (885,300), the tower selected will be a glue gunner
            return "gluegunner"
        elif x > 890 and x < 950 and y > 225 and y < 300: #SZ: Between (890,225) and (950,300), the tower selected will be a sniper
            return "sniper"
        elif x > 825 and x < 885 and y > 310 and y < 380: #SZ: Between (825,310) and (885,300), the tower selected will be a glue boat
            return "boat"
        elif x > 890 and x < 950 and y > 310 and y < 380: #SZ: Between (890,310) and (950,380), the tower selected will be a super monkey
            return "supermonkey"
        else: #SZ: When clicked, the mouse position is not within any of the tower icons
            return None 

    def upgrade(self): #SZ: This function upgrades the tower, and updates stats for the tower 
        self.name = self.name + "_upgraded" #SZ: changes the name from the original name by adding _upgraded
        self.image = pygame.image.load('images/%s.png' % self.name) #SZ: loads the image 
        self.originalImage = pygame.image.load('images/%s.png' % self.name) #SZ: loads image 
        self.price = towerTypes[self.name]["price"] #SZ: gets new price from the towertypes dictionary: searchs by name, then checks the price associated with the name, same methodology for below
        self.cooldown = towerTypes[self.name]["cooldown"] #SZ: gets new cooldown from the towertypes dictionary 
        self.damage = towerTypes[self.name]["damage"] #SZ: gets new damge from towertypes dictionary 
        self.slow = towerTypes[self.name]["slow"] #SZ: gets new slow value from towertypes dictionary 
        self.range = towerTypes[self.name]["range"] #SZ: gets new range from towertypes dictionary 
        self.upgraded = True #SZ: updates the value of upgraded to True
        player.money -= towerTypes[self.name]["upgrade_price"] #SZ: subtracts the players money from the cost of the upgrade price, retrieved from the tower types dictionary 

    def legalPlacements(self, x, y): #SZ: This function determines the valid coordinates of where the towers can be placed. x, y is the location of where the player wants to put 
        if self.name == "boat": #SZ: if the tower is the boat tower 
            #can only be placed in water 
            if player.game != "map2": #SZ: Map 1 
                coordinates = Coord.boatValues #SZ: gets coordinates from boatValues (in data)
            else: #SZ: Map 2 
                coordinates = Coord.boatValues2 #SZ: gets coordinates from boatValues2 (in data)
            x1, x2 = coordinates[0][0], coordinates[1][0] #SZ: sets x1, x2 coordinates from retrieving the first item in each tuple in coordinates 
            y1, y2 = coordinates[0][1], coordinates[1][1] #SZ: sets y1, y2 coordinates from retrieving the first item in each tuple in coordinates 
            if x > x1 and x < x2: #SZ: checks if within the limits of x 
                if y > y1 and y < y2: #SZ: checks if within the limits of y
                    return True #SZ: If both are true, boat tower can be placed here 
        else: #SZ: literally any other type of tower 
            if player.game != "map2": #SZ: Map 1 
                nonTrackValues = Coord.nonTrackValues #SZ: gets non track values as valid placements for the tower 
            else: #SZ: Map 2 
                nonTrackValues = Coord.nonTrackValues2 
            #cannot place monkeys on track, sidebar, or water
            for coordinates in nonTrackValues: #SZ: A for loop for a list of tuples, to check if its a valid placement 
                x1, x2 = coordinates[0][0], coordinates[1][0] #SZ: sets x1, x2 coordinates from retrieving the first item in each tuple in coordinates 
                y1, y2 = coordinates[0][1], coordinates[1][1] #SZ: sets y1, y2 coordinates from retrieving the first item in each tuple in coordinates 
                if x > x1 and x < x2: #SZ: if within limits of x 
                    if y > y1 and y < y2: #SZ: if within limits of y 
                        return True #SZ: tower can be placed there 
            return False #SZ: tower cannot be placed there 

    def draw(self, surface): #SZ: this function is used to draw the towers onto the screen 
        #draws monkey on the surface
        surface.blit(self.image, self.rect) #SZ: draws the image, with rect being the coordinates of where the tower will be drawn onto 
        player.towers.add(self) #SZ: adds the tower to the players list of towers 

    def removeUpgradeButton(self): #SZ: This function removes the upgrade button off the screen 
        #remove the upgrade button and price from screen
        self.drawUpgradePriceRect.center = [-50, -50] #SZ: negative position moves it off the screen
        self.upgradeButtonRect.center = [-50, -50]

    #draw green range around monkey if legal placement
    #otherwise, draw red range
    def drawMonkeyAndRange(self, legal, x, y): #SZ: This draws a circle showing the monkey's range, makes the circle red if the monkey cannot be placed at the coordinate where the players wants to place it at 

        green = (141,192,55) 
        red = (204,0,0)
        color = green if legal else red #SZ: sets the color based on legality 
        self.rect.center = [x,y] #SZ: sets the center of the rects coordinates 
        width = 4

        player.screen.blit(self.image, self.rect) #SZ: draws the image at the coordinates of rect
        if self.name == "sniper" or self.name == "sniper_upgraded": 
            #since sniper has unlimited range, we cannot draw the usual circle
            #therefore we just draw a small circle of radius 40 around it
            radius = 40
            pygame.draw.circle(player.screen, color, 
            self.rect.center, radius, width) #SZ: draws a circle onto the screen with the color associated, with the circle starting at the center, and a radius of 40, with line thickness of 4
        else: #SZ: case for non sniper objects 
            pygame.draw.circle(player.screen, color, 
            self.rect.center, self.range, width) #SZ: draws a circle onto the screen with the color associated, with the circle starting at the center, and a radius based on the range, with line thickness of 4

    #do this when you click on a monkey
    def drawRangeAndSell(self, surface): #SZ: This function draws the range of the tower and the sell button when clicked 
        #draws the range and sell/upgrade button for monkey
        width = 4 
        range = 40 
        green = (141,192,55)
        if self.name == "sniper" or self.name == "sniper_upgraded": 
            pygame.draw.circle(surface, green, self.rect.center, range, width) #SZ: draws a green circle onto the screen, starting from the center of the rect associated with the image, with a radius based on the range, and line thickness of 4.
        else:
            pygame.draw.circle(surface, green, self.rect.center, 
                self.range, width) #SZ: draws a green circle onto the screen, starting from the center of the rect associated with the image, with a radius based on the range, and line thickness of 4.
        player.screen.blit(self.sellButton, self.sellButtonRect) #SZ: draws sell button at the coordinates of the rect associated with it
        player.screen.blit(self.upgradeButton, self.upgradeButtonRect) #SZ: draws upgrade button at the coordinates of the rect associated with it
        player.screen.blit(self.drawUpgradePrice, self.drawUpgradePriceRect) #SZ: draws upgrade price at the coordinates of the rect associated with it

    #sell monkey
    def sell(self): #SZ: This function is for when you sell your tower 
        moneyBack = 0.75
        #you only get 75% of your money back if you sell
        player.money += int(towerTypes[self.name]["price"] * moneyBack) #SZ: adds the money back to the players wallet based on the current cost of the tower 
        self.kill() #SZ: removes tower 

    #calculates bloon that is the closest to the end of the map
    def furthestBloon(group): #SZ: This function is used to find the bloon closest to the end of the map 
        maxDistance, furthest = 0, None #SZ: placeholder variables 
        for bloon in group: #SZ: checks every bloon on the screen 
            if bloon.distance > maxDistance:  #SZ: checks if the bloon distance is greater than the max distance, if it is, sets furthest bloon to that bloon, and updates max distance
                furthest = bloon
                maxDistance = bloon.distance
        return furthest

    #monkey shoots bloons
    def shootBloons(self): #SZ: This function is used for the tower to shoot the bloons
        now = time.time() #SZ: finds the current time from the time module 
        group = pygame.sprite.Group() #SZ: sets group to the current sprite grouping 

        #ready to fire
        if self.ready: #SZ: if current tower is ready 
            for bloon in player.spriteBloons: #SZ: checks every bloon thats currently in the sprite group 

                if "gluegunner" in self.name: #SZ: category for gluegunner tower 
                #gluegunner only wants to shoot bloons that aren't already slow
                    if (Tower.distance(bloon.rect.center, self.rect.center) <
                            self.range) and bloon.slowed == False:
                        group.add(bloon) #SZ: if the bloon is in the range of the tower and is not slowed, adds to group of bloons that can be shot 
                else: #SZ: non gluegunner towers 
                #everything else will target bloons in its range
                    if (Tower.distance(bloon.rect.center, self.rect.center) <
                                self.range):
                        group.add(bloon) #SZ: if the bloon is in the range of the tower, adds to group of bloons that can be shot 

            furthest = Tower.furthestBloon(group) #SZ: finds the furthest bloon
            #calculate which bloon is closest to the end of the map in group

            if furthest != None: #SZ: a bloon can be shot by this tower 
                if self.name != "sniper" and self.name != "sniper_upgraded": #SZ: if not a sniper tower
                    if player.game != "map2": #SZ: map 1 
                        if furthest.rect.centery >= 0: #SZ: checks if the further bloon is still within the y boundary (exit is based on y position)
                            player.bullets.add(Bullet(self, furthest)) #SZ: adds a bullet object, newly created based on the tower and the furthest bloon
                    else: #SZ: map 2 
                        if furthest.rect.centerx >= 0: #SZ: checks if the further bloon is still within the x boundary (exit is based on x position)
                            player.bullets.add(Bullet(self, furthest)) #SZ: adds a bullet object, newly created based on the tower and the furthest bloon

                #calculate rotation of monkey to face the bloon it's shooting
                deltay = self.originalImageRect.centery - furthest.rect.centery #SZ: calculates change in y distance from the furthest bloon from the tower
                deltax = self.originalImageRect.centerx - furthest.rect.centerx #SZ: calculates change in x distance from the furthest bloon from the tower 
                self.angle = math.degrees(math.atan2(deltax, deltay)) #SZ: calculates the arctan from the change in x and y, then converts this into degrees (from radians)

            self.ready = False #SZ: tower is no longer ready to shoot 
            self.timer = now #SZ: sets timer based on the current time 
            self.image = pygame.transform.rotozoom(self.originalImage, 
                self.angle, 1) #SZ: rotates the image with the angle 

        else: #SZ: tower is not currently ready to fire 
            if (now - self.timer) > self.cooldown: #SZ: checks current time, subtracts that from the current time, sees if its greater than the cooldown 
                self.ready = True #SZ: if True, then now ready to fire 

    #returns distance between two points a and b
    def distance(a, b): #SZ: This is just the shortest distance function in python, with a and b being tuples
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
