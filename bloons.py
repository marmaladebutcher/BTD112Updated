import pygame 
from data import levels, bloons, bloonColors, player #SZ: imports the levels, bloons, blooncolors, and player data from the data module 

class Bloon(pygame.sprite.Sprite): #SZ: creates class for the bloons

    #bloons are the enemies that appear on the map
    def __init__(self, color): #SZ: This function is used to initialize a bloon object, with parameter color
        super(Bloon, self).__init__() #SZ: Initializes self by inheriting self from the parent class of bloon
        self.color = color #SZ: sets color as determined 
        self.image = pygame.image.load('images/%s.png' % color) #SZ: gets the image for the bloon by substituting %s with the color 
        self.rect = self.image.get_rect() #SZ: creates rect object based on dimensions of the image 
        self.rect.center = [738,-50] #SZ: sets center of the rect object 
        self.pop = pygame.image.load('images/pop.png') #pop animation

        self.strength = bloons[self.color]["strength"] #SZ: sets the strength (health) associated with the bloon based on color in the dictionary 
        self.slowed = False #SZ: default condition, bloon is not slowed 
        self.speed = bloons[self.color]["speed"] #SZ: sets the speed associated with the bloon based on color in the dictionary 
        self.distance = 0 #SZ: currently initializes bloon with zero distance travelled

        #monkeys give $5 multiplied by their strength (health)
        self.originalPrice = self.strength * 5

        self.waypoint = 0 #SZ: sets current waypoint to zero 
        if player.game == "map1":
            self.direction = 'down' #SZ: starts by heading down 
            self.rect.center = [738,-50] #starting point
        elif player.game == "map2": 
            self.direction = 'right' #SZ: starts by heading right 
            self.rect.center = [-50,38] #starting point

    def __str__(self): #SZ: this function defines the string representation of itself
        return "%s" % (self.color) #SZ: returns with its color as a string 

    #move a bloon
    def move(self, x, y): #SZ: This class moves the bloon object by an x and y amount 
        self.rect.centerx += x #SZ: changes the center of the rect object's x position by x 
        self.rect.centery += y #SZ: changes the center of the rect object's y position by y 
        if player.game != "map2": #SZ: map 1
            if self.rect.centery > 0: #SZ: if y position is positive 
                #we keep track of distance moved to see which bloon moved 
                #furthest; very important for Towers.furthestBloon function
                self.distance += (abs(x) + abs(y)) #SZ: updates distance based on absolute values of x and y 
        else: #SZ: map 2 
            if self.rect.centerx > 0: #SZ: if x position is positive 
                self.distance += (abs(x) + abs(y)) #SZ: updates distance based on absolute values of x and y 

    #do this every time the bloon is hit
    def updateDamage(self, damage, slow, surface): #SZ: This function updates the health of the bloon based on the damage it received and also updates if its slowed 
        self.strength -= damage #SZ: updates health by subtracting damage 

        #draw popping animation
        if damage != 0: #SZ: if it received damage 
            surface.blit(self.pop,(self.rect)) #SZ: displays pop image 

        #bloon has died
        if self.strength <= 0:  #SZ: if bloon has no more health 
            player.money += self.originalPrice #SZ: adds money based on the original price (strength*5)
            self.kill() #SZ: removes bloon object 
            return

        #there is a slow on the bloon
        if slow != 0: #SZ: if its slowed 
            if self.speed // 2 != 0: #SZ: if floor division result isn't 0 
                self.speed /= 2 #SZ: divides speed by 2
                self.slowed = True #SZ: bloon is slowed 

        else: 
            #update the type of bloon after it has been popped
            if self.strength <= bloons["pink"]["strength"]: #SZ: If the current strength of the bloon is less than or equal the strength of the pink bloon 
                self.color = bloonColors[self.strength] #SZ: changes color based on current strength 
            if self.strength > bloons["pink"]["strength"]: #SZ: if its greater than the strength of the pink bloon
                if self.strength <= bloons["ceramic"]["strength"]: #SZ: if current strength is less than or equal the strength of ceramic bloon  
                    self.color = "ceramic" #SZ: color is ceramic 
                elif self.strength <= bloons["moab"]["strength"]: #SZ: if current strength is less than or equal strength of the moab 
                    self.color = "moab" #SZ: color is moab 
            self.image = pygame.image.load('images/%s.png' % self.color)#SZ: loads new image based on new color 

            if self.slowed != True: #SZ: if slowed
                #we only want to update the speed if the bloon is not slowed
                self.speed = bloons[self.color]["speed"] #SZ: updates speed if not slowed 

class Levels(object): #SZ: creates a level class

    #creates group of all bloons in the level
    def runLevel(levelNumber): #SZ: This function runs the level based on level number 
        level = levels[levelNumber] #SZ: gets level data based on the level number 
        bloonCount = 0 #SZ: intial bloon count 
        spaceBetweenBloons = 50 #SZ: spacing so bloons don't clump together 
        spriteBloons = pygame.sprite.Group() #SZ: creates new sprite group for bloon 
        for bloonBlock in level: #SZ: for each bloon tuple 
            for bloon in range(bloonBlock[0]): #SZ: for each object within the range of bloon count (this is an int) 
                newBloon = Bloon(bloonBlock[1]) #SZ: creates bloon based on second object in tuple (a string, which is the color)
                if player.game == "map2": #SZ: if map 2 
                    newBloon.rect.centerx -= spaceBetweenBloons*bloonCount #SZ: intialized bloon center by multiplying space of bloons by bloon count, placing the bloons off the map if more bloons exist
                else:
                    newBloon.rect.centery -= spaceBetweenBloons*bloonCount
                #we want to space out the bloons as they come into the map,
                #otherwise they'll just bunch up in one location
                spriteBloons.add(newBloon) #SZ: adds to spirtegroup 
                bloonCount += 1 #SZ: adds to bloon count
        return spriteBloons #SZ: returns updated sprite group 

    def testRunLevel(self): #SZ: this tests running the level 
        print("Testing runLevel...")
        assert(len(Levels.runLevel(0)) == 0) #SZ: tests if the length of Levels.runLevel(0) is zero 
        print("Done.")
