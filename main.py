__author__ = 'Simon'
from classes import jeu
import socket

#Connexion au serveur
PORT = 12345
ADRESSE_SERVEUR = 'sixfoisneuf.fr'
colliding=0

print "Connexion au serveur..."
#creation et connexion socket
socket_joueur=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_joueur.connect((ADRESSE_SERVEUR, PORT))
print "Recuperation du numero client"
numero_client = int(socket_joueur.recv(1024))
print "Vous etes le client numero "+str(numero_client)

#creation du jeu
fenetre = jeu.Jeu(numero_client,socket_joueur)
