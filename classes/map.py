__author__ = 'Simon'
import  pygame
import layer
from pygame.locals import *
import sys
class Map():

    def __init__(self,screen):
        self.calques = []
        self.screen =screen
        self.calques.append(layer.Layer(self.screen,"../maps/cobblestone/collision.txt",30,30))

    def afficher_map(self):
        for calque in self.calques:
            calque.afficher_layer()





pygame.init()
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Play game')
map = Map(screen)
map.afficher_map()
pygame.display.flip()

while True:
    for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
