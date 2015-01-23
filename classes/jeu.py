__author__ = 'Simon'
import threading
import pygame
from pygame.locals import *
from classes import player
from Client import producer, consumer

class Jeu():


    def __init__(self,id_client,socket,width=300,height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Play game')
        self.id_client = id_client
        self.socket = socket
        self.joueurs = []
        self.joueurs.append(player.Player())
        self.joueurs.append(player.Player())
        #creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        #run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()
        
        #LOOP
        while True :
            #gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.joueurs[self.id_client].deplacer("haut")
                    elif event.key == K_DOWN:
                        self.joueurs[self.id_client].deplacer("bas")
                    elif event.key == K_RIGHT:
                        self.joueurs[self.id_client].deplacer("droite")
                    elif event.key == K_LEFT:
                        self.joueurs[self.id_client].deplacer("gauche")
            self.screen.fill((0,0,0))
            self.afficherJoueur()
            pygame.display.flip()
    
    def afficherJoueur(self):
        for joueur in self.joueurs:
            self.screen.blit(joueur.image,(joueur.rect.x,joueur.rect.y))
        
