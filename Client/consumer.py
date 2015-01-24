import threading
import socket

class Consumer(threading.Thread):
    
    def __init__(self,socket, jeu):
        threading.Thread.__init__(self)
        self.socket = socket
        self.jeu = jeu
        
    def recevoirDonneesServeur(self):
        request = ""
        car = self.socket.recv(1)
        while car != "@":
            request += car
            car = self.socket.recv(1)
        donnee = request.split(':')
        if donnee[0] == "ATK":
            attaquant = donnee[1]
            attaque = donnee[2].strip("@")

            print "Attaquant : " + attaquant
            print "Attaque : " + attaque
            if int(attaque) == self.jeu.id_client:
                print "C'est moi"
                joueur_attaque = self.jeu.playerById(self.jeu.id_client)
                joueur_attaque.receiveAttack()
                
        else: # Position
            numero = int(donnee[0])
            coords = donnee[1].split(',')
            donnee[2] = donnee[2].strip("@")
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
    
    
    
