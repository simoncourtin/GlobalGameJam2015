
import pygame

CAMP_SIZE = 80

class Camp(pygame.sprite.Sprite):

    def __init__(self, id_camp, x, y, nom="equipe", couleur="rouge"):
        pygame.sprite.Sprite.__init__(self)
        if couleur=="rouge":
            self.couleur = ((255,0,0))
        elif couleur == "vert":
            self.couleur = ((0,255,0))
        elif couleur == "bleu":
            self.couleur = ((0,0,255))
        elif couleur== "jaune":
            self.couleur = ((255,127,39))
        else:
            self.couleur = ((255,255,255))
        self.id_camp = id_camp
        self.joueurs = []
        self.pieces_capturees = pygame.sprite.Group()
        self.pieces_depart = pygame.sprite.Group()
        self.nom = nom
        self.x = x
        self.y = y
        self.image =  pygame.image.load("images/drapeau/spawn_"+couleur+".png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def deposer(self, items):
        for it in items:
            self.pieces_capturees.add(it)

    def nbPiecesPickedUp(self):
        total = 0
        for j in self.joueurs:
            total += len(j.items)
        return total
