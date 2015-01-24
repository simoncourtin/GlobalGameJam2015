import pygame
from pygame.locals import *

VELOCITY = 3
WEAPON_DAMAGE = 2
LIFE_MAX = 10

BASE_RESSOURCE = "images/"
RESSOURCES_J1 = ["sprite_profile.png", "sprite_dos.png", "sprite_face.png"]
RESSOURCES_J2 = ["sprite2_profile.png", "sprite2_dos.png", "sprite2_face.png"]
RESSOURCES_J3 = ["sprite3_profile.png", "sprite3_dos.png", "sprite3_face.png"]
RESSOURCES_J4 = ["sprite4_profile.png", "sprite4_dos.png", "sprite4_face.png"]


class Healthbar(object):
    def __init__(self, owner, unit_character="#", blank_unit_character="~"):
        self.owner = owner
        self.unit = unit_character
        self.blank_unit_character = blank_unit_character

        self.font = pygame.font.Font(None, 13)

    def displayLife(self, xAbs, yAbs):
        rendered_text = self.font.render(self.getLife(), True, (0, 0, 0))
        rendered_rect = rendered_text.get_rect()
        rendered_rect.topleft = (xAbs, yAbs)
        return rendered_text, rendered_rect

    def getLife(self):
        return self.unit * self.owner.life + self.blank_unit_character * (self.owner.life_max - self.owner.life)


    def displayName(self, xAbs, yAbs):
        rendered_text = self.font.render(self.getName(), True, (0, 0, 0))
        rendered_rect = rendered_text.get_rect()
        rendered_rect.topleft = (xAbs, yAbs)
        return rendered_text, rendered_rect

    def getName(self):
        return self.owner.name.upper()


