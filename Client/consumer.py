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
        numero = int(donnee[0])
        donnee = donnee[1].split(',')
        donnee = donnee.strip("@")
        x = int(donnee[0])
        y = int(donnee[1])
        
        #changement de direction du personnage
        
        if(self.jeu.joueurs.sprites()[numero].rect.x<x):
            self.jeu.joueurs.sprites()[numero].changerPosition("droite")
        elif(self.jeu.joueurs.sprites()[numero].rect.x>x):
            self.jeu.joueurs.sprites()[numero].changerPosition("gauche")
        
        if(self.jeu.joueurs.sprites()[numero].rect.y<y):
            self.jeu.joueurs.sprites()[numero].changerPosition("bas")
        elif(self.jeu.joueurs.sprites()[numero].rect.y>y):
            self.jeu.joueurs.sprites()[numero].changerPosition("haut")
          
        self.jeu.joueurs.sprites()[numero].rect.x = x
        self.jeu.joueurs.sprites()[numero].rect.y = y
    def run(self):
        while True:
            self.recevoirDonneesServeur()
    
    
    
