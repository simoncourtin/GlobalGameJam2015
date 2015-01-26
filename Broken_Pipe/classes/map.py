__author__ = 'Simon'
import  pygame
import layer
from pygame.locals import *
import sys
class Map():

    def __init__(self,screen,information_claque):
        self.spawn = []
        self.objets = []
        self.calques = []
        #tableau sous forme [(schema sur la map, tilset ,calque de collision, calque d'objet, taille x des tiles ,taille y des tiles),(...)]
        self.futureCalques = information_claque
        self.screen =screen
        #definition des layer:
        #1ere couche
        """
        self.layer1 = layer.Layer(self.screen,"maps/cobblestone2/background.txt",'maps/cobblestone2/cobblestone.png',False,False,30,30)
        self.calques.append(self.layer1)
        #2eme couche
        self.layer2 = layer.Layer(self.screen,"maps/cobblestone2/collision.txt",'maps/cobblestone2/cobblestone.png',True,False,30,30)
        self.calques.append(self.layer2)
        #3eme couche
        self.layer3 = layer.Layer(self.screen,"maps/cobblestone2/spawn.txt",'maps/cobblestone2/cobblestone.png',False,False,30,30)
        self.calques.append(self.layer3)
        self.spawn=self.layer3.spawn
        #4eme couche
        self.layer4 = layer.Layer(self.screen,"maps/cobblestone2/piece.txt",'maps/cobblestone2/piece_tile.png',False,True,30,30)
        self.calques.append(self.layer3)
        self.objets=self.layer4.objets
        """
        self.buildLayerOnMap()

    def buildLayerOnMap(self):
        for layer_elem in self.futureCalques:
            calque = layer.Layer(self.screen,layer_elem[0],layer_elem[1],layer_elem[2],layer_elem[3],layer_elem[4],layer_elem[5])
            self.calques.append(calque)
            if len(calque.spawn)>0:
                self.spawn= calque.spawn
            if calque.isLayerObjet:
                self.objets=calque.objets


    def afficher_map(self, camera):
        for calque in self.calques:
            calque.afficher_layer(camera)

    def getSpawn(self):
        return self.spawn
    def getObjets(self):
        return self.objets

"""
screen = pygame.display.set_mode((100,100))
carte = Map(screen,[("../maps/cobblestone2/background.txt",'../maps/cobblestone2/cobblestone.png',False,False,32,32),
            ("../maps/cobblestone2/collision.txt",'../maps/cobblestone2/cobblestone.png',True,False,32,32),
            ("../maps/cobblestone2/spawn.txt",'../maps/cobblestone2/cobblestone.png',False,False,32,32),
            ("../maps/cobblestone2/piece.txt",'../maps/cobblestone2/piece_tile.png',False,True,32,32)])
print carte.spawn
"""



