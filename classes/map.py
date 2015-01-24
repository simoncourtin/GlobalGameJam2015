__author__ = 'Simon'
import  pygame
import layer
from pygame.locals import *
import sys
class Map():

    def __init__(self,screen):
        self.spawn = []
        self.calques = []
        self.screen =screen
        self.layer1 = layer.Layer(self.screen,"maps/cobblestone2/background.txt",'maps/cobblestone2/cobblestone.png',False,30,30)
        self.calques.append(self.layer1)
        self.layer2 = layer.Layer(self.screen,"maps/cobblestone2/collision.txt",'maps/cobblestone2/cobblestone.png',True,30,30)
        self.calques.append(self.layer2)
        self.layer3 = layer.Layer(self.screen,"maps/cobblestone2/spawn.txt",'maps/cobblestone2/cobblestone.png',False,30,30)
        self.calques.append(self.layer3)
        self.spawn=self.layer3.spawn
    def afficher_map(self, camera):
        for calque in self.calques:
            calque.afficher_layer(camera)

    def getSpawn(self):
        return self.spawn








