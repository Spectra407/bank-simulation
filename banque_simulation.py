# Noms : Kenny Ly et Eva Delarue

from tkinter import *
import random
import sqlite3
from PIL import ImageTk, Image
from itertools import count  # Importation de la fonction `count` pour itérer sans fin.
from datetime import datetime

'''PLUGIN POUR LA CRÉATION DE GIF SUR TKINTER'''
'''CLASS POUR L'AFFICHAGE D'IMAGE GIF'''
class ImageLabel(Label):  # Déclaration d'une classe qui hérite de `Label` pour afficher des images animées.
    """Un label qui affiche des images et simulent l'animation d'un gif"""

    def load(self, im):  # Fonction pour charger un fichier image ou GIF.
        if isinstance(im, str):  # Si l'entrée est une chaîne de caractères, cela signifie qu'il s'agit du chemin d'un fichier.
            im = Image.open(im)  # Ouvre l'image à partir du chemin spécifié.

        self.loc = 0  # Initialise un compteur pour suivre le frame courant.
        self.frames = []  # Liste pour stocker les différentes frames de l'animation.

        try:
            for i in count(1):  # Boucle pour lire chaque frame de l'image.
                # Ajoute une copie de chaque frame convertie en objet `PhotoImage` à la liste des frames.
                self.frames.append(ImageTk.PhotoImage(im.copy().resize((110, 140))))
                im.seek(i)  # Passe à la frame suivante dans l'image.
        except EOFError:  # Exception levée lorsque toutes les frames ont été lues.
            pass

        try:
            self.delay = im.info['duration']  # Tente de lire la durée entre les frames à partir des métadonnées du fichier GIF.
        except:  # En cas d'erreur (par exemple, pas de durée spécifiée), définit une valeur par défaut.
            self.delay = 100  # Définit un délai de 100 ms entre les frames.

        if len(self.frames) == 1:  # Si l'image n'a qu'une seule frame (image statique).
            self.config(image=self.frames[0])  # Configure l'image dans le label avec cette frame unique.
        else:
            self.next_frame()  # Lance l'animation en affichant les frames successives.

    def unload(self):  # Méthode pour réinitialiser l'objet et décharger l'image.
        self.config(image="")  # Réinitialise l'image affichée dans le label.
        self.frames = None  # Vide la liste des frames.

    def next_frame(self):  # Fonction récursive pour afficher les frames une par une avec un délai.
        if self.frames:  # Vérifie que des frames sont disponibles.
            self.loc += 1  # Incrémente l'index de la frame actuelle.
            self.loc %= len(self.frames)  # Revient au début de la liste si l'index dépasse le nombre total de frames.
            self.config(image=self.frames[self.loc])  # Met à jour l'image affichée.
            self.after(self.delay, self.next_frame)  # Programme un rappel pour afficher la frame suivante après le délai.


"""INITIALISATION DE LA BASE DE DONNÉES"""

connexion = sqlite3.connect("banquegrasseenne.db")     # Création/accès à la base de données de la Banque Grasséenne
cursor = connexion.cursor()         # Création du curseur

# Requête de création d'une table utilisateurs
requete = """CREATE TABLE IF NOT EXISTS utilisateurs(id TEXT PRIMARY KEY,
         mdp TEXT NOT NULL,
         argent INTEGER,
         phrase TEXT NOT NULL,
         nb_virements INTEGER)"""

cursor.execute(requete)     # Exécuter la requête
connexion.commit()          # Validation de l'exécution la requête


"""VARIABLES DE RAPPELS/GLOBALES"""
u_valide = True                 # Variable qui permet de créer des nouveaux utilisateurs
liste_ids = ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110"]  # Liste de tous les utilisateurs possibles
utilisateur_actuel = ""

contenu = cursor.execute("SELECT * FROM utilisateurs")  # On accède à toutes les IDs de la base de données

for row in contenu:  # Pour chaque ID de la base de donnée
    # On enlève de la liste les utilisateurs déjà pris, pour être certain de donner un nouvel ID à chaque fois
    liste_ids.remove(row[0])
if not liste_ids:  # Si on a déjà 10 utilisateurs, donc plus d'utilisateurs libres
    u_valide = False    # On ne peut plus créer de nouveaux utilisateurs


"""FONCTIONS"""

