import pygame
import tuile as _tuile


class Layer():

    def __init__(self,screen,fichier,image,collision=False,objet=False,x_tile=32,y_tile=32,):
        #fenetre ou ajouter
        self.screen = screen

        #tilset de l'image du calque
        self.tilset = pygame.image.load(image).convert_alpha()

        #definition si claque de collision
        self.collision = collision

        #definition si calque d'objet interactif
        self.layer_objet = objet

        #hauteur et largeur des tuile dans le tilset
        self.x_tile=x_tile
        self.y_tile=y_tile

        #creation des groupe des tuile de collision et non collision
        self.tuiles_colision = pygame.sprite.Group()
        self.tuiles_non_colision = pygame.sprite.Group()

        #tableau des spawn et des objet interactif
        self.spawn = []
        self.objets =[]

        #largeur de la map
        self.largeur_map = 0
        self.hauteur_map = 0

        #Debut de le creation du calque
        #lecture du fichier
        self.f = open(fichier, "r")
        self.ligne = self.f.read()
        self.ligne = self.ligne.replace('\n','\n,')

        #generation du tableau pour les differents element du calque
        self.calque=[]
        self.calque= self.ligne.split(',')
        self.construire_layer()


    def construire_layer(self):
        hauteur = self.x_tile
        largeur = self.y_tile
        x=0
        y=0
        for element in self.calque:
            if element != '\n':
                self.largeur_map += 1
                if element!='0':
                    X = (((int(element))-(((int(element)-1)/16)*16))-1)*32
                    Y=(int(element)/16)*32
                    if(Y==512):
                        Y= 512-32
                    tile = self.tilset.subsurface(X,Y,hauteur,largeur)
                    tuile = _tuile.Tuile(tile,x,y)
                    if self.isCollision():
                        self.tuiles_colision.add(tuile)
                    elif self.layer_objet:
                        self.objets.append((element,(x,y)))
                    else:
                        self.tuiles_non_colision.add(tuile)
                    if element == '256':
                        self.tuiles_non_colision.remove(tuile)
                        self.spawn.append((x ,y))
                x+=largeur
            else:
                y+=hauteur
                x=0

                self.hauteur_map += 1
                self.largeur_map = 0

    def afficher_layer(self, cam):
        for tuile_c in self.tuiles_colision:
            self.screen.blit(tuile_c.image, cam.apply(tuile_c))
        for tuile_nc in self.tuiles_non_colision:
            self.screen.blit(tuile_nc.image, cam.apply(tuile_nc))

    def isCollision(self):
        return self.collision

    def setCollision(self,collision=True):
        self.collision = collision

    def setLayerObjet(self,objet=True):
        self.layer_objet = objet

    def isLayerObjet(self):
        return  self.layer_objet
