__author__ = 'Simon'
import pygame
from pygame.locals import *

class Jeu():


    def __init__(self,width=300,height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Play game')

        while True :
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
            pygame.display.flip()


