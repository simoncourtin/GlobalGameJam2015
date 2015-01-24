__author__ = 'Simon'
import pygame
import math
class Layer():

    def __init__(self,screen,fichier,x_tile=32,y_tile=32):
        #fenetre ou ajouter
        self.screen = screen
        #image du calque
        self.mur = pygame.image.load('../maps/cobblestone/mur.png').convert_alpha()
        self.plant = pygame.image.load('../maps/cobblestone/grass.png').convert_alpha()
        self.tilset = pygame.image.load('../maps/cobblestone/cobblestone.png').convert_alpha()
        #lecture du fichier
        self.f = open(fichier, "r")
        self.ligne = self.f.read()
        self.ligne = self.ligne.replace('\n','\n,')
        #generation du tableau pour les differents element du calque
        self.calque=[]
        self.calque= self.ligne.split(',')
        #hauteur et largeur des tuile
        self.x_tile=x_tile
        self.y_tile=y_tile


    def afficher_layer(self):
        hauteur = self.x_tile
        largeur = self.y_tile
        x=0
        y=0
        for element in self.calque:
            if element != '\n':
                if element!='0':
                    X = (((int(element))-(((int(element)-1)/16)*16))-1)*32
                    Y=(int(element)/16)*32
                    print element,X, Y
                    self.screen.blit(self.tilset.subsurface(X,Y,hauteur,largeur),(x,y))
                x+=largeur
            else:
                y+=hauteur
                x=0