import pygame
import tuile as _tuile


class Layer():

    def __init__(self,screen,fichier,image,x_tile=32,y_tile=32,):
        #fenetre ou ajouter
        self.screen = screen
        #image du calque
        self.tilset = pygame.image.load(image).convert_alpha()
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
        #collision
        self.collision = False
        self.tuiles = pygame.sprite.Group()


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
                    tile = self.tilset.subsurface(X,Y,hauteur,largeur)
                    if self.isCollision():
                        tuile = _tuile.Tuile(tile,x,y)
                        self.tuiles.add(tuile)
                    else:
                        self.screen.blit(tile,(x,y))
                x+=largeur
            else:
                y+=hauteur
                x=0
        self.tuiles.draw(self.screen)

    def isCollision(self):
        return self.collision


    def setCollision(self,collision=True):
        self.collision = collision