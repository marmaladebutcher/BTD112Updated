import pygame
#MW: import pygame module

class Player(pygame.sprite.Sprite): #MW: create class for the player

    def __init__(self): #MW: create instance for the player's stats (ex. money availble, health, level, etc.)
        self.money = 600 #MW: set the player's initial money to 600
        self.lives = 100 #MW: set the player's initial health to 100
        self.level = 0 #MW: set the player's initial level to 0
        self.start = False #MW: the game has not started at the beginning (the main menu is open at the start)
        self.gameOver = False #MW: the game is not over at the beginning
        self.gameWon = False #MW: the game hasn't been won at the begin
        self.screen = pygame.display.set_mode((966, 598)) #MW: create window for the game with dimensions of 966 pixels wide by 598 pixels tall 

        self.spriteBloons = pygame.sprite.Group() #MW: create group of sprites for the bloons
        self.towers = pygame.sprite.Group() #MW: create group of sprites
        self.selectedTower = None #MW: the player hasn't initially selected a tower
        self.bullets = pygame.sprite.Group() #MW: create group of bullet object sprites

    def checkGameOver(self, group): #MW: create a function that checks if the game is over
        if self.gameOver == True:
            for bloon in group:
                bloon.speed = 0 #MW: if the game is over, all bloons stop moving (the game stops)

    def checkGameWon(self, group): #MW: create a function that checks if the game has been won
        if self.level == 10 and len(group) == 0: #no bloons left in level 10
            self.gameWon = True
        #MW: if no bloons are left in level 10 (the last level) the player wins the game

class Music(object): #Mw: creates a new-style class to play the music (new-style classes work better with object oriented programming)
    play = True #MW: play the background music