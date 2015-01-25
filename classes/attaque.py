import pygame

RESSOURCE = "images/frappe.png"

HAUT = 'haut'
BAS = 'bas'
GAUCHE = 'gauche'
DROITE = 'droite'


class Attaque(pygame.sprite.Sprite):
    def __init__(self, joueur):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(RESSOURCE).convert_alpha()
        self.rect = self.image.get_rect()

        self.joueur = joueur

        self.images = {
            HAUT: self.image,
            BAS: pygame.transform.rotate(self.image, 180),
            GAUCHE: pygame.transform.rotate(self.image, 90),
            DROITE: pygame.transform.rotate(self.image, 270)
        }

        self.direction = BAS

    def update(self):
        self.image = self.images[self.direction]

        if self.direction == HAUT:
            self.rect.x = self.joueur.rect.x - 10
            self.rect.y = self.joueur.rect.y - 32

        elif self.direction == BAS:
            self.rect.x = self.joueur.rect.x - 10
            self.rect.y = self.joueur.rect.y + 32

        elif self.direction == GAUCHE:
            self.rect.x = self.joueur.rect.x - 32
            self.rect.y = self.joueur.rect.y - 10

        elif self.direction == DROITE:
            self.rect.x = self.joueur.rect.x + 32
            self.rect.y = self.joueur.rect.y - 10


