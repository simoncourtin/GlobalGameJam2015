import thread
class Producer(thread.Thread):
    
    def __init__(self,socket,jeu):
        self.socket = socket
        self.jeu = jeu
    
    def envoyerDonneeServeur(self):
        num=self.jeu.id_client
        x=self.joueurs[num].rect.x
        y=self.joueurs[num].rect.y
        self.socket.send(str(num)+':'+str(x)+','+str(y))
        
    def run(self):
        while True:
            self.envoyerDonneeServeur()