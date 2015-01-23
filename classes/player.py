__author__ = 'Simon'
import pygame
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #images du personnage
        self.droite = pygame.image.load("images/personnage_1_droite.png").convert_alpha()
        self.gauche = pygame.image.load("images/personnage_1_gauche.png").convert_alpha()
        self.haut = pygame.image.load("images/personnage_1_haut.png").convert_alpha()
        self.bas = pygame.image.load("images/personnage_1_bas.png").convert_alpha()
        #image actuelle du personnage
        self.image = self.droite
        #position de depart du personnage
        self.case_x=0
        self.case_y=0
        self.x=0
        self.y=0
        self.rect = self.image.get_rect()

    def deplacer(self, direction):
        if direction == 'droite':
            self.case_x +=1
            self.setX(3)
            self.image = self.droite
        elif direction == 'gauche':
            self.case_x -=1
            self.setX(-3)
            self.image = self.gauche
        elif direction == 'haut':
            self.case_y -=1
            self.setY(-3)
            self.image = self.haut
        elif direction == 'bas':
            self.case_y +=1
            self.setY(3)
            self.image = self.bas

    def setX(self,x):
        self.rect.x += x

    def setY(self,y):
            self.rect.y += y