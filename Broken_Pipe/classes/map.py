__author__ = 'Simon'
import  pygame
import layer
from pygame.locals import *
import sys
class Map():

    def __init__(self,screen):
        self.spawn = []
        self.objets = []
        self.calques = []
        self.screen =screen
        #definition des layer:
        #1ere couche
        self.layer1 = layer.Layer(self.screen,"maps/cobblestone2/background.txt",'maps/cobblestone2/cobblestone.png',False,False,30,30)
        self.calques.append(self.layer1)
        #2eme couche
        self.layer2 = layer.Layer(self.screen,"maps/cobblestone2/collision.txt",'maps/cobblestone2/cobblestone.png',True,False,30,30)
        self.calques.append(self.layer2)
        #3eme couche
        self.layer3 = layer.Layer(self.screen,"maps/cobblestone2/spawn.txt",'maps/cobblestone2/cobblestone.png',False,False,30,30)
        self.calques.append(self.layer3)
        #4eme couche
        self.spawn=self.layer3.spawn
        self.layer4 = layer.Layer(self.screen,"maps/cobblestone2/piece.txt",'maps/cobblestone2/piece_tile.png',False,True,30,30)
        self.calques.append(self.layer3)
        self.objets=self.layer4.objets

    def afficher_map(self, camera):
        for calque in self.calques:
            calque.afficher_layer(camera)

    def getSpawn(self):
        return self.spawn
    def getObjets(self):
        return self.objets









