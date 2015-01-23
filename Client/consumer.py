import threading
import socket

class Consumer(threading.Thread):
    
    def __init__(self,socket, jeu):
        threading.Thread.__init__(self)
        self.socket = socket
        self.jeu = jeu
        
    def recevoirDonneesServeur(self):
        request = self.socket.recv(1024)
        donnee = request.split(':')
        numero =int(donnee[0])
        donnee = donnee[1].split(',')
        x = int(donnee[0])
        y = int(donnee[1])
        self.jeu.joueurs[numero].rect.x = x
        self.jeu.joueurs[numero].rect.y = y
    def run(self):
        while True:
            self.recevoirDonneesServeur()
    
    
    