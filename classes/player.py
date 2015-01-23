__author__ = 'Simon'
import pygame
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #images du personnage
        self.droite = pygame.image.load("images/sprite_profile.png").convert_alpha()
        self.gauche = pygame.transform.flip(self.droite,False,True)
        self.haut = pygame.image.load("images/sprite_dos.png").convert_alpha()
        self.bas = pygame.image.load("images/sprite_face.png").convert_alpha()
        #image actuelle du personnage
        self.image = self.droite
        #position de depart du personnage
        self.rect = self.image.get_rect()

    def deplacer(self, direction):
        if direction == 'droite':
            self.setX(3)
            self.image = self.droite
        elif direction == 'gauche':
            self.setX(-3)
            self.image = self.gauche
        elif direction == 'haut':
            self.setY(-3)
            self.image = self.haut
        elif direction == 'bas':
            self.setY(3)
            self.image = self.bas

    def setX(self,x):
        self.rect.x += x

    def setY(self,y):
            self.rect.y += y