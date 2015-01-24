__author__ = 'Simon'
import threading
import pygame
import time
from pygame.locals import *
from classes import player , map, interface
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
        self.joueurs.add(player.Player(self,0))
        self.joueurs.add(player.Player(self,1))
        self.joueurs.add(player.Player(self,2))
        self.joueurs.add(player.Player(self,3))

        groupe_sansJ = pygame.sprite.Group()
        for j in self.joueurs:
            if not j is self.playerById(self.id_client):
                groupe_sansJ.add(j)
        
        self.HUD = interface.Interface(self)
        
        #definition du sprite controlable
        self.playerById(self.id_client).setControllable(True)
        #creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        #run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()
        #map
        self.map = map.Map(self.screen)
        #repetition des touches
        pygame.key.set_repeat(5,20)
        clock = pygame.time.Clock()
        colliding = 0
        tempsAvantHit = 0
        tempsApresHit = 0
        #LOOP
        while True :
            clock.tick(MAX_FPS)
            #gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return
            
            #marqueur avant collision
            tempsAvantHit=time.time()
            #collision avec les autres joueurs
            collision=pygame.sprite.spritecollide(self.playerById(self.id_client),groupe_sansJ,False)
            #collision avec le decors
            collision_decors= pygame.sprite.spritecollide(self.playerById(self.id_client),self.map.layer2.tuiles,False)
            if tempsApresHit-tempsAvantHit > 2:
                for other in collision:
                    self.playerById(self.id_client).life -= 10
                    print 'hit'
                    tempsApresHit=time.time()
                    
                    if (self.playerById(self.id_client).life <= 0):
                        print "You dead"
    
            self.HUD.displayScoreJoueur(self.playerById(self.id_client))
            
            #gestion collision avec le decors
            #for other in collision_decors:

            #rafraichissement de la map des des affichages des joueurs
            self.map.afficher_map()
            self.joueurs.update()
            self.joueurs.draw(self.screen)
            pygame.display.flip()
    #recuperer je joueur controlle par le client
    def playerById(self, id_player):
        for j in self.joueurs:
            if j.classe == id_player:
                return j
    #deplacer la map
    def deplacer(self, x, y) :
        #decaller map
        print str(y)
