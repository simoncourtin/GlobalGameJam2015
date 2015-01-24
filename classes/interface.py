from gtweak.tweaks.tweak_group_test import screen
__author__ = 'Simon'
import pygame
from pygame.locals import *

class Interface(pygame.sprite.Sprite):

    def __init__(self,  player, screen):
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.screen = screen
        
    def displayScoreJoueur(self, player):
        resultSurf = BASICFONT.render('Vie : %s' %(player.life), True, (0,0,0))
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (700, 25)
        DISPLAYSURF.blit(resultSurf, resultRect)