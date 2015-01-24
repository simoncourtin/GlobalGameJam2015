__author__ = 'Simon'
import threading
import pygame
from pygame.locals import *
from classes import player
from Client import producer, consumer

MAX_FPS = 60

class Jeu():


    def __init__(self,id_client,socket,width=300,height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        pygame.display.set_caption('Broken pipe')
        self.id_client = id_client
        self.socket = socket
        
        #self.joueurs = pygame.sprite.Group()
        #self.joueurs.add(player.Player(0))
        #self.joueurs.add(player.Player(1))
        #self.joueurs.add(player.Player(2))
        #self.joueurs.add(player.Player(3))
        
        #declaration du groupe des joueurs
        player_group=pygame.sprite.RenderClear()
        
        #ajout des joueurs au groupe
        for i in range(0,3):
            player_group.add(player_group, player.Player(i))
        
        #definition du sprite controlable
        self.joueurs.sprites()[self.id_client].is_controllable = True
        #creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        #run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()
        #repetition des touches
        pygame.key.set_repeat(5,20)
        clock = pygame.time.Clock()
        #LOOP
        while True :
            clock.tick(MAX_FPS)
            #gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return
            collision=pygame.sprite.spritecollide(player,player_group,False,pygame.sprite.collide_circle_ratio(0.7))
            if(colliding==1):
                if(not collision):
                    colliding=0
            else:
                if(collision):
                    colliding=1
                    player.life-=10
                    if(player.life==0):
                        print("perdu")
                        return
                
            self.screen.fill((0,0,0))
            self.joueurs.update()
            self.joueurs.draw(self.screen)
            pygame.display.flip()
    
    
        
