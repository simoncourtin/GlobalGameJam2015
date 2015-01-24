__author__ = 'Simon'
import pygame
from pygame.locals import *
VELOCITY=3

class Player(pygame.sprite.Sprite):

    def __init__(self,  jeu, classe = 0):
        pygame.sprite.Sprite.__init__(self)
        self.classe = classe
        self.xAbs = 0
        self.yAbs = 0
        self.jeu = jeu
        #images du personnage
        if classe == 0 :
            self.droite = pygame.image.load("images/sprite_profile.png").convert_alpha()
            self.gauche = pygame.transform.flip(self.droite,True,False)
            self.haut = pygame.image.load("images/sprite_dos.png").convert_alpha()
            self.bas = pygame.image.load("images/sprite_face.png").convert_alpha()
        elif classe ==1  :
            self.droite = pygame.image.load("images/sprite2_profile.png").convert_alpha()
            self.gauche = pygame.transform.flip(self.droite,True,False)
            self.haut = pygame.image.load("images/sprite2_dos.png").convert_alpha()
            self.bas = pygame.image.load("images/sprite2_face.png").convert_alpha()
        elif classe ==2  :
            self.droite = pygame.image.load("images/sprite3_profile.png").convert_alpha()
            self.gauche = pygame.transform.flip(self.droite,True,False)
            self.haut = pygame.image.load("images/sprite3_dos.png").convert_alpha()
            self.bas = pygame.image.load("images/sprite3_face.png").convert_alpha()
        elif classe ==3  :
            self.droite = pygame.image.load("images/sprite4_profile.png").convert_alpha()
            self.gauche = pygame.transform.flip(self.droite,True,False)
            self.haut = pygame.image.load("images/sprite4_dos.png").convert_alpha()
            self.bas = pygame.image.load("images/sprite4_face.png").convert_alpha()
        
        w,h=self.droite.get_size()
        self.droite = pygame.transform.scale(self.droite, (w*5, h*5))
        w,h=self.gauche.get_size()
        self.gauche = pygame.transform.scale(self.gauche, (w*5, h*5))
        w,h=self.haut.get_size()
        self.haut = pygame.transform.scale(self.haut, (w*5, h*5))
        w,h=self.bas.get_size()
        self.bas = pygame.transform.scale(self.bas, (w*5, h*5))
        #image actuelle du personnage
        self.image = self.droite
        self.rect.x = 400 - w/2
        self.rect.y = 400 - h/2
        #position de depart du personnage
        self.rect = self.image.get_rect()
        self.image
        #caracteristique du player
        
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
            
            
    def changerPosition(self,direction):
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
                self.x_velocite =0
            if not keys[K_UP] and not keys[K_DOWN]:
                self.y_velocite =0
            
            self.jeu.deplacer(self.x_velocite,self.y_velocite)
            self.xAbs += self.x_velocite
            self.yAbs += self.y_velocite
    
    def setControllable(self, boolean) :
        self.is_controllable = True
        if boolean :
            h,w = self.image.get_size()
            self.rect.x = 400 - w/2
            self.rect.y = 400 - h/2