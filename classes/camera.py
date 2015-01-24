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

    def apply_rect(self, rect):
        return rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, self.jeu.screen)


def simple_camera(camera, target_rect, screen):
    HALF_WIDTH = screen.get_rect().width / 2
    HALF_HEIGHT = screen.get_rect().height / 2
    l, t, _, _ = target_rect # l = left,  t = top
    _, _, w, h = camera      # w = width, h = height
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)
