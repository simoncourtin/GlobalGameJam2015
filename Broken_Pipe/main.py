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

socket_joueur=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_joueur.connect((ADRESSE_SERVEUR, PORT))

fenetre = jeu.Jeu(NOM,socket_joueur)
