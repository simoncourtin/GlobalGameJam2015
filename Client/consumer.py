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

        
    def run(self):
        while True:
            self.recevoirDonneesServeur()
    
    
    
