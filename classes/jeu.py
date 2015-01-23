__author__ = 'Simon'
import pygame
from pygame.locals import *
from classes import player
class Jeu():


    def __init__(self,width=300,height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Play game')
        self.id_client = 0
        self.joueurs = []
        self.joueurs.append(player.Player())
        self.joueurs.append(player.Player())
        self.joueurs[1].setX(20)
        self.joueurs[1].setY(20)
        self.afficherJoueur()
        
        while True :
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            pygame.display.flip()
    
    def afficherJoueur(self):
        for joueur in self.joueurs:
            self.screen.blit(joueur.image,(joueur.rect.x,joueur.rect.y))
        
