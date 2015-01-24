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
        
        self.joueurs = pygame.sprite.Group()
        self.joueurs.add(player.Player(0,self))
        self.joueurs.add(player.Player(1,self))
        self.joueurs.add(player.Player(2,self))
        self.joueurs.add(player.Player(3,self))

        groupe_sansJ = pygame.sprite.Group()
        for j in self.joueurs:
            if not j is self.playerById(self.id_client):
                groupe_sansJ.add(j)
        
        #definition du sprite controlable
        self.playerById(self.id_client).setControllable(True)
        #creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        #run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()
        #repetition des touches
        pygame.key.set_repeat(5,20)
        clock = pygame.time.Clock()
        colliding = 0
        #LOOP
        while True :
            clock.tick(MAX_FPS)
            #gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return
            

            
            collision=pygame.sprite.spritecollide(self.playerById(self.id_client),groupe_sansJ,False)
            
            for other in collision:
                self.playerById(self.id_client).life -= 10
                print 'hit'
                if (self.playerById(self.id_client).life <= 0):
                    print "You dead"
            """
            if len(collision) > 1:
                if(colliding==1):
                    print collision
                    if(len(collision) == 1):
                        colliding=0
                        print collision
                else:
                    print collision
                    if(len(collision) > 1):
                        colliding=1
                        print 'encule !'+str(self.id_client)
                        self.playerById(self.id_client).life-=10
                        if(self.playerById(self.id_client).life==0):
                            print("perdu")
                            return
            """
    
            self.screen.fill((0,0,0))
            self.joueurs.update()
            self.joueurs.draw(self.screen)
            pygame.display.flip()

    def playerById(self, id_player):
        for j in self.joueurs:
            if j.classe == id_player:
                return j
    
    def deplacer(self, x, y) :
        print str(y)