'''CHOIX CLIENT'''
def client():
    global utilisateur_actuel   # Pour garder en mémoire l'utilisateur qui a été entré dans connexion_application
    fen_client = Tk()           # Nom de la fenêtre pour la page des clients
    fen_client.title("Client")      # Titre de la fenêtre
    fen_client.geometry("400x600")      # Taille de la fenêtre
    fen_client.resizable(False,False)      # Taille de la fenêtre ne peut pas être modifiée

    # INITIAL TAB
    base_layer = Frame(fen_client, width=400, height=600)     # Frame de la fenêtre client sur laquelle on place les widgets
    base_layer.pack(fill="both", expand=True)  # Ensures base_layer takes up available space

    # Affichage du nom de la banque sur l'écran d'accueil
    texte_bg = Label(base_layer, text="BANQUE GRASSÉENNE")
    texte_bg.config(font=("Arial", 20, "bold"), fg = "brown4")
    texte_bg.place(relx=0.5, rely=0.25, anchor=CENTER)

    # Image initiale
    canvas = Canvas(base_layer, width=320, height=180)  # Canevas pour placer l'image d'accueil "Banque Grasséene"
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)     # Place le canevas à la moitié de la fenêtre
    Mon_image = ImageTk.PhotoImage(Image.open("client_welcome.jpg").resize((320, 180)))   # Redimensionne l'image aux dimensions du canevas
    canvas.create_image(160, 90, image=Mon_image)    # Place l'image sur le canevas
    canvas.Mon_image = Mon_image

    '''PLUGIN QUI MONTRE L'HEURE ACTUELLE SUR L'ÉCRAN D'ACCUEIL'''
    temps = (datetime.now())  # Prend la date et l'heure actuelle de l'ordinateur
    temps_actuel = temps.strftime("%H:%M")  # Conserve seulement l'heure et les minutes
    texte_temps = Label(base_layer, text=temps_actuel)
    texte_temps.config(font=("Arial", 20, "bold"))
    texte_temps.place(relx=0.5, rely=0.75, anchor=CENTER)

    def clear_all_inside_frame():
        '''Fonction pour nettoyer la page à chaque fois que l'on change d'onglet'''

        # Animation de transition entre chaque page à l'aide d'un toplevel
        top = Toplevel(fen_client)
        top.title("Renseignements d'ouverture de sessions erronées")
        top.geometry("300x100")
        top.resizable(False, False)
        texte = Label(top, text="CHARGEMENT DE LA PAGE")
        texte.config(font=("Roboto", 16, "bold"))
        texte.place(relx=0.5, rely=0.2, anchor=CENTER)

        def deplacement():    # Déplacement de la barre verte du toplevel
            fully_loaded = False
            canvas_loading_bar.move(green_bar, 5, 0)  # Déplace la barre verte de 5 pixels vers la droite
            (gauche, haut, droite, bas) = canvas_loading_bar.coords(green_bar)
            if gauche >= 0:
                fully_loaded = True    # La barre est complètement chargée

            if fully_loaded:        # Si la barre est complètement chargée, on détruit le toplevel
                top.destroy()
            else:
                top.after(30, deplacement)   # Sinon, on anime la barre verte

        # Paramètres de la barre
        canvas_loading_bar = Canvas(top, width=300, height=20, bg="dark grey")
        canvas_loading_bar.place(relx=0, rely=0.7)
        green_bar = canvas_loading_bar.create_rectangle(-300, 0, 0, 20, fill="green")

        deplacement()

        '''PLUGIN POUR EFFACER LA FENÊTRE LORSQU'ON CLIQUE SUR UN NOUVEAU MENU'''
        # Itère à travers chaque widget dans le Frame de base
        for widget in base_layer.winfo_children():  # On choisit chaque widget de la base_layer
            print(f"Clearing widget: {widget}")  # Debugging output to check each widget
            widget.destroy()  # Delete le widget


    def mon_compte():                # Menu Mon compte dans la page client
        clear_all_inside_frame()        # Nettoie la page

        contenu = cursor.execute("SELECT * FROM utilisateurs")     # On sélectionne toutes les données de la base de données

        for row in contenu:                      # Pour chaque rangée de la base de données
            if row[0] == utilisateur_actuel:     # Si l'ID est celle de l'utilisateur nommé dans connexion_application
                # On sauvegarde toutes les informations du compte dans des Labels
                texte_titre = Label(base_layer, text="Informations sur votre compte")
                texte_utilisateur = Label(base_layer, text="Votre utilisateur est : {}".format(utilisateur_actuel))
                texte_mdp = Label(base_layer, text="Votre mot de passe est : {}".format(row[1]))
                texte_argent = Label(base_layer, text="Votre solde est : {}".format(row[2]))
                texte_phrase_rappel = Label(base_layer, text="Votre phrase rappel est : {}".format(row[3]))
                texte_nb_virements = Label(base_layer, text="Votre nombre de virements effectués est : {}".format(row[4]))

                # Configuration et placement des Labels
                texte_titre.config(font=("Arial", 16, "bold"))
                texte_utilisateur.config(font=("Arial", 12))
                texte_mdp.config(font=("Arial", 12))
                texte_argent.config(font=("Arial", 12))
                texte_phrase_rappel.config(font=("Arial", 12))
                texte_nb_virements.config(font=("Arial", 12))
                texte_titre.place(relx=0.5, rely=0.1, anchor=CENTER)
                texte_utilisateur.place(x=50, rely=0.2, anchor=W)
                texte_mdp.place(x=50, rely=0.3, anchor=W)
                texte_argent.place(x=50, rely=0.4, anchor=W)
                texte_phrase_rappel.place(x=50, rely=0.5, anchor=W)
                texte_nb_virements.place(x=50, rely=0.6, anchor=W)

        # Placement de l'image en bas de la fenêtre
        canvas = Canvas(base_layer, width=400, height=200)  # Canvas pour placer l'image d'accueil
        canvas.place(x=0, y=400, anchor=NW)
        Mon_image = ImageTk.PhotoImage(Image.open("confidentiel.jpg").resize((400, 200)))
        canvas.create_image(200, 100, image=Mon_image)
        canvas.Mon_image = Mon_image


    def virements():   # Menu virements
        def open_toplevel_montant():  # Toplevel s'il y a un problème avec le montant à transférer
            top = Toplevel(fen_client)
            top.title("Erreur de montant d'argent à transférer")
            top.geometry("300x100")
            top.resizable(False, False)
            texte = Label(top, text="VEUILLEZ ENTRER UN\nNOMBRE ENTIER INFÉRIEUR\nÀ VOS SOLDES (ET >= 1)")
            texte.config(font=("Roboto", 16, "bold"), fg="red")
            texte.place(relx=0.5, rely=0.5, anchor=CENTER)

        def open_toplevel_utilisateur():   # Toplevel s'il y a un problème avec l'utilisateur choisi pour recevoir le transfert
            top = Toplevel(fen_client)
            top.title("Erreur d'ID de l'utilisateur recevant le virement")
            top.geometry("300x100")
            top.resizable(False, False)
            texte = Label(top, text="VEUILLEZ ENTRER UN\nUTILISATEUR VALIDE DE\nLA BANQUE GRASSÉENNE")
            texte.config(font=("Roboto", 16, "bold"), fg="red")
            texte.place(relx=0.5, rely=0.5, anchor=CENTER)

        def open_toplevel_transfert():    # Toplevel si le virement a été effectué
            top = Toplevel(fen_client)
            top.title("Succès du virement!")
            top.geometry("300x100")
            top.resizable(False, False)
            texte = Label(top, text="TRANSFERT EFFECTUÉ\nAVEC SUCCÈS!")
            texte.config(font=("Roboto", 16, "bold"), fg="green")
            texte.place(relx=0.5, rely=0.5, anchor=CENTER)

        def transfert_valide():   # Fonction qui vérifie si un virement peut être fait ou non, et qui le fait si c'est possible
            liste_utilisateurs_transferts = []
            utilisateur_recevant = champ_utilisateur_recevant.get()   # Variable représentant l'utilisateur qui recevra l'argent du virement
            contenu = cursor.execute("SELECT * FROM utilisateurs")

            for row in contenu:
                liste_utilisateurs_transferts.append(row[0])   # Ajoute tous les utilisateurs éligibles à un virement dans la liste

                if row[0] == utilisateur_actuel:    # Si l'itération est sur l'ID de l'utilisateur actuel
                    liste_utilisateurs_transferts.remove(utilisateur_actuel)   # On l'enlève de la liste des utilisateurs éligibles
                    argent_ua = row[2]    # On sauvegarde le montant d'argent qu'il a dans une variable
                    nb_virements = row[4]    # On sauvegarde le nombre de virements qu'il a fait dans une autre variable

                if row[0] == utilisateur_recevant:   # Si l'itération est sur l'ID de l'utilisateur recevant le virement
                    argent_ur = row[2]    # On sauvegarde le montant d'argent qu'il a dans une variable

            # Si le montant d'argent n'est pas un chiffre, qu'il est supérieur aux soldes du compte ou inférieur à 1
            if champ_montant.get().isdigit() == False or int(champ_montant.get()) > argent_ua or int(champ_montant.get()) < 1:
                open_toplevel_montant()   # On ouvre le toplevel associé au montant d'argent

            # Si l'utilisateur recevant n'est pas dans la liste des utilisateurs éligibles à un virement
            if champ_utilisateur_recevant.get() not in liste_utilisateurs_transferts:
                open_toplevel_utilisateur()    # On ouvre le toplevel associé à un mauvais utilisateur
            else:
                argent_ua -= int(champ_montant.get())  # On enlève à l'utilisateur actual le montant entré
                argent_ur += int(champ_montant.get())  # On le rajoute à l'utilisateur recevant le montant

                # On actualise la base de données en changeant les montants ainsi que le nombre de virements de l'utilisateur actuel
                requete1 = "UPDATE utilisateurs set (argent, nb_virements) = (?, ?) where id = (?)"
                requete2 = "UPDATE utilisateurs set (argent) = (?) where id = (?)"
                cursor.execute(requete1, (argent_ua, nb_virements + 1, utilisateur_actuel))
                cursor.execute(requete2, (argent_ur, utilisateur_recevant))

                connexion.commit()

                open_toplevel_transfert()    # On ouvre le toplevel qui montre que le transfert a été effectué avec succès

        clear_all_inside_frame()        # Nettoie la page

        # Création des widgets de la page des virements
        champ_montant = Entry(base_layer)
        champ_utilisateur_recevant = Entry(base_layer)
        texte_titre = Label(base_layer, text="Transferts/Virements\nd'argent à un autre compte")
        texte_champ_montant = Label(base_layer, text="Veuillez entrer un montant d'argent à transférer")
        texte_champ_utilisateur = Label(base_layer, text="Veuillez entrer un utilisateur qui recevra le virement")
        texte_titre.config(font=("Arial", 16, "bold"))
        texte_champ_montant.config(font=("Arial", 12))
        texte_champ_utilisateur.config(font=("Arial", 12))
        bouton_validation = Button(base_layer, text="Valider le transfert", command=transfert_valide)

        connexion.commit()

        # Pour sélectionner les utilisateurs valides à un virement et les mettre dans un label
        contenu = cursor.execute("SELECT * FROM utilisateurs")

        texte_utilisateurs_valides = ""
        liste_utilisateurs_possible = []

        for row in contenu:
            if row[0] == utilisateur_actuel:  # Si l'itération est sur l'ID de l'utilisateur actuel
                continue          # On ne l'ajoute pas à la liste des utilisateurs éligibles
            liste_utilisateurs_possible.append(row[0])    # On ajoute chaque ID dans la liste

        liste_utilisateurs_possible.sort()    # On trie la liste pour qu'elle soit en ordre numérique croissant

        for i in range(len(liste_utilisateurs_possible)):    # Pour chaque ID de la liste
            # On crée un string qui contient tous les utilisateurs de forme "aaa, aab, abb, etc"
            if i == 0:
                texte_utilisateurs_valides = texte_utilisateurs_valides + liste_utilisateurs_possible[i]
            else:
                texte_utilisateurs_valides = texte_utilisateurs_valides + ", " + liste_utilisateurs_possible[i]

        # On met le string créé dans un Label pour pouvoir l'afficher sur la fenêtre
        utilisateurs_possibles = Label(base_layer,
        text="Les utilisateurs auxquels vous\npouvez effectuer un virement sont : \n{}".format(texte_utilisateurs_valides))
        utilisateurs_possibles.config(font=("Arial", 12))

        # Placement de tous les widgets de Labels sur la fenêtre
        texte_titre.place(relx=0.5, rely=0.1, anchor=CENTER)
        texte_champ_montant.place(relx=0.5, rely=0.2, anchor=CENTER)
        champ_montant.place(relx=0.5, rely=0.25, anchor=CENTER)
        texte_champ_utilisateur.place(relx=0.5, rely=0.35, anchor=CENTER)
        utilisateurs_possibles.place(relx=0.5, rely=0.45, anchor=CENTER)
        champ_utilisateur_recevant.place(relx=0.5, rely=0.55, anchor=CENTER)
        bouton_validation.place(relx=0.5, rely=0.65, anchor=CENTER)

        # Placement de l'image sur la fenêtre
        canvas = Canvas(base_layer, width=200, height=100)  # Canvas pour placer l'image d'accueil
        canvas.place(x=100, y=450, anchor=NW)
        Mon_image = ImageTk.PhotoImage(Image.open("transfert_argent.jpg").resize((200, 100)))
        canvas.create_image(100, 50, image=Mon_image)
        canvas.Mon_image = Mon_image


    def fermer_la_session():    # Menu Fermer la session
        def close_window():
            fen_client.destroy()     # Détruit la fenêtre actuelle

        clear_all_inside_frame()        # Nettoie la page
        fen_client.after(2500, close_window)     # Ferme la fenêtre après 2.5 secondes
        connexion_application()    # Rouvre la page de connexion à l'application


    # Création des menus
    client_menu = Menu(fen_client)
    client_menu.add_command(label="Mon Compte", command=mon_compte)
    client_menu.add_command(label="Virements", command=virements)
    client_menu.add_command(label="Fermer la session", command=fermer_la_session)

    # Configuration des menus
    fen_client.config(menu=client_menu)
    fen_client.mainloop()