class Player(pygame.sprite.Sprite):
    def __init__(self, jeu, classe=0, name="joueur"):
        pygame.sprite.Sprite.__init__(self)
        self.classe = classe
        self.jeu = jeu
        self.attaque = pygame.image.load("images/frappe.png").convert_alpha()
        self.afficher_attaque = False
        if name == "joueur":
            self.name = name + ' ' + str(classe + 1)
        else:
            self.name = name

        self.healthbar = Healthbar(owner=self)

        # images du personnage
        if classe == 0:
            ressources = RESSOURCES_J1
        elif classe == 1:
            ressources = RESSOURCES_J2
        elif classe == 2:
            ressources = RESSOURCES_J3
        elif classe == 3:
            ressources = RESSOURCES_J4

        self.droite = pygame.image.load(BASE_RESSOURCE + ressources[0]).convert_alpha()
        self.gauche = pygame.transform.flip(self.droite, True, False)
        self.haut = pygame.image.load(BASE_RESSOURCE + ressources[1]).convert_alpha()
        self.bas = pygame.image.load(BASE_RESSOURCE + ressources[2]).convert_alpha()
        # image actuelle du personnage
        self.image = self.droite
        # position de depart du personnage
        self.rect = self.image.get_rect()
        self.rect.x = 70
        self.rect.y = 70
        self.is_controllable = False
        self.life_max = LIFE_MAX
        self.life = 10
        self.speed = VELOCITY
        self.force = 1
        self.dash_cooldown = 0
        self.death_cooldown = -1
        # la velocite
        self.x_velocite = 0
        self.y_velocite = 0
        # les items
        self.items = []

    def reinit(self):
        respawn = pygame.mixer.Sound("respawn.ogg")
        respawn.play()
        self.rect.x = 70
        self.rect.y = 70
        self.life = LIFE_MAX

    def deplacer(self, direction):
        if direction == 'droite':
            self.x_velocite = VELOCITY * self.speed
            self.image = self.droite
        elif direction == 'gauche':
            self.x_velocite = -VELOCITY * self.speed
            self.image = self.gauche
        elif direction == 'haut':
            self.y_velocite = -VELOCITY * self.speed
            self.image = self.haut
        elif direction == 'bas':
            self.y_velocite = VELOCITY * self.speed
            self.image = self.bas


    def changerPosition(self, direction):
        if direction == 'droite':
            self.image = self.droite
        elif direction == 'gauche':
            self.image = self.gauche
        elif direction == 'haut':
            self.image = self.haut
        elif direction == 'bas':
            self.image = self.bas

    def getClasse(self):
        return self.classe

    def setX(self, x):
        self.rect.x += x

    def setY(self, y):
        self.rect.y += y

    def getX(self):
        return self.rect.x

    def getY(self):
        return self.rect.y

    def getXVelocity(self):
        return self.x_velocite

    def getYVelocity(self):
        return self.y_velocite

    def getRect(self):
        return self.rect

    def setSpeed(self, speed):
        self.speed = speed


    def getDirection(self):
        if self.image == self.droite:
            direction = 1
        elif self.image == self.gauche:
            direction = 2
        elif self.image == self.haut:
            direction = 3
        elif self.image == self.bas:
            direction = 4
        return direction

    def dash(self):
        if self.dash_cooldown <= 0:
            self.speed = 20
            self.dash_cooldown = 500
            dash= pygame.mixer.Sound("dash.ogg")
            dash.play()

    def update(self):
        if self.is_controllable:
            keys = pygame.key.get_pressed()
            if keys[K_UP]:
                self.deplacer("haut")
            if keys[K_DOWN]:
                self.deplacer("bas")
            if keys[K_RIGHT]:
                self.deplacer("droite")
            if keys[K_LEFT]:
                self.deplacer("gauche")
            if keys[K_LSHIFT]:
                self.dash()
            if not keys[K_LEFT] and not keys[K_RIGHT]:
                self.x_velocite = 0
            if not keys[K_UP] and not keys[K_DOWN]:
                self.y_velocite = 0
            if keys[K_e]:
                self.y_velocite = 0
                self.x_velocite = 0
                self.Arect = self.attaque.get_rect()
                self.afficher_attaque = True
                if self.image == self.droite:
                    self.attaque = pygame.transform.rotate(self.attaque, 90)
                    self.Arect.x = self.rect.x + 32
                    self.Arect.y = self.rect.y - 32
                elif self.image == self.gauche:
                    self.attaque = pygame.transform.rotate(self.attaque, 90)
                    self.Arect.x = self.rect.x - 32
                    self.Arect.y = self.rect.y - 32
                elif self.image == self.haut:
                    self.Arect.x = self.rect.x - 32
                    self.Arect.y = self.rect.y - 32
                elif self.image == self.bas:
                    self.attaque = pygame.transform.rotate(self.attaque, 180)
                    self.Arect.x = self.rect.x - 32
                    self.Arect.y = self.rect.y + 32

            old_x = self.rect.x
            old_y = self.rect.y
            self.setX(self.x_velocite)
            self.setY(self.y_velocite)
            collision_decors = pygame.sprite.spritecollide(self.jeu.playerById(self.jeu.id_client),
                                                           self.jeu.map.layer2.tuiles_colision, False)
            if collision_decors:
                self.rect.x = old_x
                self.rect.y = old_y

            if self.speed > VELOCITY:
                self.speed -= 1

            self.dash_cooldown -= 1
            if self.dash_cooldown < 0:
                self.dash_cooldown = 0

            self.death_cooldown -= 1
            if self.death_cooldown == 0: # Si =0, on fait repop
                self.death_cooldown = -1
                self.reinit()
            elif self.death_cooldown <= -1:
                self.death_cooldown = -1


    def getHealthbar(self):
        return self.healthbar


    def setControllable(self, boolean):
        self.is_controllable = boolean


    def attack(self, target=None):
        self.setSpeed(0)

        if len(target) > 1:
            target.remove(self)
            for ennemy in target:
                message = "ATK:%d:%d:%d@" % (self.classe, ennemy.getClasse(), WEAPON_DAMAGE)
                hit = pygame.mixer.Sound("hit.ogg")
                hit.play()
                print message
                self.jeu.socket.send(message)

    def receiveAttack(self, damage):
        if damage > self.life:
            self.life = 0
        else:
            self.life -= damage
            hit = pygame.mixer.Sound("hit.ogg")
            hit.play()


    def pickUpItem(self, item):
        print item
        self.items.append(item)
        for it in item:
            it.setVisible(False)

    def lacherItems(self):
        for item in self.items:
            item.setVisible(True)
        self.items[:] = []

    def deposerItem(self, camp):
        camp.deposer(self.items)
        self.items[:] = []

    def mourir(self):
        self.death_cooldown = 100
        self.rect.x = -30
        self.rect.y = -30
