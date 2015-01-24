import pygame
import time
from pygame import sprite
from pygame.locals import *
from classes import player, map, interface, camera, item
from Client import producer, consumer


NB_JOUEURS = 4
NB_PIECES = 3

MAX_FPS = 60
FONT_SIZE = 16
FONT_STYLE = None
KEY_REPEAT_DELAY = 2000  # milliseconds

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

LINE_THIKNESS = 20
SCOREBOARD_TOP_X = WINDOW_WIDTH * 6 / 8
SCOREBOARD_TOP_Y = WINDOW_HEIGHT - NB_JOUEURS * LINE_THIKNESS


class Jeu():
    def __init__(self, id_client, socket, idnom, width=300, height=300):
        pygame.init()
        self.idnom = idnom
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Broken pipe')
        self.font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.id_client = id_client
        self.socket = socket
        # map
        self.map = map.Map(self.screen)
        self.spawn = self.map.getSpawn()
        if len(self.spawn) > 0:
            x = self.spawn[0][0]
            y = self.spawn[0][1]

        self.joueurs = pygame.sprite.Group()
        self.joueurs.add(player.Player(self, 0, self.idnom[0], x, y))
        self.joueurs.add(player.Player(self, 1, self.idnom[1], x, y))
        self.joueurs.add(player.Player(self, 2, self.idnom[2], x, y))
        self.joueurs.add(player.Player(self, 3, self.idnom[3], x, y))

        self.items = pygame.sprite.Group()
        self.items_taken = pygame.sprite.Group()
        for i in range(NB_PIECES):
            for j in range(NB_PIECES):
                self.items.add(item.Item(self, "sprite_coins.png", 200 + 50 * j, 200 + 50 * i, "rouge"))

        self.items.add(item.Item(self, "sprite_coins.png", 10, 10, "bleu"))

        # definition du sprite controlable
        self.playerById(self.id_client).setControllable(True)
        # creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        # run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()


        # load de toutes les musiques + bruitages
        pygame.mixer.music.load("fondSonore.ogg")
        pygame.mixer.music.queue("fondSonore.ogg")
        pickCoins = pygame.mixer.Sound("pickCoins.ogg")
        missCoins = pygame.mixer.Sound("missCoins.ogg")
        select = pygame.mixer.Sound("select.ogg")

        # declenchement du fond sonore
        pygame.mixer.music.play()
        # pygame.mixer.music.set_volume(0.5)

        # La camera
        largeur_map = self.map.layer1.largeur_map * self.map.layer1.x_tile
        hauteur_map = self.map.layer1.hauteur_map * self.map.layer1.y_tile
        self.cam = camera.Camera(self, camera.complex_camera, largeur_map, hauteur_map)

        # repetition des touches
        pygame.key.set_repeat(5, 20)

        clock = pygame.time.Clock()
        timeFirst = pygame.time.get_ticks()
        
        self.groupe_attaque = pygame.sprite.Group()
        self.groupe_attaque.add(self.playerById(self.id_client).attaque)
        # LOOP
        while True:
            clock.tick(MAX_FPS)

            # gestion des evenement
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.socket.send("QUIT")
                    self.socket.close()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.playerById(self.id_client).setSpeed(0)

                        if timeFirst + KEY_REPEAT_DELAY < pygame.time.get_ticks():
                            target = pygame.sprite.spritecollide(self.playerById(self.id_client), self.joueurs, False)
                            self.playerById(self.id_client).attack(target)
                            timeFirst = pygame.time.get_ticks()

                    if event.key == K_e:
                        coins = pygame.sprite.spritecollide(self.playerById(self.id_client), self.items, False)
                        if coins:
                            if self.playerById(self.id_client).pickUpItem(coins):
                                pickCoins.play()
                                self.items.remove(coins)
                                self.items_taken.add(coins)
                            else:
                                missCoins.play()

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.playerById(self.id_client).setSpeed(player.VELOCITY)

            self.joueurs.update()

            # rafraichissement de la map des des affichages des joueurs
            self.cam.update(self.playerById(self.id_client))
            
            if (self.playerById(self.id_client)).attaque.getVisible() :
                self.groupe_attaque.draw(self.playerById(self.id_client).attaque.image)
                #self.screen.blit(self.playerById(self.id_client).attaque.image,self.cam.apply(self.playerById(self.id_client).attaque))
                #self.playerById(self.id_client).afficher_attaque = False


            # rafraichissement de la map des des affichages des joueurs
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

                self.displayScore(joueur, SCOREBOARD_TOP_X, SCOREBOARD_TOP_Y + LINE_THIKNESS * (id + 1))

                if id == self.id_client:
                    text, rect = joueur.getHealthbar().displayLife(joueur.getX() - 20, joueur.getY() - 10)
                    self.screen.blit(text, self.cam.apply_rect(rect))

            pygame.display.flip()

            # pygame.draw.line(self.screen, (180, 0, 0), (SCOREBOARD_TOP_X, SCOREBOARD_TOP_Y), (WINDOW_WIDTH * 2 / 8, SCOREBOARD_TOP_Y), 50)


    # recuperer je joueur controlle par le client
    def playerById(self, id_player):
        for j in self.joueurs:
            if j.classe == id_player:
                return j


    def displayScore(self, joueur, xAbs, yAbs):
        handlebar = joueur.getHealthbar()

        name = handlebar.getName()[:11]
        name += (17 - len(name)) * " "

        joueur_text = self.font.render(name + "  :  " + handlebar.getLife(), True, (0, 0, 0))
        joueur_rect = joueur_text.get_rect()
        joueur_rect.topleft = (xAbs, yAbs)

        self.screen.blit(joueur_text, joueur_rect)
