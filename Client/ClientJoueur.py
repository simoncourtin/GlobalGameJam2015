#! /usr/bin/env python
#̣ coding : utf-8
import socket

PORT = 12345
ADRESSE_SERVEUR = '10.45.30.96'

socket_joueur1=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_joueur1.connect((ADRESSE_SERVEUR, PORT))
    
while True:
    msg=raw_input("Saisissez votre message : ")
    socket_joueur1.send(msg)