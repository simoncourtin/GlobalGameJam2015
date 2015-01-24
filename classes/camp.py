
import pygame

CAMP_SIZE = 80

class Camp(pygame.sprite.Sprite):

    def __init__(self, id_camp, x, y, nom="equipe", couleur=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        
        self.id_camp = id_camp
        self.joueurs = []
        self.pieces_capturees = []
        self.pieces_depart = []
        self.nom = nom
        self.couleur = couleur
        self.x = x
        self.y = y
        self.image = pygame.Surface((CAMP_SIZE, CAMP_SIZE))
        self.image.fill(couleur)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def deposer(self, items):
        self.pieces_capturees.extend(items)
