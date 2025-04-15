import tkinter as tk
import random
import speech_recognition as sr

# Variables globales
score = 0
total = 0
current_answer = 0

# Fonction pour générer une nouvelle opération
def nouvelle_operation():
    global current_answer, total
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(['+', '-'])

    if op == '+':
        current_answer = a + b
    else:
        if a < b:
            a, b = b, a  # éviter les négatifs
        current_answer = a - b

    question_label.config(text=f"{a} {op} {b} = ?")
    entry.delete(0, tk.END)
    total += 1
    update_score_label()

# Vérifie la réponse
def valider_reponse():
    global score
    try:
        reponse = int(entry.get())
        if reponse == current_answer:
            score += 1
    except ValueError:
        pass  # si la saisie n'est pas un nombre

    nouvelle_operation()

# Met à jour le score
def update_score_label():
    score_label.config(text=f"Score : {score}/{total}")

# Fonction pour écouter la voix
def ecouter_et_reconnaitre():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="🎤 Écoute...")
            fenetre.update()
            audio = recognizer.listen(source, timeout=5)

            status_label.config(text="⏳ Reconnaissance...")
            fenetre.update()
            texte = recognizer.recognize_google(audio, language="fr-FR")
            print(f"Tu as dit : {texte}")
            reponse = int(texte)  # conversion en nombre
            print(f"Réponse : {reponse}")
            # Affichage de la réponse dans un label 
            entry.delete(0, tk.END)
            entry.insert(0, str(reponse))
            valider_reponse()

            
            entry.delete(0, tk.END)
            entry.insert(0, str(reponse))
            valider_reponse()
            status_label.config(text="✅ Réponse vocale enregistrée")
        except sr.UnknownValueError:
            status_label.config(text="❌ Je n'ai pas compris.")
        except sr.RequestError:
            status_label.config(text="❌ Erreur de connexion.")
        except ValueError:
            status_label.config(text="❌ Ce n'était pas un nombre.")

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Jeu de maths 🎲")
fenetre.geometry("350x300")
fenetre.configure(bg="#f0f8ff")

question_label = tk.Label(fenetre, text="", font=("Arial", 24), bg="#f0f8ff")
question_label.pack(pady=20)

entry = tk.Entry(fenetre, font=("Arial", 20), justify='center')
entry.pack()

valider_button = tk.Button(fenetre, text="Valider ✏️", command=valider_reponse, font=("Arial", 12))
valider_button.pack(pady=10)

micro_button = tk.Button(fenetre, text="Répondre au micro 🎤", command=ecouter_et_reconnaitre, font=("Arial", 12))
micro_button.pack()

status_label = tk.Label(fenetre, text="", font=("Arial", 12), fg="gray", bg="#f0f8ff")
status_label.pack(pady=5)

score_label = tk.Label(fenetre, text="Score : 0/0", font=("Arial", 14), bg="#f0f8ff")
score_label.pack(pady=10)

nouvelle_operation()

fenetre.mainloop()
