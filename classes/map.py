__author__ = 'Simon'
import  pygame
class Map():

    def __init__(self,screen):
        self.calques = []
        self.screen =screen


    def afficher_calque(self,calque):
        for element in calque:
            if element > -1:
                print element
            else:
                print element

    def afficher_map(self):
        for calque in self.calques:
            self.afficher_calque(calque)





pygame.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption('Play game')
map = Map(screen)
pygame.display.flip()

while True:
    print "ca tourne"