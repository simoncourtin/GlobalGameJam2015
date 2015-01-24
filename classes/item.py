__author__ = 'Simon'
import pygame
from pygame.locals import *

BASE_RESSOURCE = "images/"

class Item(pygame.sprite.Sprite):

    def __init__(self,  jeu, resource, x, y ,camp = None):
        pygame.sprite.Sprite.__init__(self)
        self.jeu = jeu
        self.resource = BASE_RESSOURCE + resource
        self.image=pygame.image.load(self.resource)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.screen = self.jeu.screen
        self.visible = True
        self.camp = camp
        
    def afficherItem(self, jeu):
        self.screen.blit(self.image, (self.rect.x,self.rect.y))

    def setVisible(self,bool):
        self.visible=bool

    def setCamp(self,camp):
        self.camp=camp
