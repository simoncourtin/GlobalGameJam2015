__author__ = 'Simon'
import  pygame
import layer
from pygame.locals import *
import sys
class Map():

    def __init__(self,screen):
        self.calques = []
        self.screen =screen
        self.layer1 = layer.Layer(self.screen,"maps/cobblestone/background.txt",'maps/cobblestone/cobblestone.png',False,30,30)
        self.calques.append(self.layer1)
        self.layer2 = layer.Layer(self.screen,"maps/cobblestone/collision.txt",'maps/cobblestone/cobblestone.png',True,30,30)
        self.calques.append(self.layer2)

    def afficher_map(self):
        for calque in self.calques:
            calque.afficher_layer()






