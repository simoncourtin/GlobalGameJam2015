
class Camp():

    def __int__(self,nom=equipe):
        self.items = []
        self.player_team = []
        self.nom = nom

    def ajouterJoueur(self,joueur):
        self.player_team.append(joueur)

    def ajouterItem(self,item):
        self.items.append(item)

    def detruireItem(self,item):
        self.items.remove(item)

    def deposerItem(self,items):
        for item in items:
            items.camp.deposerItem(item)
