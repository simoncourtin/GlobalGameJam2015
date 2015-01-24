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
        donnee[1] = donnee[1].strip("@")
        x = int(donnee[0])
        y = int(donnee[1])
        
        #changement de direction du personnage
        
        if(self.jeu.playerById(numero).xAbs<x):
            self.jeu.playerById(numero).changerPosition("droite")
        elif(self.jeu.playerById(numero).xAbs>x):
            self.jeu.playerById(numero).changerPosition("gauche")
        
        if(self.jeu.playerById(numero).yAbs<y):
            self.jeu.playerById(numero).changerPosition("bas")
        elif(self.jeu.playerById(numero).yAbs>y):
            self.jeu.playerById(numero).changerPosition("haut")
        
        xAbs = self.jeu.playerById(self.jeu.id_client).xAbs
        yAbs = self.jeu.playerById(self.jeu.id_client).yAbs
        h,w = self.jeu.playerById(self.jeu.id_client).image.get_size()
        self.jeu.playerById(numero).rect.x = (x -xAbs) * 5 +(400-w/2)
        self.jeu.playerById(numero).rect.y = (y -yAbs) * 5 +(400-h/2)
        self.jeu.playerById(numero).xAbs = x
        self.jeu.playerById(numero).yAbs = y
        
    def run(self):
        while True:
            self.recevoirDonneesServeur()
    
    
    
