import tkinter as tk

# Créer la fenêtre
root = tk.Tk()
root.title("Jeu de maths")
root.geometry("300x200")

# Ajouter un label
label = tk.Label(root, text="Bienvenue dans le jeu !")
label.pack(pady=10)

# Ajouter un bouton
button = tk.Button(root, text="Commencer")
button.pack()

# Lancer l'appli
root.mainloop()
