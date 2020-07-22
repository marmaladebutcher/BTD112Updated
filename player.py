import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self):
        self.money = 600
        self.lives = 100
        self.level = 0
        self.start = False
        self.gameOver = False
        self.gameWon = False
        self.screen = pygame.display.set_mode((966, 598))

        self.spriteBloons = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.selectedTower = None
        self.bullets = pygame.sprite.Group()

    def checkGameOver(self, group):
        if self.gameOver == True:
            for bloon in group:
                bloon.speed = 0

    def checkGameWon(self, group):
        if self.level == 10 and len(group) == 0: #no bloons left in level 10
            self.gameWon = True


class Music(object):
    play = True