#!/usr/bin/env python2
# coding: utf-8

from classes import jeu
from functions import recup_message
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
numero_client = int(recup_message(socket_joueur))
print "Vous etes le client numero "+str(numero_client)

#creation du jeu
nbr_players_string = recup_message(socket_joueur)
nbr_players = int(nbr_players_string.split(" ")[1])

idnom = []
for i in range(nbr_players):
    idnom.append('')

socket_joueur.send("NAME "+str(numero_client) + " "+NOM+'@')

idnom[numero_client] = NOM
for i in range(0,nbr_players-1):
    resultat = recup_message(socket_joueur)
    donnee = resultat.split(' ')
    idnom[int(donnee[1])] = donnee[2]

fenetre = jeu.Jeu(numero_client,socket_joueur,idnom, donnee)
