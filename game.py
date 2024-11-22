import pygame #MW: import pygame module
import sys
from pygame.locals import *
from bloons import Levels
from towers import Tower
from player import Player, Music
from data import Coord, towerTypes, player

"""
Citations:

1. Game recreated from and monkey/bloon/map images taken from Bloons Tower 
    Defense 5 by Ninja Kiwi:
    http://ninjakiwi.com/Games/Tower-Defense/Bloons-Tower-Defense-5.html

2. Game.run and Game.init function referenced and modified from Lukas Peraza: 
    http://blog.lukasperaza.com/getting-started-with-pygame/

3. Towers.shootBloons and Bullet.update referenced and modified from Cactusson:
    https://github.com/Cactusson/towers

4. Other game images (basketball, shurikens, bombs, etc) from sources found
    on Google images

5. Basic tutorials and pygame code examples from Pygame.org:
    http://www.pygame.org/hifi.html

6. Splash screen and game over/won screen made with help from Canva application
    http://www.canva.com
"""

class Game(object): #MW: create a class for the game

    player = Player()

    def __init__(self, width=966, height=598, fps=40): #create
        self.width = width
        self.height = height
        self.fps = fps
        self.title = "Bloons Tower Defense 112: By Sarah Wang"
        pygame.init() #MW: initializes all pygame modules (needed to set up game window, fonts, music, etc.)

        pygame.mixer.music.load('btd_theme.ogg') #MW: load the music file from the module
        pygame.mixer.music.play(-1) #-1 means play forever #MW: play the background music forever

    def initializeMap(self):
        player.screen.blit(self.map, (0,0)) #MW: draw the map image on the screen at the coordinates (0,0) (top left of screen)

    def timerFired(self): #MW: creates a function that shoots the monkeys' bullets across the screen
        if player.gameOver == False:

            #creates bullet if monkey is not on cooldown
            for monkey in player.towers:
                if "sniper" in monkey.name:
                    monkey.shootBloons() #MW: calls the shootBloons function for the monkey on the field to check if the monkey can shoot a bloon
                    if monkey.ready:
                        bloon = Tower.furthestBloon(player.spriteBloons) #MW: if the monkey's cooldown is finished, the targetted bloon becomes the bloon closest to the end of the map
                        if bloon != None: #MW: run if such bloon exists
                            sniperStrength = towerTypes[monkey.name]["damage"] #MW: finds the strength of the tower by looking up the name of the tower and its damage value in the TowerTypes dictionary
                            bloon.updateDamage(sniperStrength,0,player.screen) #MW: damage the bloon and check if it has been destroyed (if it has been destroyed it will be remobed from the screen)
                else:
                    monkey.shootBloons() #MW: if the monkey isn't a sniper, it just calls the shootBloons function for the monkey on the field to check if the monkey can shoot a bloon and allows it to shoot bullets at a bloon if it can

            #updates bullets (make them move toward targets)
            for bullet in player.bullets:
                bullet.update(player.screen) #MW: moves the bullets across the screen and towards the targetted bloons

    def pressedButton(self, x, y): #MW: create a function that allows the player to click buttons on the screen

        #pressed start button
        if x > 829 and x < 952 and y > 461 and y < 500: #MW: checks if player clicked a coordinate in the area of the start button
            #only start next level when player just started, or completed level
            if player.spriteBloons == None or len(player.spriteBloons) == 0: #MW: checks if all bloons are gone or if none existed to begin with
                player.level += 1 #MW: after the player has just started the game or just completed a level, the next level will begin
                if player.level < 11:
                    player.spriteBloons = Levels.runLevel(player.level) #MW: if the player hasn't finished playing all of the levels, the bloon sprites will be generated based on the current level
                else:
                    player.level = 10
                    player.gameWon = True #MW: if the player has made it to level 10, the game has been won

        #pressed monkey sidebar
        if x > 825 and x < 950 and y > 140 and y < 380: #MW: checks if the player clicked a coordinate in the area of the monkey sidebar
            #check what monkey you clicked on
            player.selectedTower = Tower.clickedMonkeys(x, y) #MW: depending on what monkey was clicked, the selected tower becomes that monkey

        #pressed music button
        if x > Coord.music[0][0] and y < Coord.music[0][1]:
            if y > Coord.music[1][0] and y < Coord.music[1][1]: #MW: checks if the user has clicked the music button (Coord.music is a 2D list that holds the x and y coordinates of the music button)
                Music.play = not Music.play #MW: the music is stopped after the music button is clicked
                if Music.play == True:
                    pygame.mixer.music.unpause() #MW: if the music button has been clicked after it has previously been turned off, the music is unpaused and starts playing again
                else:
                    pygame.mixer.music.pause() #MW: if the music was playing and the button has been clicked, the music is paused

        #pressed home button
        if x > 840 and x < 872 and y > 538 and y < 568:
            self.splashScreenActive = True #MW: if coordinates within the home button are pressed, the main menu screen is displayed again

        #place a monkey onto the canvas
        if player.selectedTower != None:
            monkeyName = player.selectedTower #MW: if a monkey from the sidebar hasn't been selected, the monkey the player has clicked will now be the monkey that the player has selected
            if player.money < towerTypes[monkeyName]["price"]: #MW: use a dictionary to search up the selected monkey's price and check if the player has enough money to buy the monkey
                #you don't have enough money to buy it
                player.selectedTower = None #MW: if the player doesn't have enough money to buy the monkey they want, no monkey will be selected 
            else: #MW: this section runs if a monkey has been selected and the player can afford to buy the monkey
                monkey = Tower(player.selectedTower) #MW: the selected monkey is turned into a tower object
                #check if monkey is placed in a "legal" area
                if monkey.legalPlacements(x,y): #MW: using the coordinates at the centre of the monkey, the code checks if the player is allowed to place the monkey where they want to place it
                    monkey.rect.center = [x,y]
                    monkey.originalImageRect.center = [x,y] #MW: if the player was allowed to place the monkey at a specific set of coordinates, the monkey's coordinates will be set to those (the coordinates are based on the centre of the monkey)
                    monkey.sellButtonRect.center = [x, y + 50]
                    monkey.upgradeButtonRect.center = [x, y - 50] 
                    monkey.drawUpgradePriceRect.center = [x, y - 70] #MW: The coordinates of the monkey's upgrade and sell buttons will be set accordingly (ex. the sell button will always be 50 units above the middle of the monkey)
                    player.towers.add(monkey) #MW: the monkey that has been placed will be added to the player's sprite group of tower objects
                    player.money -= towerTypes[monkeyName]["price"] #MW: after placing the monkey, the player's money will decrease based on the price of the monkey
                    player.selectedTower = None #reset selected tower

    def mousePressed(self, event): #MW: creates a function that checks if the user has clicked somewhere with their mouse and responds to it (the event parameter gathers information such as what mouse button was clicked and what coordinates were clicked)
        x, y = event.pos[0], event.pos[1] #MW: collect the coordinates where the mouse was clicked

        if player.gameOver == True:
            return #MW: the player has lost the game, "return" will prevent the rest of the function from running (the player can't click things and keep playing the game after losing)

        mouse = pygame.sprite.Sprite() #MW: a sprite for the mouse is made
        mouse.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1)) #MW: a rectangle is made around the mouse to create a hit box for it

        self.pressedButton(x,y) #MW: the pressedButton function uses the coordinates of the mouse obtained in this function to see if the player has clicked a button and responds accordingly

        #draw the range if you click on a monkey
        for monkey in player.towers:
            if monkey.selected == True:
                #check if player clicked "sell" button
                sell = monkey.sellButtonRect #MW: creates a rectangle containing the sell button (makes a hit box for the sell button)
                if x > sell[0] and x < sell[0] + sell[2]:
                    if y > sell[1] and y < sell[1] + sell[3]:
                        monkey.sell() #MW: if the player has clicked within the rectangle containing the sell button, the monkey the player wants to sell is sold
                        break #MW: after the code finds the correct monkey from the group of towers to delete, the for loop ends (there's no need to keep checking if the sell button for a monkey has been clicked)
                #check if player clicked "upgrade" button
                upgrade = monkey.upgradeButtonRect #MW: creates a rectangle around the upgrade button (makes a hit box for the upgrade button)
                if x > upgrade[0] and x < upgrade[0] + upgrade[2]:
                    if y > upgrade[1] and y < upgrade[1] + upgrade[3]: #MW: checks if the player has clicked within the rectangle containing the upgrade button
                        if monkey.upgraded == False:
                            name = monkey.name + "_upgraded" #MW: if the monkey hasn't already been upgrades, the monkey's name is changed to the original name with "_upgraded" at the end (there are dictionary entries for the upgraded versions of the monkeys that contain new stats such as the monkey's price)
                            if player.money >= towerTypes[name]["upgrade_price"]: #MW: check if the player's monkey is greater than equal to price of the upgrade (check if the player can afford to upgrade the monkey)
                                monkey.upgrade() #MW: the monkey is upgraded
                                #remove the upgrade button and price
                                monkey.removeUpgradeButton()
                                break #MW: the for loop ends because there is no need for the code to keep looping through all of the placed monkeys if the correct one has already been upgraded
                if monkey.upgraded == True:
                    monkey.removeUpgradeButton() #MW: if the monkey the player has selected has already been upgraded, the upgrade button no longer appears
            monkey.selected = False #MW: after the selected monkey has already been sold or upgraded, the player is no longer selecting a monkey
            if pygame.sprite.collide_rect(mouse, monkey): #MW: if the rectangles (hit boxes) of the mouse and a monkey collide, that means the user wants to select a monkey
                #select a monkey if you click it
                monkey.selected = True

    #makes bloons move across map
    def moveBloons(self, bloonsList):
        for bloon in bloonsList:

            speed = bloon.speed #MW: the speed of each bloon in the bloon list is collected
            x = bloon.rect.centerx
            y = bloon.rect.centery #MW: the x and y coordinates of each bloon are set to the centres of each bloon

            if player.game == "map1" or player.game == "tutorial": #MW: checks if the map the player is playing is the first map or the tutorial
                lastWaypoint = 19 #MW: there are 19 waypoints before the end of map
                if bloon.waypoint == lastWaypoint:
                    bloon.move(-speed, 0) #MW: if the bloon is at the last waypoint before the end of the map, it stop moving in the y direction and starts moving left in the x direction (at this section of the map, the path requires the bloon to move in this way)
                    if x <= -5: #check if bloon has moved past the map
                        player.lives -= bloon.strength
                        bloon.kill() #MW: the player's health is depleted according to the bloon's strength and the bloon is removed from the map after going off of the screen
                        if player.lives <= 0:
                            player.gameOver = True
                            player.lives = 0 #MW: if the player has run out of lives, the player has lost the game and the player's lives is set to 0 (if a bloon makes the player's health a negative number, the player's health will still end up being zero)

                else: #MW: this section runs if the bloon hasn't made it to the last waypoint (it's not close to the end of the map yet)
                    if bloon.direction == 'right':
                        bloon.move(speed, 0) #MW: if the bloon is facing right, the bloon will only move in the x direction at its speed
                        if x in Coord.waypoints[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the x coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)
                    elif bloon.direction == 'down':
                        bloon.move(0, speed) #MW: if the bloon is facing down, the bloon only moves down in the y direction
                        if y in Coord.waypoints[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the y coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)
                    elif bloon.direction == 'left':
                        bloon.move(- speed, 0) #MW: if the bloon is facing left, the bloon only moves left in the x direction
                        if x in Coord.waypoints[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the x coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints[bloon.waypoint][1]
                    elif bloon.direction == 'up':
                        bloon.move(0, - speed) #MW: if the bloon is facing up, the bloon only moves up in the y direction
                        if y in Coord.waypoints[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the y coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)

            elif player.game == "map2": #MW: run if the current map is "map 2"
                lastWaypoint = 12 #MW: there are 12 waypoints before the end of the map
                if bloon.waypoint == lastWaypoint: #MW: run if the bloon is at the last waypoint
                    bloon.move(-speed, 0) #MW: if the bloon is at the last waypoint, the bloon starts moving left (needs to move that way because of the way the path is structured)
                    if x <= -5: #check if bloon has moved past the map
                        player.lives -= bloon.strength
                        bloon.kill() #MW: removes the amount of strength from the bloon from the player's lives and removes the bloon from the screen
                        if player.lives <= 0:
                            player.gameOver = True
                            player.lives = 0 #MW: if the player runs out of lives, the game is over and the number of lives the player has is set to 0 (if the bloon made the player have a negative number of lives, they will still have zero lives at the end)

                else: #MW: run if the bloon isn't at the last waypoint
                    if bloon.direction == 'right':
                        bloon.move(speed, 0) #MW: if the bloon is facing right, the bloon only moves right in the x direction
                        if x in Coord.waypoints2[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the x coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)
                    elif bloon.direction == 'down':
                        bloon.move(0, speed) #MW: if the bloon is facing down, the bloon only moves down in the y direction
                        if y in Coord.waypoints2[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the y coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)
                    elif bloon.direction == 'left': 
                        bloon.move(- speed, 0) #MW: if the bloon is facing left, the bloon only moves left in the x direction
                        if x in Coord.waypoints2[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the x coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)
                    elif bloon.direction == 'up': 
                        bloon.move(0, - speed) #MW: if the bloon is facing up, the bloon only moves up in the y direction
                        if y in Coord.waypoints2[bloon.waypoint + 1][0]: #MW: using a directory of waypoints, check if the y coordinate of the bloon is within a range of points that depends on the location of the bloon in relation to other waypoints and the map
                            bloon.waypoint += 1 #MW: the waypoint being looked at is changed to the next one (the next range of points for the next waypoint will be looked at next time)
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1] #MW: the bloon faces the corresponding direction (the dictionary full of hard coded waypoints helps the bloon change directions depending on where the turns in the path are on the map)

            player.screen.blit(bloon.image,(bloon.rect)) #MW: draw the bloons onto the screen with rectangles drawn under them to act as hit boxes

    #draws lives, money, and level number on the sidebar
    def drawPlayerStats(self):
        white = (255,255,255) #MW: creates a variable for the colour white using RGB values

        fontSize = 25 #MW: set the font size to 25
        fontSizeLevel = 20 #MW: set the font size for the text that displays the level to 20

        font = pygame.font.SysFont("myriadpro", fontSize) #MW: for the regular font, use the myriad pro font with a font size of 25
        levelFont = pygame.font.SysFont("myriadpro", fontSizeLevel) #MW: for the font that displays the level, use the myriad pro font with a font size of 20

        lives = font.render(str(player.lives), 1, white) #MW: make the text that displays the number of lives the regular font with a white colour
        livesPos = lives.get_rect() #MW: get a rectangle that defines the boundaries of where the lives text is placed on screen
        livesPos.center = (890, 68) #MW: set the centre of the lives text to the coordinates (890, 68)
        
        money = font.render(str(player.money), 1, white) #MW: make the text that displays the player's money use the regular font with a white colour
        moneyPos = money.get_rect() #MW: get a rectangle that defines the boundaries of where the money text is placed on screen
        moneyPos.center = (890, 30) #MW: set the centre of the lives text to the coordinates (890, 30)

        levelNumber = levelFont.render("Level %d/10" % player.level, 1, white) #MW: make the text that displays the current level number use the level font with a white colour
        levelNumberPos = levelNumber.get_rect() #MW: get a rectangle that defines the boundaries of where the current level text is placed on screen
        levelNumberPos.center = (890, 120) #MW: set the centre of the lives text to the coordinates (890, 120)

        player.screen.blit(lives, livesPos) #draw lives
        player.screen.blit(money, moneyPos) #draw money
        player.screen.blit(levelNumber, levelNumberPos) #draw level number

    def drawMusicButton(self): #MW: create a function that draws the music button
        if Music.play == False:
            #draw a red line over the music button if paused
            redLine = pygame.image.load('images/red_line.png') #MW: import the red lilne image
            redLine.convert() #MW: convert the image to same pixel format of the screen it's supposed to display on (this makes using .blit() to draw it on screen faster)
            player.screen.blit(redLine, (918,533)) #MW: draw the red line on the screen on top of the music button

    def drawAllMonkeys(self): #MW: create a function that draws the monkeys placed on screen
        for monkey in player.towers:
            monkey.draw(player.screen) #MW: for every monkey in the sprite group that contains towers that are placed on the field, draw the monkey on screen

    def drawBullets(self): #MW: createa  function that draws the bullets the monkeys shoot
        for bullet in player.bullets:
            player.screen.blit(bullet.image, bullet.rect) #MW: for every bullet in the group of bullet sprites, draw the bullets on the screen along with a rectangle that acts as their hit box (needed to see if the bullets collide with the bloons and deal damage)

    #if you hover over a monkey then you can see the price and description
    def drawPrices(self):
        x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] #MW: get the x and y coordinate of the mouse

        if Tower.clickedMonkeys(x,y) != None: #MW: run if the mouse hasn't clicked on a monkey but is hovering over one
            monkey = Tower.clickedMonkeys(x,y) 
            white = (255,255,255) #MW: create the colour white using RGB values

            priceFontSize = 20 #MW: set the font  size of the price to 20
            priceFont = pygame.font.SysFont("myriadpro", priceFontSize) #MW: make the font size of the price 20 and use the myriad pro font
            price = priceFont.render("Price: $%d" % 
                towerTypes[monkey]["price"], 1, white) #MW: using the dictionary containing information on each monkey, display the corresponding price of the monkey the mouse is hovering over

            pricePos = price.get_rect() #MW: get a rectangle that covers all of the price text (acts as a hit box)
            pricePos.center = (890, 405) #MW: set the centre of the price text to the point (890, 405)

            descriptionFontSize = 13 #MW: set the description font size to 13
            descriptionFont = pygame.font.SysFont("myriadpro", 
                descriptionFontSize) #MW: for the description font use the myriad pro font and make the font size 13
            desc = descriptionFont.render(towerTypes[monkey]["description"], 
                1, white) #MW: make the description text by using the description font, using white text, and using the towerTypes dictionary to display the appropriate description for the selected monkey

            descriptionPos = desc.get_rect() #MW: create a rectangle that covers all of the description (to act as a hit box)
            descriptionPos.center = (890, 428) #MW: set the centre of the description to the point (890, 428)

            player.screen.blit(price, pricePos) #MW: draw the price text on the screen
            player.screen.blit(desc, descriptionPos) #MW: draw the description text on the screen

    def redrawAll(self): #MW: create a function to draw everything the player needs to see on the screen
        self.drawMusicButton()
        self.drawAllMonkeys()
        self.drawBullets()
        self.drawPlayerStats() #MW: draw the music button, all monkeys placed on the field, bullets, and the player's stats on the screen

    def initializeSplashScreen(self): #MW: create function to draw the main menu on the screen
        self.splashScreen = pygame.image.load("images/splash_screen.png").convert() #MW: get the splash screen image and convert it to the same pixel format of the display screen to reduce rendering time
        player.screen.blit(self.splashScreen, (0,0)) #MW: draw the main menu in the top left of the screen

    def splashScreenMousePressed(self, event): #MW: create a function to respond to clicking different parts of the main menu
        x, y = event.pos[0], event.pos[1]
        if y > 404 and y < 586:
            if x > 11 and x < 318: #MW: if the player clicks the area where the tutorial button is, the level will now be the "tutorial"
                return "tutorial" #tutorial level
            elif x > 328 and x < 631: #MW: if the player clicks the area where the middle map is, the level will now be "map 1"
                return "map1" #center map
            elif x > 649 and x < 956: #MW: if the player clicks the area where the rightmost map is, the level will now be "map 2"
                return "map2" #rightmost map

    def tutorialPressed(self): #MW: create a function that runs the tutorial level
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #MW: if the event that occurs is the player pressing the mouse button down, this section of code runs
                self.tutorialPage += 1 #MW: every time the player clicks the screen, the next step of the tutorial is displayed
                self.map = pygame.image.load("images/map1.png")
                self.map.convert() #MW: "map 1" is loaded and converted to decrease render time when drawing the image
                player.game = map #MW: collects the current map being used so it can be drawn
                player.__init__() #reset player values
                player.spriteBloons == Levels.runLevel(0) #MW: the bloons for the tutorial are generated
            elif event.type == QUIT:
                pygame.quit()
                sys.exit() #MW: if the player quits the game, pygame quits and the system exits (the program stops running and the game is closed)

    def run(self): #MW: create a function that actually runs the game

        clock = pygame.time.Clock() #MW: create clock object (deals with managing time and creating loops)
        screen = pygame.display.set_mode((self.width, self.height)) #MW: the width and height of the screen are set as the ones set in the player class
        # set the title of the window
        pygame.display.set_caption(self.title)

        self.splashScreenActive = True #MW: the main menu is shown on the screen

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.__init__()
        playing = True #MW: set playing to True to show that the player is currently playing the game (used in the while loop below)

        while playing: #MW: loop this section while the player is playing the game
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] #MW: get the position of the player's mouse

            if self.splashScreenActive == True: 
                self.tutorial = False #MW: if the main menu is being shown, the tutorial isn't being shown
                self.initializeSplashScreen() #MW: function is called to draw the main menu on the screen
                for event in pygame.event.get(): #MW: use a for loop to look through every event in pygame
                    if event.type == pygame.MOUSEBUTTONDOWN: #MW: check if the event that's occuring is the player clicking the screen
                        if self.splashScreenMousePressed(event) != None: #MW: check if the player has clicked a button on the main menu yet
                            if self.splashScreenMousePressed(event) == "tutorial": #MW: check if the player has clicked the tutorial button
                                self.tutorial = True
                                self.tutorialPage = 1 #MW: initialize the first tutorial step to one (you start playing the tutorial at step one)
                                self.splashScreenActive = False #MW: the tutorial begins and is shown on the screen and the main menu is turned off
                                player.__init__() #reset player values
                                player.spriteBloons == Levels.runLevel(0) #MW: make the sprite group of bloons the one for the first level
                            else: #MW: run if another map was clicked in the main menu
                                map = self.splashScreenMousePressed(event) #MW: change the current map to the one that was clicked (either map 1 or map 2)
                                self.map = pygame.image.load("images/%s.png" % map) #MW: load the image for the corresponding map
                                self.map.convert() #MW: convert the map png to reduce rendering time when drawing it
                                player.game = map #MW: gets the current map being used so it can be drawn on the screen
                                self.splashScreenActive = False #MW: the main menu has been turned off
                                player.__init__() #reset player values
                                player.spriteBloons == Levels.runLevel(0) #MW: make the sprite group of bloons the one for the first level
                    elif event.type == QUIT: #MW: check if the user wants to quit the game
                        pygame.quit()
                        sys.exit() #MW: pygame and the screen is turned off and the code stops running

            elif self.tutorial == True: #MW: check if the user is currently playing the tutorial
                self.map = pygame.image.load("images/slide%d.png" % self.tutorialPage).convert() #MW: the tutorial map is imported as the map and "convert" is used to reduce rendering time when drawing the map on the screen
                player.screen.blit(self.map, (0,0)) #MW: draw the map starting from the top left corner of the screen
                self.drawPlayerStats() #MW: draw all of the player's stats on the screen
                self.drawPrices() #MW: draw the price of the monkeys on the screen (if they're hovered over with the mouse)
                for event in pygame.event.get(): #MW: use for loop to check all events that are happening
                    if event.type == pygame.MOUSEBUTTONDOWN: #MW: check if the player clicked the mouse button
                        if self.tutorialPage == 7: #MW: check if the player has made it to the last step of the tutorial
                            self.tutorial = False
                            self.splashScreenActive = True #MW: the tutorial ends and the main menu is shown on screen again
                        else:
                            self.tutorialPage += 1 #MW: if the player hasn't made it to the last step of the tutorial, add a new step to the tutorial
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit() #MW: if the player wants to quit the game, pygame stops, the screen closes, and the code stops running

            elif player.gameOver == True: #MW: check if the player has lost the game
                self.lost = pygame.image.load("images/lost.png").convert() #MW: load the image with the lost screen and use .convert() to reduce rendering time when drawing it
                player.screen.blit(self.lost, (0,0)) #MW: draw the image starting at the top left of the screen
                for event in pygame.event.get(): #MW: check all events happening
                    if event.type == pygame.MOUSEBUTTONDOWN: #MW: check if the player is clicking on the screen
                        if x > 223 and x < 723:
                            if y > 343 and y < 410: #MW: check if the player clicked the button that says "back to home"
                                #go back to splash screen
                                player.gameOver = False 
                                self.splashScreenActive = True #MW: the player goes back to the main menu
                    elif event.type == QUIT: #MW: check if the player wants to quit the game
                        pygame.quit()
                        sys.exit() #MW: if the player wants to quit the game, pygame stops, the screen closes, and the code stops running

            elif player.gameWon == True: #MW: check if the player has won the game
                self.won = pygame.image.load("images/won.png").convert() #MW: import the image that tells the user they won teh game and use .convert() to reduce rendering time when drawing the image
                player.screen.blit(self.won, (0,0)) #MW: draw the image starting from the top left of the screen
                for event in pygame.event.get(): #MW: check all events
                    if event.type == pygame.MOUSEBUTTONDOWN: #MW: check if the user clicked on the screen
                        if x > 223 and x < 723:
                            if y > 343 and y < 410: #MW: check if the user clicks the button that says "back to home"
                                #go back to splash screen
                                player.gameWon = False #MW: the player has no longer won a game after going back to the main menu
                                self.splashScreenActive = True #MW: the player goes back to the main menu
                    elif event.type == QUIT: #MW: check if the player wants to quit the game
                        pygame.quit()
                        sys.exit() #MW: if the player wants to quit the game, pygame stops, the screen closes, and the code stops running

            else: #MW: this section rusn if the player isn't on the main menu, tutorial, and hasn't won or lost the game
                self.initializeMap() #MW: draw the map immage on the screen
                self.timerFired() #MW: draw the monkeys' bullets on screen according to the type of monkey and cooldown time (if applicable to that monkey time)
                self.moveBloons(player.spriteBloons) #MW: make the bloons move across the screen

                if player.selectedTower != None: #MW: check if the player hasn't selected a monkey
                    monkeyName = player.selectedTower #MW: the monkey being selected is changed according to the monkey the player clicked on screen
                    if player.money >= towerTypes[monkeyName]["price"]: #MW: check if the player can afford to buy the monkey (if the player's money is equal to or greater than the monkey's price, they can buy it)
                        monkeyName = player.selectedTower
                        monkey = Tower(monkeyName) #MW: the monkey selected becomes one of the towers placed on the field
                        legal = monkey.legalPlacements(x, y) #MW: collects the coordinates where the monkey can be placed
                        monkey.drawMonkeyAndRange(legal, x, y) #MW: draw a circle showing the monkey's range and make the circle red if the monkey cannot be placed at the coordinate the player's mouse is at

                for monkey in player.towers: #MW: go through all monkeys placed on the field
                    if monkey.selected == True: #MW: check if the player has selected a monkey
                        monkey.drawRangeAndSell(player.screen) #MW: draw the range of the selected monkey and the upgrade/sell button

                for event in pygame.event.get(): #MW: check all pytgame events
                    if event.type == pygame.MOUSEBUTTONDOWN: #MW: check if the player has clicked on the screen
                        self.mousePressed(event) #MW: check if the player has clicked somewhere with their mouse and responds accordingly
                    elif event.type == KEYDOWN: #MW: check if the player has clicked a key on the keyboard
                        if event.key == K_ESCAPE: #MW: check if the "esc" key has been clicked
                            #press "esc" key to deselect a tower
                            player.selectedTower = None
                    elif event.type == QUIT: #MW: check if the user wants to quit the game
                        pygame.quit()
                        sys.exit() #MW: if the player wants to quit the game, pygame stops, the screen closes, and the code stops running

                if player.spriteBloons == None or len(player.spriteBloons) == 0: #MW: check if there are no bloons on the field
                    pass #MW: nothing needs to be checked if the game isn't going on

                self.redrawAll() #MW: draw the music button, all monkeys placed on the field, bullets, and the player's stats on the screen
                self.drawPrices() #MW: draw the prices of the monkeys on the screen
                player.checkGameOver(player.spriteBloons) #MW: check if the game is over and makes all bloons stop moving if that is the case
                player.checkGameWon(player.spriteBloons) #MW: check if the game has been won and changes the screen to show the winning screen

            pygame.display.flip() #MW: display everything on the screen ("flip" updates the screen to the show the lastest rednered frame, which is needed when images are moving across the screen)
            clock.tick(self.fps) #MW: use the clock object and .tick() to set the frame rate of the game to 40 fps

        pygame.quit() #MW: pygame quits and no more pygame operations can be used (the whole game has been run and you no longer need to use pygame operations)

def main(): #MW: create a main function to run the Game() function
    game = Game() 
    game.run() #MW: run everything in the Game() function

if __name__ == '__main__':
    main() #MW: if this file is run directly (not imported file), then the main function will run (which makes the game start)