'''CHOIX ADMIN'''
def admin():
    fen_admin = Tk()     # Nom de la fenêtre pour la page admin
    fen_admin.title("Admin")        # Titre de la fenêtre
    fen_admin.geometry("400x300")       # Taille de la fenêtre
    fen_admin.resizable(False, False)       # Taille de la fenêtre ne peut pas être modifiée

    # INITIAL TAB
    base_layer = Frame(fen_admin, width=400, height=300)        # Frame de la fenêtre client sur laquelle on place les widgets
    base_layer.pack(fill="both", expand=True)  # Ensures base_layer takes up available space

    # Affichage du texte initial sur l'écran d'accueil
    text = Label(base_layer, text="Choisissez une option de\nréglages dans le menu", font=("Times New Roman", 20, "bold" ))
    text.pack()

    # Affichage du gif sur l'écran d'accueil
    label_gif = ImageLabel(base_layer)  # Crée un widget `ImageLabel` dans cette fenêtre.
    label_gif.place(x=280, y=160)  # Ajoute le widget à la fenêtre et l'organise automatiquement.
    label_gif.load('bonzibuddy-cope.gif')  # Charge un fichier GIF (ici nommé 'pacman.gif') dans le widget.

    # Affichage de l'image initale sur l'écran d'accueil
    canvas = Canvas(base_layer, width=200,  height=200)  # Canvas pour placer l'image d'accueil
    canvas.pack()       # Place le canevas en dessous du texte initial
    Mon_image = ImageTk.PhotoImage(Image.open("admin_welcome.jpg").resize((200, 200)))      # Redimensionne l'image aux dimensions du canevas
    canvas.create_image(100, 100, image=Mon_image)      # Place l'image au centre du canevas
    canvas.Mon_image = Mon_image


    def clear_all_inside_frame():
        '''Fonction pour nettoyer la page à chaque fois que l'on change d'onglet'''

        # Animation de transition entre chaque page à l'aide d'un toplevel
        top = Toplevel(fen_admin)
        top.title("Renseignements d'ouverture de sessions erronées")
        top.geometry("300x100")
        top.resizable(False, False)
        texte = Label(top, text="CHARGEMENT DE LA PAGE")
        texte.config(font=("Roboto", 16, "bold"))
        texte.place(relx=0.5, rely=0.2, anchor=CENTER)

        def deplacement():
            '''Déplacement de la barre verte du toplevel'''
            fully_loaded = False
            canvas_loading_bar.move(green_bar, 5, 0)    # Déplace la barre verte de 5 pixel vers la droite
            (gauche, haut, droite, bas) = canvas_loading_bar.coords(green_bar)
            if gauche >= 0:
                fully_loaded = True     # La barre est complètement chargée

            if fully_loaded:
                top.destroy()       # Si la barre est complètement chargée, on détruit le toplevel
            else:
                top.after(30, deplacement)      # Sinon, on anime la barre verte

        # Paramètres de la barre
        canvas_loading_bar = Canvas(top, width=300, height= 20, bg="dark grey")
        canvas_loading_bar.place(relx=0, rely=0.7)
        green_bar = canvas_loading_bar.create_rectangle(-300, 0, 0, 20, fill="green")

        deplacement()

        '''PLUGIN POUR EFFACER LA FENÊTRE LORSQU'ON CLIQUE SUR UN NOUVEAU MENU'''
        # Itère à travers chaque widget dans le Frame de base
        for widget in base_layer.winfo_children():      # On choisit chaque widget de la base_layer
            print(f"Clearing widget: {widget}")  # Debugging output to check each widget
            widget.destroy()  # Delete le widget


    def base_donnees():
        '''Fonction lorsqu'on clique sur la base de données'''
        clear_all_inside_frame()        # Nettoie la page

        # On redéfinit liste_ids à chaque fois pour s'assurer qu'il y a toujours au moins 1 compte même si on en supprime un
        liste_ids = ["101", "102", "103", "104", "105", "106", "107", "108", "109",
                     "110"]  # Liste de tous les utilisateurs possibles

        contenu = cursor.execute("SELECT * FROM utilisateurs")  # On accède à toutes les IDs de la base de données

        for row in contenu:  # Pour chaque ID de la base de donnée
            # On enlève de la liste les utilisateurs déjà pris, pour être certain de donner un nouvel ID à chaque fois
            liste_ids.remove(row[0])

        if len(liste_ids) == 10:  # Si on a 0 utilisateur dans la base de données, on va créer un nouveau compte fictif
            utilisateur = random.choice(liste_ids)  # On assigne une ID au hasard au compte fictif
            mdp = "compte fictif"       # On assigne un mot de passe arbitraire au compte fictif
            argent = random.randint(100, 500)  # On donne un montant d'argent aléatoire au compte fictif
            phrase = "placeholder"      # On assigne une phrase de rappel arbitraire au compte fictif
            nb_virements = 0        # On assigne un nombre de virements au compte fictif

            # Requête servant à insérer les nouveaux ID, mot de passe, montant d'argent, phrase de rappel et nombre de virements sélectionnés
            requete2 = """INSERT INTO utilisateurs(id, mdp, argent, phrase, nb_virements)    
                                          VALUES
                                          (?, ?, ?, ?, ?)"""

            cursor.execute(requete2, (
            utilisateur, mdp, argent, phrase, nb_virements))  # Insertion des valeurs dans la base de données

            connexion.commit()  # Validation de l'exécution de la requête

        # Contenu va contenir chaque "ligne" d'utilisateurs de la banque avec leur infos dans la forme d'une liste
        contenu = cursor.execute("select*from utilisateurs")


        texte_entier = ""
        # Afficher toutes les données sauf le mdp
        for row in contenu:  # Row contient les infos de l'etudiant dans une liste [ID, nom, email, programme]
            texte_entier += "ID : " + str(row[0]) + "\n"
            texte_entier += "solde : " + str(row[2]) + "$" + "\n"
            texte_entier += "--------------------" + "\n"
        MonTexte = Text(base_layer, width=20)       # Création d'un widget Text de 20 caractères de largeur
        MonTexte.insert("1.0", texte_entier)        # Insérer le contenu du texte
        MonTexte["state"] = "disabled"      # Empêcher d'éditer le texte écrit
        MonTexte.pack(side=LEFT)        # Place le widget texte à la gauche de l'écran

        # Image
        canvas = Canvas(base_layer, width=250, height=300)  # Canevas pour placer une image pour la page base de données
        canvas.pack(side=RIGHT)
        Mon_image = ImageTk.PhotoImage(Image.open("database.jpg").resize((250, 300)))
        canvas.create_image(125, 150, image=Mon_image)
        canvas.Mon_image = Mon_image

    def mise_a_jour():
        clear_all_inside_frame()        # Nettoie la page

        label_gif = ImageLabel(base_layer)      # Crée un widget `ImageLabel` dans cette fenêtre.
        label_gif.place(x=280, y=160)       # Ajoute le widget à la fenêtre et l'organise automatiquement.
        label_gif.load('bonzibuddy-cope.gif')       # Charge un fichier GIF (ici nommé 'pacman.gif') dans le widget.

        # Entrées de texte
        Entree_id = Entry(base_layer)       # Entrée pour le ID du compte qu'on veut modifier
        Entree_id.place(x=200, y=160, anchor=CENTER)
        Entree_argent = Entry(base_layer)       # Entrée pour le nouveau montant d'argent du compte qu'on veut modifier
        Entree_argent.place(x=200, y=190, anchor=CENTER)

        # Titres des entrées de texte
        id_label = Label(base_layer, text="ID de l'utilisateur")
        id_label.place(x=65, y=160, anchor=CENTER)
        argent_label = Label(base_layer, text="Nouveau solde")
        argent_label.place(x=65, y=190, anchor=CENTER)


        def update():
            '''Fonction pour mettre à jour le montant d'argent dans le compte de la personne'''
            id = Entree_id.get()    # ID qu'on a choisi
            nouveau_argent = Entree_argent.get()        # Nouveau montant d'argent qu'on a choisi

            # Mettre à jour l'argent de l'ID
            requete = "UPDATE utilisateurs set (argent)  =  (?) where (id) = (?)"
            cursor.execute(requete, (nouveau_argent, id))
            # Le cursor execute la requete et update l'argent de l'ID

            connexion.commit()  # Validation de l'exécution de la requête

        def delete_user():
            '''Fonction pour supprimer un utilisateur'''
            id = Entree_id.get()    # ID de la personne qu'on veut supprimer

            # Supprimer l'utilisateur
            requete = "DELETE FROM utilisateurs where (id) = (?)"
            cursor.execute(requete, (id,))  # Deletes l'utilisateur possédant cet ID

            connexion.commit()  # Validation de l'exécution de la requête

        # Notre bouton
        Update_bouton = Button(base_layer, text="Mettre à jour", width=10, command=update)
        Update_bouton.place(x=200, y=230, anchor=CENTER)
        Delete_bouton = Button(base_layer, text="Supprimer l'utilisateur", width=18, command=delete_user)
        Delete_bouton.place(x=200, y=260, anchor=CENTER)

        # Image
        canvas = Canvas(base_layer, width=220, height=140)  # Canevas pour placer l'image pour la page mise à jour
        canvas.pack(side=TOP)
        Mon_image = ImageTk.PhotoImage(Image.open("update.jpg").resize((220, 140)))
        canvas.create_image(110, 70, image=Mon_image)
        canvas.Mon_image = Mon_image

    def quitter():
        '''Fonction pour quitter l'interface admin'''
        def close_window():
            fen_admin.destroy()     # Détruit la fenêtre actuelle

        clear_all_inside_frame()        # Nettoie la page
        fen_admin.after(2500, close_window)             # Ferme la fenêtre après 2.5 secondes
        connexion_application()         # Rouvre la page de connexion à l'application

    # Création des menus
    admin_menu = Menu(fen_admin)
    admin_menu.add_command(label="Base de données", command=base_donnees)
    admin_menu.add_command(label="Mise à jour", command=mise_a_jour)
    admin_menu.add_command(label="Quitter", command=quitter)

    # Configuration des menus
    fen_admin.config(menu=admin_menu)
    fen_admin.mainloop()


