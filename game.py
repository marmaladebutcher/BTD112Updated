import pygame
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

class Game(object):

    player = Player()

    def __init__(self, width=966, height=598, fps=40):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = "Bloons Tower Defense 112: By Sarah Wang"
        pygame.init()

        pygame.mixer.music.load('btd_theme.ogg')
        pygame.mixer.music.play(-1) #-1 means play forever

    def initializeMap(self):
        player.screen.blit(self.map, (0,0))

    def timerFired(self):
        if player.gameOver == False:

            #creates bullet if monkey is not on cooldown
            for monkey in player.towers:
                if "sniper" in monkey.name:
                    monkey.shootBloons()
                    if monkey.ready:
                        bloon = Tower.furthestBloon(player.spriteBloons)
                        if bloon != None:
                            sniperStrength = towerTypes[monkey.name]["damage"]
                            bloon.updateDamage(sniperStrength,0,player.screen)
                else:
                    monkey.shootBloons()

            #updates bullets (make them move toward targets)
            for bullet in player.bullets:
                bullet.update(player.screen)

    def pressedButton(self, x, y):

        #pressed start button
        if x > 829 and x < 952 and y > 461 and y < 500:
            #only start next level when player just started, or completed level
            if player.spriteBloons == None or len(player.spriteBloons) == 0:
                player.level += 1
                if player.level < 11:
                    player.spriteBloons = Levels.runLevel(player.level)
                else:
                    player.level = 10
                    player.gameWon = True

        #pressed monkey sidebar
        if x > 825 and x < 950 and y > 140 and y < 380:
            #check what monkey you clicked on
            player.selectedTower = Tower.clickedMonkeys(x, y)

        #pressed music button
        if x > Coord.music[0][0] and y < Coord.music[0][1]:
            if y > Coord.music[1][0] and y < Coord.music[1][1]:
                Music.play = not Music.play
                if Music.play == True:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()

        #pressed home button
        if x > 840 and x < 872 and y > 538 and y < 568:
            self.splashScreenActive = True

        #place a monkey onto the canvas
        if player.selectedTower != None:
            monkeyName = player.selectedTower
            if player.money < towerTypes[monkeyName]["price"]:
                #you don't have enough money to buy it
                player.selectedTower = None
            else:
                monkey = Tower(player.selectedTower)
                #check if monkey is placed in a "legal" area
                if monkey.legalPlacements(x,y):
                    monkey.rect.center = [x,y]
                    monkey.originalImageRect.center = [x,y]
                    monkey.sellButtonRect.center = [x, y + 50]
                    monkey.upgradeButtonRect.center = [x, y - 50]
                    monkey.drawUpgradePriceRect.center = [x, y - 70]
                    player.towers.add(monkey)
                    player.money -= towerTypes[monkeyName]["price"]
                    player.selectedTower = None #reset selected tower

    def mousePressed(self, event):
        x, y = event.pos[0], event.pos[1]

        if player.gameOver == True:
            return

        mouse = pygame.sprite.Sprite()
        mouse.rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

        self.pressedButton(x,y)

        #draw the range if you click on a monkey
        for monkey in player.towers:
            if monkey.selected == True:
                #check if player clicked "sell" button
                sell = monkey.sellButtonRect
                if x > sell[0] and x < sell[0] + sell[2]:
                    if y > sell[1] and y < sell[1] + sell[3]:
                        monkey.sell()
                        break
                #check if player clicked "upgrade" button
                upgrade = monkey.upgradeButtonRect
                if x > upgrade[0] and x < upgrade[0] + upgrade[2]:
                    if y > upgrade[1] and y < upgrade[1] + upgrade[3]:
                        if monkey.upgraded == False:
                            name = monkey.name + "_upgraded"
                            if player.money >= towerTypes[name]["upgrade_price"]:
                                monkey.upgrade()
                                #remove the upgrade button and price
                                monkey.removeUpgradeButton()
                                break
                if monkey.upgraded == True:
                    monkey.removeUpgradeButton()
            monkey.selected = False
            if pygame.sprite.collide_rect(mouse, monkey):
                #select a monkey if you click it
                monkey.selected = True

    #makes bloons move across map
    def moveBloons(self, bloonsList):
        for bloon in bloonsList:

            speed = bloon.speed
            x = bloon.rect.centerx
            y = bloon.rect.centery

            if player.game == "map1" or player.game == "tutorial":
                lastWaypoint = 19 #waypoint before the end of map
                if bloon.waypoint == lastWaypoint:
                    bloon.move(-speed, 0)
                    if x <= -5: #check if bloon has moved past the map
                        player.lives -= bloon.strength
                        bloon.kill()
                        if player.lives <= 0:
                            player.gameOver = True
                            player.lives = 0

                else:
                    if bloon.direction == 'right':
                        bloon.move(speed, 0)
                        if x in Coord.waypoints[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints[bloon.waypoint][1]
                    elif bloon.direction == 'down':
                        bloon.move(0, speed)
                        if y in Coord.waypoints[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints[bloon.waypoint][1]
                    elif bloon.direction == 'left':
                        bloon.move(- speed, 0)
                        if x in Coord.waypoints[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints[bloon.waypoint][1]
                    elif bloon.direction == 'up':
                        bloon.move(0, - speed)
                        if y in Coord.waypoints[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints[bloon.waypoint][1]

            elif player.game == "map2":
                lastWaypoint = 12
                if bloon.waypoint == lastWaypoint:
                    bloon.move(-speed, 0)
                    if x <= -5: #check if bloon has moved past the map
                        player.lives -= bloon.strength
                        bloon.kill()
                        if player.lives <= 0:
                            player.gameOver = True
                            player.lives = 0

                else:
                    if bloon.direction == 'right':
                        bloon.move(speed, 0)
                        if x in Coord.waypoints2[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1]
                    elif bloon.direction == 'down':
                        bloon.move(0, speed)
                        if y in Coord.waypoints2[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1]
                    elif bloon.direction == 'left':
                        bloon.move(- speed, 0)
                        if x in Coord.waypoints2[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1]
                    elif bloon.direction == 'up':
                        bloon.move(0, - speed)
                        if y in Coord.waypoints2[bloon.waypoint + 1][0]:
                            bloon.waypoint += 1
                            bloon.direction = Coord.waypoints2[bloon.waypoint][1]

            player.screen.blit(bloon.image,(bloon.rect))

    #draws lives, money, and level number on the sidebar
    def drawPlayerStats(self):
        white = (255,255,255)

        fontSize = 25
        fontSizeLevel = 20

        font = pygame.font.SysFont("myriadpro", fontSize)
        levelFont = pygame.font.SysFont("myriadpro", fontSizeLevel)

        lives = font.render(str(player.lives), 1, white)
        livesPos = lives.get_rect()
        livesPos.center = (890, 68)
        
        money = font.render(str(player.money), 1, white)
        moneyPos = money.get_rect()
        moneyPos.center = (890, 30)

        levelNumber = levelFont.render("Level %d/10" % player.level, 1, white)
        levelNumberPos = levelNumber.get_rect()
        levelNumberPos.center = (890, 120)

        player.screen.blit(lives, livesPos) #draw lives
        player.screen.blit(money, moneyPos) #draw money
        player.screen.blit(levelNumber, levelNumberPos) #draw level number

    def drawMusicButton(self):
        if Music.play == False:
            #draw a red line over the music button if paused
            redLine = pygame.image.load('images/red_line.png')
            redLine.convert()
            player.screen.blit(redLine, (918,533))

    def drawAllMonkeys(self):
        for monkey in player.towers:
            monkey.draw(player.screen)

    def drawBullets(self):
        for bullet in player.bullets:
            player.screen.blit(bullet.image, bullet.rect)

    #if you hover over a monkey then you can see the price and description
    def drawPrices(self):
        x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

        if Tower.clickedMonkeys(x,y) != None:
            monkey = Tower.clickedMonkeys(x,y) 
            white = (255,255,255)

            priceFontSize = 20
            priceFont = pygame.font.SysFont("myriadpro", priceFontSize)
            price = priceFont.render("Price: $%d" % 
                towerTypes[monkey]["price"], 1, white)

            pricePos = price.get_rect()
            pricePos.center = (890, 405)

            descriptionFontSize = 13
            descriptionFont = pygame.font.SysFont("myriadpro", 
                descriptionFontSize)
            desc = descriptionFont.render(towerTypes[monkey]["description"], 
                1, white)

            descriptionPos = desc.get_rect()
            descriptionPos.center = (890, 428)

            player.screen.blit(price, pricePos)
            player.screen.blit(desc, descriptionPos)

    def redrawAll(self):
        self.drawMusicButton()
        self.drawAllMonkeys()
        self.drawBullets()
        self.drawPlayerStats()

    def initializeSplashScreen(self):
        self.splashScreen = pygame.image.load("images/splash_screen.png").convert()
        player.screen.blit(self.splashScreen, (0,0))

    def splashScreenMousePressed(self, event):
        x, y = event.pos[0], event.pos[1]
        if y > 404 and y < 586:
            if x > 11 and x < 318:
                return "tutorial" #tutorial level
            elif x > 328 and x < 631:
                return "map1" #center map
            elif x > 649 and x < 956:
                return "map2" #rightmost map

    def tutorialPressed(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.tutorialPage += 1
                self.map = pygame.image.load("images/map1.png")
                self.map.convert()
                player.game = map
                player.__init__() #reset player values
                player.spriteBloons == Levels.runLevel(0)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        self.splashScreenActive = True

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.__init__()
        playing = True

        while playing:
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

            if self.splashScreenActive == True:
                self.tutorial = False
                self.initializeSplashScreen()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.splashScreenMousePressed(event) != None:
                            if self.splashScreenMousePressed(event) == "tutorial":
                                self.tutorial = True
                                self.tutorialPage = 1
                                self.splashScreenActive = False
                                player.__init__() #reset player values
                                player.spriteBloons == Levels.runLevel(0)
                            else:
                                map = self.splashScreenMousePressed(event)
                                self.map = pygame.image.load("images/%s.png" % map)
                                self.map.convert()
                                player.game = map
                                self.splashScreenActive = False
                                player.__init__() #reset player values
                                player.spriteBloons == Levels.runLevel(0)
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            elif self.tutorial == True:
                self.map = pygame.image.load("images/slide%d.png" % self.tutorialPage).convert()
                player.screen.blit(self.map, (0,0))
                self.drawPlayerStats()
                self.drawPrices()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.tutorialPage == 7:
                            self.tutorial = False
                            self.splashScreenActive = True
                        else:
                            self.tutorialPage += 1
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            elif player.gameOver == True:
                self.lost = pygame.image.load("images/lost.png").convert()
                player.screen.blit(self.lost, (0,0))
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if x > 223 and x < 723:
                            if y > 343 and y < 410:
                                #go back to splash screen
                                player.gameOver = False
                                self.splashScreenActive = True
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            elif player.gameWon == True:
                self.won = pygame.image.load("images/won.png").convert()
                player.screen.blit(self.won, (0,0))
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if x > 223 and x < 723:
                            if y > 343 and y < 410:
                                #go back to splash screen
                                player.gameWon = False
                                self.splashScreenActive = True
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

            else:
                self.initializeMap()
                self.timerFired()
                self.moveBloons(player.spriteBloons)

                if player.selectedTower != None:
                    monkeyName = player.selectedTower
                    if player.money >= towerTypes[monkeyName]["price"]:
                        monkeyName = player.selectedTower
                        monkey = Tower(monkeyName)
                        legal = monkey.legalPlacements(x, y)
                        monkey.drawMonkeyAndRange(legal, x, y)

                for monkey in player.towers:
                    if monkey.selected == True:
                        monkey.drawRangeAndSell(player.screen)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mousePressed(event)
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            #press "esc" key to deselect a tower
                            player.selectedTower = None
                    elif event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                if player.spriteBloons == None or len(player.spriteBloons) == 0:
                    pass

                self.redrawAll()
                self.drawPrices()
                player.checkGameOver(player.spriteBloons)
                player.checkGameWon(player.spriteBloons)

            pygame.display.flip()
            clock.tick(self.fps)

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()