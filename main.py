__author__ = 'Simon'
from classes import jeu
import socket
from classes import accueil
#Connexion au serveur

PORT = 345
ADRESSE_SERVEUR = 'sf.fr'

fenetre = accueil.Accueil(ADRESSE_SERVEUR, PORT)
ADRESSE_SERVEUR = fenetre.ADRESSE
PORT = fenetre.PORT
NOM = fenetre.NOM 
print "Connexion au serveur..."
#creation et connexion socket
socket_joueur=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_joueur.connect((ADRESSE_SERVEUR, PORT))
print "Recuperation du numero client"
numero_client = int(socket_joueur.recv(1024))
print "Vous etes le client numero "+str(numero_client)
#creation du jeu
request = socket_joueur.recv(1024)
print request
idnom = {
    '0': 'Joueur 1',
    '1': 'Joueur 2',
    '2': 'Joueur 3',
    '3': 'Joueur 4'
}
socket_joueur.send("NAME "+str(numero_client) + " "+NOM+'@')

car = socket_joueur.recv(1)
idnom[numero_client] = NOM
for i in range(0,3):
    request = ''
    while car != "@":
        print car
        request += car
        car = socket_joueur.recv(1)
    donnee = request.split(' ')
    print donnee
    idnom[donnee[1]] = donnee[2]
fenetre = jeu.Jeu(numero_client,socket_joueur,NOM, donnee)