'''OUVERTURE DE L'APPLICATION'''
def connexion_application():
    global utilisateur_actuel   # Garde en mémoire l'utilisateur entré

    def oubli_mdp():    # Si le bouton "mot de passe oublié?" est cliqué
        if type_connexion.get() == "2":
            return None
        liste_numeros = []    # On sauvegarde tous les IDs de la base de données dans une liste
        contenu = cursor.execute("SELECT id FROM utilisateurs")
        for row in contenu:  # Pour chaque ID de la base de donnée
            liste_numeros.append(row[0])

        print("Quel est votre numéro de compte?")   # On demande à l'utilisateur quel est son numéro de compte
        numero = input()

        boucle_numeros = True

        while boucle_numeros:
            if numero not in liste_numeros:   # Si le numéro de compte n'est pas dans la liste, on repose la question
                print("Ceci n'est pas un numéro de compte valide. Veuillez réessayer.")
                numero = input()

            else:   # S'il est valide, on sort de la boucle while
                boucle_numeros = False

        # On demande à l'utilisateur d'entrer la phrase rappel associée à son compte
        print("Veuillez taper la phrase/le mot indiqué à la création de votre mot de passe : ")
        rappel = input()

        contenu2 = cursor.execute("SELECT * FROM utilisateurs")
        for row in contenu2:
            phrase_rappel = row[3]
            # Si le numéro de compte correspond à la rangée de la base de données et que la phrase entrée correspond à la phrase rappel
            if row[0] == numero and rappel == phrase_rappel:
                print("Votre mot de passe est :", row[1])
                break     # On sort de la boucle for

    def open_toplevel():    # Fonction qui ouvre un toplevel si une des informations de connexion est erronée (mauvaise ID ou mot de passe)
        top = Toplevel(fenetre)
        top.title("Renseignements d'ouverture de sessions erronées")
        top.geometry("300x100")
        top.resizable(False, False)
        texte = Label(top, text="VEUILLEZ VÉRIFIER VOS \n DONNÉES DE CONNEXION \n ET RÉESSAYER")
        texte.config(font=("Roboto", 16, "bold"))
        texte.place(relx=0.5, rely=0.5, anchor=CENTER)

    def ouvrir_session():     # Fonction qui est activée lorsque le bouton "Ouvrir la session" est cliqué
        global utilisateur_actuel

        utilisateur_actuel = champ_entree1.get()   # On sauvegarde l'utilisateur actuel dans la variable globale

        mauvais_mdp = False
        if type_connexion.get() == "1":     # Si le type de connexion est sur connexion client
            contenu = cursor.execute("SELECT * FROM utilisateurs")
            for row in contenu:
                if champ_entree1.get() == row[0] and champ_entree2.get() == row[1]:  # Si l'ID et le mot de passe correspondent
                    mauvais_mdp = False   # Assure que lorsqu'on appelle récursivement connexion_application() dans client(), on ne commence pas avec un mauvais_mdp à True
                    fenetre.destroy()   # Détruit la fenêtre de connexion à l'application
                    client()     # Ouvre la fenêtre de client
                    break    # Arrête l'itération sur les rangées de la base de données
                else:
                    mauvais_mdp = True    # Si le mot de passe ne correspond pas à celui de la base de données, le mot de passe est mauvais
            if mauvais_mdp:
                open_toplevel()    # On ouvre alors le toplevel qui dit qu'une des données est erronée


        if type_connexion.get() == "2":     # Si le type de connexion est sur connexion admin
            if champ_entree1.get() == "adm" and champ_entree2.get() == "123":   # Si les champs ont "adm" et "123" entrés
                fenetre.destroy()       # On détruit la fenêtre de connexion à l'application
                admin()                 # On ouvre la fenêtre admin
            else:
                open_toplevel()         # Sinon, on ouvre le toplevel qui dit qu'une des données est erronée


    # Création de la fenêtre ainsi que de ses paramètres
    fenetre = Tk()
    fenetre.title("Connexion à l'application")
    fenetre.geometry("400x600")
    fenetre.resizable(False, False)

    # Variable associée aux boutons radio
    type_connexion = StringVar(fenetre, "1")

    # Création des widgets de la fenêtre
    texte_titre = Label(fenetre, text="BANQUE GRASSÉENNE")
    texte_type_connexion = Label(fenetre, text="À quel type d'utilisateur\nsouhaitez-vous vous connecter?")
    bouton_radio1 = Radiobutton(fenetre, text="Connexion CLIENT", variable=type_connexion, value="1")
    bouton_radio2 = Radiobutton(fenetre, text="Connexion ADMIN", variable=type_connexion, value="2")
    texte_connexion = Label(fenetre, text="Veuillez entrer les informations de\nvotre compte afin de vous connecter:")
    texte_champ_entree1 = Label(fenetre, text="Indiquez votre numéro de compte de client :")
    texte_champ_entree2 = Label(fenetre, text="Indiquez votre mot de passe :")

    '''PLUGIN POUR LIMITER LE NOMBRE DE CARACTÈRES D'UN CHAMP D'ENTRÉE TKINTER'''
    # Prend en argument le caractère que l'utilisateur essaie de taper et la valeur actuelle du champ d'entrée
    def validation_input(caractere, valeur):
        # Si la valeur actuelle du champ d'entrée est supérieure à 3, l'entrée est rejetée et n'est donc pas modifiable
        return len(valeur) <= 3
    # %S correspond au caractère que l'utilisateur tape et %P correspond à la valeur du champ d'entrée
    validation = (fenetre.register(validation_input), '%S', '%P')

    # Widgets de la fenêtre
    champ_entree1 = Entry(fenetre, validate="key", validatecommand=validation)
    champ_entree2 = Entry(fenetre)

    bouton_mdp_oubli = Button(fenetre, text="Mot de passe oublié?", command=oubli_mdp)
    bouton_session = Button(fenetre, text="Ouvrir une session", command=ouvrir_session)

    # Configuration de tous les widgets de la fenêtre
    texte_titre.config(font=("Arial", 20, "bold"), fg="brown4")
    texte_type_connexion.config(font=("Arial", 16, "bold"))
    texte_connexion.config(font=("Arial", 16, "bold"))
    bouton_radio1.config(font=("Arial", 12))
    bouton_radio2.config(font=("Arial", 12))
    texte_champ_entree1.config(font=("Arial", 12))
    texte_champ_entree2.config(font=("Arial", 12))
    bouton_session.config(font=("Arial", 14), width=15)
    bouton_mdp_oubli.config(font=("Arial", 10))

    # Placement de tous les widgets sur la fenêtre
    texte_titre.place(relx=0.5, rely=0.06, anchor=CENTER)
    texte_type_connexion.place(relx=0.5, rely=0.15, anchor=CENTER)
    bouton_radio1.place(relx=0.5, rely=0.25, anchor=CENTER)
    bouton_radio2.place(relx=0.5, rely=0.3, anchor=CENTER)

    texte_connexion.place(relx=0.5, rely=0.4, anchor=CENTER)
    texte_champ_entree1.place(relx=0.5, rely=0.5, anchor=CENTER)
    champ_entree1.place(relx=0.5, rely=0.55, anchor=CENTER)

    texte_champ_entree2.place(relx=0.5, rely=0.6, anchor=CENTER)
    champ_entree2.place(relx=0.5, rely=0.65, anchor=CENTER)

    bouton_session.place(relx=0.5, rely=0.75, anchor=CENTER)
    bouton_mdp_oubli.place(relx=0.5, rely=0.9, anchor=CENTER)

    fenetre.mainloop()



