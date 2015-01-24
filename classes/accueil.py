from Tkinter import Button
import Tkinter as tk

class Accueil() :
    
    def __init__(self, ADRESSE, PORT) :
        self.ADRESSE = ADRESSE
        self.PORT = PORT
        fenetre = tk.Tk()
        fenetre.title("Broken Pipe")
        fenetre.geometry("500x500+500+500")
        texte = tk.Label ( fenetre, text="Broken Pipe Connection" )
 
        # l'objet Label() nomm? texte est ensuite
        # rendu visible dans fenetre gr?ce ? pack()
 
        texte.pack()
 
        # pour finir, on lance la boucle programme
 
        invite0=tk.Label(fenetre, text='Adresse du serveur :', width=20, height=3, fg="navy")
        invite0.pack()
        texte0=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        texte0.set("sixfoisneuf.fr")  # facultatif: assigne une valeur ? la variable
        saisie0=tk.Entry(textvariable=texte0, width=30)
        saisie0.pack()
        
        invite1=tk.Label(fenetre, text='Port du serveur :', width=20, height=3, fg="navy")
        invite1.pack()
        texte1=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        texte1.set("12345")  # facultatif: assigne une valeur ? la variable
        saisie1=tk.Entry(textvariable=texte1, width=30)
        saisie1.pack()

        invite2=tk.Label(fenetre, text='Pseudo :', width=20, height=3, fg="navy")
        invite2.pack()
        texte2=tk.StringVar()  # definition d'une variable-chaine pour recevoir la saisie d'un texte
        texte2.set("Joueur")  # facultatif: assigne une valeur ? la variable
        saisie2=tk.Entry(textvariable=texte2, width=30)
        saisie2.pack()
        
        b = Button(fenetre, text="OK",command=fenetre.quit)
        b.pack()
        
        fenetre.mainloop()
        self.ADRESSE = texte0.get()
        self.PORT = int(texte1.get())
        self.NOM = texte2.get()

        fenetre.destroy()
