import pygame
#MW: import pygame module

class Player(pygame.sprite.Sprite): #MW: create class for the player

    def __init__(self): #MW: create instance for the player's stats (ex. money availble, health, level, etc.)
        self.money = 600 #MW: set the player's initial money to 600
        self.lives = 100 #MW: set the player's initial health to 100
        self.level = 0 #MW: set the player's initial level to 0
        self.start = False
        self.gameOver = False #MW: the game is not over at the beginning
        self.gameWon = False #MW: the game hasn't been won at the begin
        self.screen = pygame.display.set_mode((966, 598)) #MW: display the background image

        self.spriteBloons = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.selectedTower = None #MW: the player hasn't initially selected a tower
        self.bullets = pygame.sprite.Group() #MW: create bullet objects

    def checkGameOver(self, group): #MW: create a class that checks if the game is over
        if self.gameOver == True:
            for bloon in group:
                bloon.speed = 0 #MW: if the game is over, the bloons stop moving (the game stops)

    def checkGameWon(self, group): #MW: create a class that checks if the game has been won
        if self.level == 10 and len(group) == 0: #no bloons left in level 10
            self.gameWon = True
        #MW: if no bloons are left in level 10 (the last level) the player wins the game

class Music(object):
    play = True #MW: play the background music