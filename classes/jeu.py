__author__ = 'Simon'
import threading
import pygame
import time
from pygame.locals import *
from classes import player , map, interface, camera, item
from Client import producer, consumer


MAX_FPS = 60


class Jeu():
    def __init__(self, id_client, socket, idnom,width=300, height=300,):
        pygame.init()
        self.idnom = idnom
        NB_PIECES=3
        """
        global BASICFONT, BASICFONTSIZE
        BASICFONTSIZE = 20
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
        """

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Broken pipe')
        self.id_client = id_client
        self.socket = socket

        self.joueurs = pygame.sprite.Group()
        self.joueurs.add(player.Player(self, 0, idnom[0]))
        self.joueurs.add(player.Player(self, 1, idnom[1]))
        #self.joueurs.add(player.Player(self, 2,idnom[2]))
        #self.joueurs.add(player.Player(self, 3,idnom[3]))

        self.items = pygame.sprite.Group()
        for i in range(NB_PIECES):
            for j in range(NB_PIECES):
                self.items.add(item.Item(self, "sprite_coins.png", 200+50*j, 200+50*i, "rouge"))
    
        self.items.add(item.Item(self, "sprite_coins.png", 10, 10, "bleu"))
        
        groupe_sansJ = pygame.sprite.Group()
        for j in self.joueurs:
            if not j is self.playerById(self.id_client):
                groupe_sansJ.add(j)

        """
        self.HUD = interface.Interface(self)
        """

        # definition du sprite controlable
        self.playerById(self.id_client).setControllable(True)
        # creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        # run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()
        # map
        self.map = map.Map(self.screen)

        # La camera
        largeur_map = self.map.layer1.largeur_map * self.map.layer1.x_tile
        hauteur_map = self.map.layer1.hauteur_map * self.map.layer1.y_tile
        self.cam = camera.Camera(self, camera.complex_camera, largeur_map, hauteur_map)
        #repetition des touches
        pygame.key.set_repeat(5,20)

        clock = pygame.time.Clock()
        colliding = 0
        tempsAvantHit = 0
        tempsApresHit = 0
        
        #load de toutes les musiques + bruitages
        pygame.mixer.music.load("fondSonore.ogg")
        pygame.mixer.music.queue("fondSonore.ogg")
        hit=pygame.mixer.Sound("hit.wav")
        pickCoins=pygame.mixer.Sound("pickCoins.wav")
        respawn=pygame.mixer.Sound("respawn.wav")
        death=pygame.mixer.Sound("death.wav")
        select=pygame.mixer.Sound("select.wav")
        
        #declenchement du fond sonore
        pygame.mixer.music.play()
        
        # LOOP
        while True:
            clock.tick(MAX_FPS)
            # gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return

            # marqueur avant collision
            tempsAvantHit = time.time()
            # collision avec les autres joueurs
            collision = pygame.sprite.spritecollide(self.playerById(self.id_client), groupe_sansJ, False)
           
            #collisions avec les items
            collision_items = pygame.sprite.spritecollide(self.playerById(id_client), self.items, False)
            for it in collision_items:
                keys = pygame.key.get_pressed()
                if keys[K_SPACE]:
                    self.playerById(id_client).pickUpItem(it)
                    pickCoins.play()
            
            # collision avec le decors

            if tempsApresHit - tempsAvantHit > 2:
                for other in collision:
                    self.playerById(self.id_client).life -= 10
                    print 'hit'
                    tempsApresHit = time.time()

                    if (self.playerById(self.id_client).life <= 0):
                        print "You dead"

            """
            self.HUD.displayScoreJoueur(self.playerById(self.id_client))
            """

            self.joueurs.update()
            
            self.cam.update(self.playerById(self.id_client))
            if self.playerById(self.id_client).afficher_attaque :
                self.cam.update(self.playerById(self.id_client).attaque)
                self.playerById(self.id_client).afficher_attaque = False
            #rafraichissement de la map des des affichages des joueurs
            self.map.afficher_map(self.cam)
            for j in self.joueurs:
                self.screen.blit(j.image, self.cam.apply(j))
            
            for it in self.items:
                self.screen.blit(it.image, self.cam.apply(it))

            pygame.display.update()
            for id in range(len(self.joueurs.sprites())):
                joueur = self.playerById(id)

                text, rect = joueur.getHealthbar().displayName(joueur.getX() - 20, joueur.getY() - 20)
                self.screen.blit(text, self.cam.apply_rect(rect))

                if id == self.id_client:
                    text, rect = joueur.getHealthbar().displayLife(joueur.getX() - 20, joueur.getY() - 10)
                    self.screen.blit(text, self.cam.apply_rect(rect))

            pygame.display.flip()


    # recuperer je joueur controlle par le client
    def playerById(self, id_player):
        for j in self.joueurs:
            if j.classe == id_player:
                return j

    # deplacer la map
    def deplacer(self, x, y):
        # decaller map
        print str(y)
