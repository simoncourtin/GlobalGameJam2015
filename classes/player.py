__author__ = 'Simon'
import pygame
from pygame.locals import *

VELOCITY = 3

BASE_RESSOURCE = "images/"
RESSOURCES_J1 = ["sprite_profile.png", "sprite_dos.png", "sprite_face.png"]
RESSOURCES_J2 = ["sprite2_profile.png", "sprite2_dos.png", "sprite2_face.png"]
RESSOURCES_J3 = ["sprite3_profile.png", "sprite3_dos.png", "sprite3_face.png"]
RESSOURCES_J4 = ["sprite4_profile.png", "sprite4_dos.png", "sprite4_face.png"]


class Player(pygame.sprite.Sprite):
    def __init__(self, jeu, classe=0):
        pygame.sprite.Sprite.__init__(self)
        self.classe = classe
        self.jeu = jeu

        # images du personnage
        if classe == 0:
            ressources = RESSOURCES_J1
        elif classe == 1:
            ressources = RESSOURCES_J2
        elif classe == 2:
            ressources = RESSOURCES_J2
        elif classe == 3:
            ressources = RESSOURCES_J2

        self.droite = pygame.image.load(BASE_RESSOURCE + ressources[0])
        self.gauche = pygame.transform.flip(self.droite, True, False)
        self.haut = pygame.image.load(BASE_RESSOURCE + ressources[1]).convert_alpha()
        self.bas = pygame.image.load(BASE_RESSOURCE + ressources[2]).convert_alpha()

        w, h = self.droite.get_size()
        self.droite = pygame.transform.scale(self.droite, (w * 5, h * 5))
        w, h = self.gauche.get_size()
        self.gauche = pygame.transform.scale(self.gauche, (w * 5, h * 5))
        w, h = self.haut.get_size()
        self.haut = pygame.transform.scale(self.haut, (w * 5, h * 5))
        w, h = self.bas.get_size()
        self.bas = pygame.transform.scale(self.bas, (w * 5, h * 5))
        # image actuelle du personnage
        self.image = self.droite
        # position de depart du personnage
        self.rect = self.image.get_rect()
        self.is_controllable = False
        self.life = 100
        self.speed = 1
        self.force = 1
        #la velocite
        self.x_velocite = 0
        self.y_velocite = 0

    def deplacer(self, direction):
        if direction == 'droite':
            self.x_velocite = VELOCITY
            self.image = self.droite
        elif direction == 'gauche':
            self.x_velocite = -VELOCITY
            self.image = self.gauche
        elif direction == 'haut':
            self.y_velocite = -VELOCITY
            self.image = self.haut
        elif direction == 'bas':
            self.y_velocite = VELOCITY
            self.image = self.bas


    def changerPosition(self, direction):
        if direction == 'droite':
            self.image = self.droite
        elif direction == 'gauche':
            self.image = self.gauche
        elif direction == 'haut':
            self.image = self.haut
        elif direction == 'bas':
            self.image = self.bas
    
    def setX(self,x):
        self.rect.x += x

    def setY(self,y):
            self.rect.y += y
   

    def getDirection(self):
        if self.image == self.droite:
            direction = 1
        elif self.image == self.gauche:
            direction = 2
        elif self.image == self.haut:
            direction = 3
        elif self.image == self.bas:
            direction = 4
        return direction

    def update(self):
        if self.is_controllable:
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.deplacer("haut")
            if keys[K_DOWN]:
                self.deplacer("bas")
            if keys[K_RIGHT]:
                self.deplacer("droite")
            if keys[K_LEFT]:
                self.deplacer("gauche")
            if not keys[K_LEFT] and not keys[K_RIGHT]:
                self.x_velocite = 0
            if not keys[K_UP] and not keys[K_DOWN]:
                self.y_velocite =0
            
            self.setX(x)
            self.setY(y)
    
    def setControllable(self, boolean):
        self.is_controllable = boolean
