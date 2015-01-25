import threading
import socket
import pygame

class Consumer(threading.Thread):
    
    def __init__(self,socket, jeu):
        threading.Thread.__init__(self)
        self.socket = socket
        self.jeu = jeu
        self.death_cooldown = 0
        
    def recevoirDonneesServeur(self):
        request = ""
        car = self.socket.recv(1)
        while car != "@":
            request += car
            car = self.socket.recv(1)
        
        donnee = request.split(':')
        donnee[-1] = donnee[-1].strip("@")
        if donnee[0] == "ATK":
            attaquant = donnee[1]
            attaque = donnee[2]
            damage = donnee[3]

            if int(attaque) == self.jeu.id_client:
                # C'est notre joueur
                joueur_attaque = self.jeu.playerById(self.jeu.id_client)
                joueur_attaque.receiveAttack(int(damage))

            # Ensuite on verifie si le perso est mort, si oui on l'enleve
            joueur_attaque = self.jeu.playerById(int(attaque))
            if joueur_attaque.life <= 0:
                death = pygame.mixer.Sound("death.ogg")
                death.play()
                # Il est mort
                joueur_attaque.mourir()
                
        elif donnee[0] == "ITM_PK": # Item Pick (on ramasse un item)
            id_camp = int(donnee[1])
            id_item = int(donnee[2])
            id_joueur = int(donnee[3])

            joueur = self.jeu.playerById(id_joueur)
            item = self.jeu.itemById(id_item)
            camp = self.jeu.campById(id_camp)
            
            joueur.items.append(item)
            self.jeu.items_taken.add(item)
            self.jeu.items.remove(item)
            print joueur.name + " a recupere un item d'id " + str(id_item)

        elif donnee[0] == "ITM_RL": # Item Release (on depose un item au camp)
            id_joueur = int(donnee[1])

            joueur = self.jeu.playerById(id_joueur)
            camp = joueur.camp

            for it in joueur.items:
                camp.pieces_capturees.append(it)
                it.camp.pieces_depart.remove(it)
                joueur.items.remove(it)

            print joueur.name + " a depose ses pieces."

        elif donnee[0] == "ITM_DR": # Item Drop (il meurt et repose ses items)
            id_joueur = int(donnee[1])
            
            joueur = self.jeu.playerById(id_joueur)

            for it in joueur.items:
                self.jeu.items.add(it)
                self.jeu.items_taken.remove(it)
            
            joueur.lacherItems()
            print joueur.name + " est mort est a lache ses pieces"
            
        
        else: # Position
            numero = int(donnee[0])
            coords = donnee[1].split(',')
            donnee[2] = donnee[2]
            x = int(coords[0])
            y = int(coords[1])
            life = int(donnee[2])
            
            #changement de direction du personnage
            
            if(self.jeu.playerById(numero).rect.x<x):
                self.jeu.playerById(numero).changerPosition("droite")
            elif(self.jeu.playerById(numero).rect.x>x):
                self.jeu.playerById(numero).changerPosition("gauche")
                
            if(self.jeu.playerById(numero).rect.y<y):
                self.jeu.playerById(numero).changerPosition("bas")
            elif(self.jeu.playerById(numero).rect.y>y):
                self.jeu.playerById(numero).changerPosition("haut")
        
            self.jeu.playerById(numero).rect.x = x 
            self.jeu.playerById(numero).rect.y = y
            self.jeu.playerById(numero).life = life

        
    def run(self):
        while True:
            self.recevoirDonneesServeur()
            self.death_cooldown -= 1
            if self.death_cooldown < 0:
                self.death_cooldown = 0
    
    
    
