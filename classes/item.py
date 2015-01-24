__author__ = 'Simon'
import pygame
from pygame.locals import *

class Item(pygame.sprite.Sprite):

    BASE_RESSOURCE = "images/"

    def __init__(self,  jeu, resource, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.jeu = jeu
        self.resource = BASE_RESSOURCE + resource
        self.rect.x=x
        self.rect.y=y
        self.image=pygame.image.load(self.resource)
        self.screen = self.jeu.screen
        self.visible = True
        
    def afficherItem(self, jeu):
        self.screen.blit(self.image, (self.rect.x,self.rect.y))
<<<<<<< HEAD

    def setVisible(self,bool):
        self.visible=bool
        
=======
>>>>>>> origin/master
