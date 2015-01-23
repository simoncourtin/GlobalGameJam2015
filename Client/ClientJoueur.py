#! /usr/bin/env python
#̣ coding: utf-8
import socket

PORT = 12345
ADRESSE_SERVEUR = 'sixfoisneuf.fr'

socket_joueur1=socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
socket_joueur1.connect((ADRESSE_SERVEUR, PORT))
numero_client = socket_joueur1.recv(1024)
message = "attente"
while not message == "CHARGEZ":
    message = socket_joueur1.recv(1024)
    
#chargement
socket_joueur1.send("READY")
for i in range (0,2) :
    message = socket_joueur1.recv(1024)

while True :
    wait(0.01)
    socket_joueur1.send(numero_client+":0,0")
    message = socket_recv(1024)
    
