from Tkinter import Button
import Tkinter as tk
import time

class Accueil() :
    
    def __init__(self, ADRESSE, PORT) :
        self.ADRESSE = ADRESSE
        self.PORT = PORT



        def donnee():
            self.ADRESSE = adresse_input.get()
            self.PORT = int(port_serveur.get())
            self.NOM =  pseudo_input.get()
            validation=tk.Label(fenetre, text='Connexion de '+self.NOM+' a '+self.ADRESSE+":"+str(self.PORT)+" en cours", height=5, fg="navy")
            validation.pack()
            attente=tk.Label(fenetre, text='Veuillez patienter lors de la connexion des autres joueurs', height=2, fg="navy")
            attente.pack()
            warning=tk.Label(fenetre, text='La fenetre de connexion va se fermee automatiquement dans 5 secondes ', height=2, fg="navy")
            warning.pack()
            fenetre.update()
            time.sleep(5)
            fenetre.quit()



        fenetre = tk.Tk()
        fenetre.title("Broken Pipe")
        fenetre.geometry("500x500+500+500")
        titre_principal = tk.Label ( fenetre, text="Broken Pipe Connexion" )
        espace = tk.Label(fenetre, text="")
 
        # l'objet Label() nomm? texte est ensuite
        # rendu visible dans fenetre gr?ce ? pack()
        espace.pack()
        titre_principal.pack()
 
        # pour finir, on lance la boucle programme
 
        adresse_label=tk.Label(fenetre, text='Adresse du serveur :', width=20, height=3, fg="navy")
        adresse_label.pack()
        adresse_input=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        adresse_input.set("sixfoisneuf.fr")  # facultatif: assigne une valeur ? la variable

        saisie_default=tk.Entry(textvariable=adresse_input, width=30)
        saisie_default.pack()
        
        port_label=tk.Label(fenetre, text='Port du serveur :', width=20, height=3, fg="navy")
        port_label.pack()
        port_serveur=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        port_serveur.set("12345")  # facultatif: assigne une valeur ? la variable
        saisie_port=tk.Entry(textvariable=port_serveur, width=30)
        saisie_port.pack()

        pseudo_label=tk.Label(fenetre, text='Pseudo :', width=20, height=3, fg="navy")
        pseudo_label.pack()
        pseudo_input=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        pseudo_input.set("Joueur")  # facultatif: assigne une valeur ? la variable
        saisie_peusdo=tk.Entry(textvariable=pseudo_input, width=30)
        saisie_peusdo.pack()
        
        b = Button(fenetre, text="Connexion",command=donnee)
        espace.pack()
        b.pack()
        
        fenetre.mainloop()

        fenetre.destroy()
