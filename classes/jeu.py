import pygame
import time
from pygame.locals import *
from classes import player, map, interface, camera
from Client import producer, consumer


MAX_FPS = 60


class Jeu():
    def __init__(self, id_client, socket, width=300, height=300):
        pygame.init()

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
        self.joueurs.add(player.Player(self, 0))
        self.joueurs.add(player.Player(self, 1))
        self.joueurs.add(player.Player(self, 2))
        self.joueurs.add(player.Player(self, 3))

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
        self.cam = camera.Camera(self, camera.simple_camera, self.screen.get_rect().width,
                                 self.screen.get_rect().height)
        # repetition des touches
        pygame.key.set_repeat(5, 20)

        clock = pygame.time.Clock()
        timeFirst = pygame.time.get_ticks()

        # LOOP
        while True:
            clock.tick(MAX_FPS)

            # gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.close()
                    return

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if timeFirst + 3000 < pygame.time.get_ticks():
                            target = pygame.sprite.spritecollide(self.playerById(self.id_client), self.joueurs, False)
                            self.playerById(self.id_client).attack(target)

                            timeFirst = pygame.time.get_ticks()

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.playerById(self.id_client).setSpeed(player.VELOCITY)

            """
            self.HUD.displayScoreJoueur(self.playerById(self.id_client))
            """

            self.joueurs.update()

            self.cam.update(self.playerById(self.id_client))

            # rafraichissement de la map des des affichages des joueurs
            self.map.afficher_map(self.cam)
            for j in self.joueurs:
                self.screen.blit(j.image, self.cam.apply(j))

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
