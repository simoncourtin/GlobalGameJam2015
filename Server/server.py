#!/usr/bin/python
# coding: utf8

'''
   Basic parallel server
'''

import socket
import signal
import sys
import time
import os

list_client = []

PORT = 12344
BUFFER_SIZE = 2048
MAX_PLAYERS = 2

# DARTH VADER ****
def kill_zombie(signum, frame):
    print('Luke, I''m your father !\n')
    os.waitpid(0, 0)

# AGENT ****
def agent(socket_client, num, list_client):

    request = socket_client.recv(BUFFER_SIZE)
    while len(request) != 0:
        for socket_other in list_client:
            if request == "QUIT" :
                print "num client se deconnecte"
                socket_client.send("OK@")
                socket_client.shutdown(0)
                socket_client.close()
                sys.exit()
            if not socket_other is socket_client:
                if socket_other.send(request):
                    pass    
                
        request = socket_client.recv(BUFFER_SIZE)
    socket_client.close()
    exit(0)

# MAIN FUNCTION****
def main():

    #signal.signal(signal.SIGCHLD, kill_zombie)

    # listening socket 
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        listening_socket.bind(("0.0.0.0", PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    
    listening_socket.listen(0)
    print('Waiting for the client ...')

    # LOOP  
    for i in range(0,MAX_PLAYERS) : 
        try:
            socket_client, address_client = listening_socket.accept()
            list_client.append(socket_client)
            socket_client.send(str(i)+"\n")
            print "client "+str(i) +" arrivee"
        except socket.error:
            time.sleep(0.01)
            continue

    print "Tout le monde est connecté."
    for i in range(0,len(list_client)): 
        socket_client = list_client[i]
        pid = os.fork()
        if pid == 0:
            listening_socket.close()
            agent(socket_client, i, list_client)
        else:
            pass
            #socket_client.close()

    for i in range(0, len(list_client)):
        list_client[i].send("ALLHERE " + str(MAX_PLAYERS) + "@")

    for i in range(0, len(list_client)):
        os.wait()

# PROGRAM ENTRY
if __name__ == '__main__':
    main()
    sys.exit(0)


