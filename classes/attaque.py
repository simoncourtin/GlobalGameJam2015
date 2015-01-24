import pygame

RESSOURCE = "images/frappe.png"
class Attaque(pygame.sprite.Sprite) :
    def __init__(self) :
        self.image = pygame.image.load(RESSOURCE).convert_alpha()
        self.rect = self.image.get_rect()
        self.isVisible = False
    
    def setVisible(self, boolean):
        self.isVisible = boolean