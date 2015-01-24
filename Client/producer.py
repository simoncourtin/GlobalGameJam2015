import threading
import time
class Producer(threading.Thread):
    
    def __init__(self,socket,jeu):
        threading.Thread.__init__(self)
        self.socket = socket
        self.jeu = jeu
    
    def envoyerDonneeServeur(self):
        num=self.jeu.id_client
        x=self.jeu.playerById(num).rect.x
        y=self.jeu.playerById(num).rect.y
        life = self.jeu.playerById(num).life
        self.socket.send(str(num)+':'+str(x)+','+str(y) + ":" + str(life) + "@")
        
    def run(self):
        while True:
            time.sleep(0.05)
            self.envoyerDonneeServeur()
