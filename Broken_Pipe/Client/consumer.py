import threading
import socket
import pygame

class Consumer(threading.Thread):
    
    def __init__(self,socket, jeu):
        threading.Thread.__init__(self)
        self.socket = socket
        self.jeu = jeu
        self.death_cooldown = 0
        self._stop = threading.Event()
        
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
                death = pygame.mixer.Sound("sounds/death.ogg")
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

            # Declenchement de la musique du stress
            if len(self.jeu.camp_rouge.pieces_depart) - self.jeu.camp_bleu.nbPiecesPickedUp() <= 2:
                if self.jeu.current_player.camp.nom == "Camp Rouge":
                    pygame.mixer.music.load("sounds/stress.ogg")
                    pygame.mixer.music.play(-1)

            if len(self.jeu.camp_bleu.pieces_depart) - self.jeu.camp_rouge.nbPiecesPickedUp() <= 2:
                if self.jeu.current_player.camp.nom == "Camp Bleu":
                    pygame.mixer.music.load("sounds/stress.ogg")
                    pygame.mixer.music.play(-1)

        elif donnee[0] == "ITM_RL": # Item Release (on depose un item au camp)
            id_joueur = int(donnee[1])

            joueur = self.jeu.playerById(id_joueur)
            camp = joueur.camp
            camp_adverse = joueur.items[0].camp

            print joueur.items

            for it in joueur.items:
                camp.pieces_capturees.add(it)
                camp_adverse.pieces_depart.remove(it)
                
            joueur.lacherItems()

            print joueur.name + " a depose ses pieces."

        elif donnee[0] == "ITM_DR": # Item Drop (il meurt et repose ses items)
            id_joueur = int(donnee[1])
            
            joueur = self.jeu.playerById(id_joueur)
            nb_pieces_avant = joueur.camp.nbPiecesPickedUp()

            for it in joueur.items:
                self.jeu.items.add(it)
                self.jeu.items_taken.remove(it)
            
            joueur.lacherItems()
            print joueur.name + " est mort est a lache ses pieces"

            nb_pieces_apres = joueur.camp.nbPiecesPickedUp()

            # On remet la musique normale
            if len(self.jeu.current_player.camp.pieces_depart) - nb_pieces_avant <= 2 and len(self.jeu.current_player.camp.pieces_depart) - nb_pieces_apres > 2:
                pygame.mixer.music.load("sounds/fondSonore.ogg")
                pygame.mixer.music.play(-1)
            
        
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
        while True :
            self.recevoirDonneesServeur()
            self.death_cooldown -= 1
            if self.death_cooldown < 0:
                self.death_cooldown = 0
    
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

