#!/usr/bin/env python
# coding: utf-8

import pygame
from pygame.locals import *
from classes import player, map, camera, item, camp
from Client import producer, consumer
from functions import recup_message

NB_JOUEURS = 4
NB_PIECES = 3

MAX_FPS = 60
FONT_SIZE = 16
FONT_STYLE = None
KEY_REPEAT_DELAY = 1000  # milliseconds

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

LINE_THIKNESS = 20
SCOREBOARD_TOP_X = WINDOW_WIDTH * 6 / 8
SCOREBOARD_TOP_Y = WINDOW_HEIGHT - NB_JOUEURS * LINE_THIKNESS

BASE_ROUGE_X = 0
BASE_ROUGE_Y = 0

BASE_BLEUE_X = 0
BASE_BLEUE_Y = 0

ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)


class Jeu():
    def __init__(self, nom_joueur, socket):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Broken pipe')
        self.font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.font_accueil = pygame.font.Font("pixelmix.ttf", 32)
        self.socket = socket
        self.nom_joueur = nom_joueur
        # map
        self.map = map.Map(self.screen)

        self.distribution_spawn(self.map)

        self.camps = pygame.sprite.Group()
        self.camp_rouge = camp.Camp(0, BASE_ROUGE_X, BASE_ROUGE_Y, "Camp Rouge", "rouge")
        self.camp_bleu = camp.Camp(1, BASE_BLEUE_X, BASE_BLEUE_Y, "Camp Bleu", "bleu")
        self.camps.add(self.camp_rouge)
        self.camps.add(self.camp_bleu)

        self.screen.blit(self.font_accueil.render("Veuillez patienter...", False, (255, 255, 255)),
                         (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 - 100))
        pygame.display.flip()

        self.connexion()

        self.joueurs = pygame.sprite.Group()
        for i in range(len(self.idnom)):
            if i % 2 == 0:
                self.joueurs.add(player.Player(self, self.camp_rouge, i, self.idnom[i], BASE_ROUGE_X, BASE_ROUGE_Y))
            else:
                self.joueurs.add(player.Player(self, self.camp_bleu, i, self.idnom[i], BASE_BLEUE_X, BASE_BLEUE_Y))

        self.current_player = self.playerById(self.id_client)

        self.groupe_attaque = pygame.sprite.Group()

        self.items = pygame.sprite.Group()
        self.items_taken = pygame.sprite.Group()

        i = 0
        for obj in self.map.objets:
            if obj[0] == "1": # ROUGE
                self.items.add(
                    item.Item(self, "pieces/piece_rouge.png", int(obj[1][0]), int(obj[1][1]), i, self.camp_rouge))
            elif obj[0] == "2": # BLEU
                self.items.add(
                    item.Item(self, "pieces/piece_bleu.png", int(obj[1][0]), int(obj[1][1]), i, self.camp_bleu))
            i += 1

        # definition du sprite controlable
        self.current_player.setControllable(True)
        # creation du producteur et du consommateur
        self.consumer = consumer.Consumer(self.socket, self)
        self.producer = producer.Producer(self.socket, self)
        # run des 2 thread qui envoie les donnees
        self.consumer.start()
        self.producer.start()


        # load de toutes les musiques + bruitages
        pygame.mixer.music.load("sounds/fondSonore.ogg")
        pickCoins = pygame.mixer.Sound("sounds/pickCoins.ogg")
        missCoins = pygame.mixer.Sound("sounds/missCoins.ogg")
        select = pygame.mixer.Sound("sounds/select.ogg")
        victoire = pygame.mixer.Sound("sounds/victory.ogg")
        defaite = pygame.mixer.Sound("sounds/defeat.ogg")

        # declenchement du fond sonore
        pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.5)

        # La camera
        largeur_map = self.map.layer1.largeur_map * self.map.layer1.x_tile
        hauteur_map = self.map.layer1.hauteur_map * self.map.layer1.y_tile
        self.cam = camera.Camera(self, camera.complex_camera, largeur_map, hauteur_map)

        # repetition des touches
        pygame.key.set_repeat(5, 20)

        clock = pygame.time.Clock()
        timeLastAttack = pygame.time.get_ticks()

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
                        self.current_player.setSpeed(0)

                        if timeLastAttack + KEY_REPEAT_DELAY < pygame.time.get_ticks():
                            self.current_player.updateAttaque()
                            self.groupe_attaque.add(self.current_player.attaque)

                            group_sans_J = [j for j in self.joueurs if j.classe != self.id_client]

                            # On test le collide du joueur et de l'epee
                            target = pygame.sprite.spritecollide(self.current_player.attaque, group_sans_J, False)
                            self.current_player.attack(target)

                            timeLastAttack = pygame.time.get_ticks()

                    if event.key == K_e:
                        coins = pygame.sprite.spritecollide(self.current_player, self.items, False)
                        # On ne garde que les pieces n'appartenant pas au camp du joueur
                        coins = [it for it in coins if it.camp != self.current_player.camp]

                        if coins:
                            if self.current_player.pickUpItem(coins):
                                pickCoins.play()
                                self.items.remove(coins)
                                self.items_taken.add(coins)
                            else:
                                missCoins.play()

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.current_player.setSpeed(player.VELOCITY)
                        self.groupe_attaque.remove(self.current_player.attaque)


            # Verification de la victoire
            if len(self.camp_rouge.pieces_depart) <= 0:
                if self.current_player.camp.nom == "Camp Rouge":
                    pygame.mixer.music.stop()
                    defaite.play()
                else:
                    pygame.mixer.music.stop()
                    victoire.play()

                print "LES BLEUS ONT GAGNE, BRAVO !!"
                break

            elif len(self.camp_bleu.pieces_depart) <= 0:
                if self.current_player.camp.nom == "Camp Bleu":
                    pygame.mixer.music.stop()
                    defaite.play()
                else:
                    pygame.mixer.music.stop()
                    victoire.play()

                print "LES ROUGES ONT GAGNE, BRAVO !!"
                break

            collision_camp = pygame.sprite.collide_rect(self.current_player, self.current_player.camp)
            if collision_camp and len(self.current_player.items) > 0:
                self.current_player.deposerItem()

            self.joueurs.update()

            self.groupe_attaque.update()

            # Gestion de la camera
            self.cam.update(self.current_player)  # Centre sur le joueur

            # rafraichissement de la map des des affichages des joueurs
            self.map.afficher_map(self.cam)

            if self.groupe_attaque:
                self.groupe_attaque.clear(self.screen, self.current_player.attaque.image)
                self.groupe_attaque.draw(self.current_player.attaque.image)
                self.screen.blit(self.current_player.attaque.image,
                                 self.cam.apply(self.current_player.attaque))

            # On blit les camps
            for c in self.camps:
                self.screen.blit(c.image, self.cam.apply(c))

            # On blit les joueurs
            for j in self.joueurs:
                self.screen.blit(j.image, self.cam.apply(j))

            # On blit les items
            for it in self.items:
                self.screen.blit(it.image, self.cam.apply(it))

            pygame.display.update()

            # Affichage des infos joueurs
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


    # recuperer un joueur par son id
    def playerById(self, id_player):
        for j in self.joueurs:
            if j.classe == id_player:
                return j


    def itemById(self, id_item):
        for i in self.items:
            if i.id_item == id_item:
                return i


    def campById(self, id_camp):
        for c in self.camps:
            if c.id_camp == id_camp:
                return c

    # Affiche le scoreboard
    def displayScore(self, joueur, xAbs, yAbs):
        handlebar = joueur.getHealthbar()

        name = handlebar.getName()[:11]
        name += (17 - len(name)) * " "

        joueur_text = self.font.render(name + "  :  " + handlebar.getLife(), True, (0, 0, 0))
        joueur_rect = joueur_text.get_rect()
        joueur_rect.topleft = (xAbs, yAbs)

        self.screen.blit(joueur_text, joueur_rect)

    def distribution_spawn(self, map_jeu):
        spawn = map_jeu.getSpawn()
        global BASE_ROUGE_NB, BASE_ROUGE_X, BASE_ROUGE_Y
        global BASE_BLEUE_NB, BASE_BLEUE_X, BASE_BLEUE_Y

        BASE_ROUGE_NB = 0
        BASE_ROUGE_X = spawn[0][0]
        BASE_ROUGE_Y = spawn[0][1]

        BASE_BLEUE_NB = 1
        BASE_BLEUE_X = spawn[1][0]
        BASE_BLEUE_Y = spawn[1][1]

    def connexion(self):
        print "Connexion au serveur..."
        print "Recuperation du numero client"
        self.id_client = int(recup_message(self.socket))
        print "Vous etes le client numero " + str(self.id_client)

        # creation du jeu
        nbr_players_string = recup_message(self.socket)
        self.nbr_players = int(nbr_players_string.split(" ")[1])

        self.idnom = []
        for i in range(self.nbr_players):
            self.idnom.append('')

        self.socket.send("NAME " + str(self.id_client) + " " + self.nom_joueur + '@')

        self.idnom[self.id_client] = self.nom_joueur
        for i in range(0, nbr_players - 1):
            resultat = recup_message(self.socket)
            donnee = resultat.split(' ')
        self.idnom[int(donnee[1])] = donnee[2]
