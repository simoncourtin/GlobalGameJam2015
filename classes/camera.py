# coding: utf-8

import pygame

class Camera():

    def __init__(self, jeu, camera_func, width, height):
        #jeu
        self.jeu = jeu

        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
