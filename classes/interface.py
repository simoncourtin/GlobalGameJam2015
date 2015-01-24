__author__ = 'Simon'
import pygame
from pygame.locals import *

class Interface(pygame.sprite.Sprite):

    def __init__(self,  jeu):
        pygame.sprite.Sprite.__init__(self)
        self.jeu = jeu
        self.jeu.playerById(self.id_client)
        self.jeu.screen
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        
    def displayScoreJoueur(self, player):
        resultSurf = self.font.render('Vie : %s' %(player.life), True, (0,0,0))
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (700, 25)
        self.screen.blit(resultSurf, resultRect)