"""ÉTAPE 1: CHOIX DE CONNEXION"""
# Demander à l'utilisateur quel choix de connexion est souhaité
if u_valide:
    print("Bonjour,\n - Tapez A, pour vous connecter à l'Application.\n - Tapez U, pour un nouvel Utilisateur.")
    choix = input().lower()
else:
    print("Bonjour,\n - Tapez A, pour vous connecter à l'Application.")
    choix = input().lower()

boucle = True

# Boucle pour s'assurer que l'utilisateur entre "u" ou "a"
while boucle:
    if choix != "u" and choix != "a" and u_valide == True:
        print("Ceci n'est pas un choix valide.\n - Tapez A, pour vous connecter à l'Application.\n - Tapez U, pour un nouvel Utilisateur.")
        choix = input().lower()  # On redéfinit la variable choix
    elif choix != "a" and u_valide == False:   # Si l'utilisateur entre autre chose, on redemande un input
        print("Ceci n'est pas un choix valide.\n - Tapez A, pour vous connecter à l'Application.")
        choix = input().lower()          # On redéfinit la variable choix

    else:      # Si l'utilisateur entre "u" ou "a", on ferme la boucle
        boucle = False


'''ÉTAPE 2: NOUVEL UTILISATEUR'''
if choix == "u":           # Si le choix de connexion est "u", on procède vers la création d'un nouvel utilisateur
    if liste_ids:     # Si il reste des ids valides
        utilisateur = random.choice(liste_ids)  # On assigne une ID au hasard à l'utilisateur
        print("Bienvenue, voici votre numéro de compte :", utilisateur)  # On affiche le numéro de l'ID à l'utilisateur
        mdp = input("Choisissez votre mot de passe et pressez sur ENTRÉE : ")  # On lui fait choisir son mot de passe

        boucle_mdp = True
        boucle_phrase_rappel = True
        while boucle_mdp:  # On entre dans une boucle, afin que les bonnes informations soit entrées
            # La boucle ne fait que cette étape tant que l'utilisateur n'a pas entré la bonne confirmation
            confirmation_mdp = input("Confirmez votre mot de passe et pressez sur ENTRÉE : ")
            if mdp == confirmation_mdp:  # S'il entre la bonne confirmation, on entre dans la boucle de la phrase rappel
                phrase_rappel = input(
                    "Indiquez un mot ou une phrase pour vous rappeler de votre mot de passe et pressez sur ENTRÉE : ")
                while boucle_phrase_rappel:
                    # Si la phrase rappel est le mot de passe en question, ou qu'aucune phrase a été entrée, on recommence.
                    if phrase_rappel == mdp or phrase_rappel == "":
                        print("Veuillez entrer une phrase pertinente pour vous rappeler de votre mot de passe")
                        phrase_rappel = input()
                    else:
                        # On insère la phrase rappel dans un dictionnaire associé à l'ID de l'utilisateur
                        boucle_phrase_rappel = False  # On ferme les deux boucles
                        boucle_mdp = False

        argent = random.randint(100, 500)  # On donne un montant d'argent aléatoire à l'utilisateur

        # Requête servant à insérer les nouveaux ID, mot de passe et montant d'argent sélectionnés
        requete2 = """INSERT INTO utilisateurs(id, mdp, argent, phrase, nb_virements)    
                          VALUES
                          (?, ?, ?, ?, ?)"""

        cursor.execute(requete2, (utilisateur, mdp, argent, phrase_rappel, 0))  # Insertion des valeurs dans la base de données

        connexion.commit()  # Validation de l'exécution de la requête

        connexion_application()  # Démarrer la connexion à l'application


'''ÉTAPE 3: CHOIX APPLICATION'''
if choix == "a":           # Si le choix de connexion est "a", on procède vers la fonction connexion_application()
    connexion_application()  # Démarrer la connexion à l'application

connexion.close()   # On ferme la connexion à la base de données