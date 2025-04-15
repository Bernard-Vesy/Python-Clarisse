import tkinter as tk
import random
import speech_recognition as sr

# === Configuration ===
NOMBRE_MAX = 10
TEMPS_PAR_QUESTION = 10

# === Variables globales ===
score = 0
total = 0
current_answer = 0
current_question = ""
chrono = None
temps_restant = TEMPS_PAR_QUESTION

# === Fonctions ===

def nouvelle_operation():
    global current_answer, total, current_question, temps_restant

    a = random.randint(1, NOMBRE_MAX)
    b = random.randint(1, NOMBRE_MAX)
    #op = random.choice(['+', '-'])
    op = '+' 
    if op == '+':
        current_answer = a + b
    else:
        if a < b:
            a, b = b, a
        current_answer = a - b

    current_question = f"{a} {op} {b}"
    question_label.config(text=f"{current_question} = ?")
    entry.delete(0, tk.END)
    total += 1
    update_score_label()

    temps_restant = TEMPS_PAR_QUESTION
    update_timer()
    demarrer_chrono()

def valider_reponse(forced=False):
    global score
    arret_chrono()
    try:
        reponse = int(entry.get())
        if reponse == current_answer:
            score += 1
            ajouter_historique(f"{current_question} = {reponse} ✅")
        else:
            ajouter_historique(f"{current_question} = {reponse} ❌ (attendu : {current_answer})")
    except ValueError:
        if forced:
            ajouter_historique(f"{current_question} = ❌ Temps écoulé (attendu : {current_answer})")
        else:
            ajouter_historique(f"{current_question} = ??? ❌ (entrée invalide)")

    nouvelle_operation()

def update_score_label():
    score_label.config(text=f"Score : {score}/{total}")

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
            reponse = int(texte)

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

def ajouter_historique(texte):
    historique_text.config(state="normal")
    historique_text.insert(tk.END, texte + "\n")
    historique_text.see(tk.END)
    historique_text.config(state="disabled")

def update_timer():
    timer_label.config(text=f"⏱ Temps : {temps_restant}s")

def compte_a_rebours():
    global temps_restant
    temps_restant -= 1
    update_timer()
    if temps_restant <= 0:
        valider_reponse(forced=True)
    else:
        global chrono
        chrono = fenetre.after(1000, compte_a_rebours)

def demarrer_chrono():
    global chrono
    arret_chrono()
    chrono = fenetre.after(1000, compte_a_rebours)

def arret_chrono():
    global chrono
    if chrono is not None:
        fenetre.after_cancel(chrono)
        chrono = None

# === Interface ===
fenetre = tk.Tk()
fenetre.title("Jeu de maths 🎲")
fenetre.geometry("650x320")
fenetre.configure(bg="#f0f8ff")

# Partie principale
main_frame = tk.Frame(fenetre, bg="#f0f8ff")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Panneau latéral (historique)
right_frame = tk.Frame(fenetre, bg="#e6f2ff", width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

question_label = tk.Label(main_frame, text="", font=("Arial", 24), bg="#f0f8ff")
question_label.pack(pady=10)

entry = tk.Entry(main_frame, font=("Arial", 20), justify='center')
entry.pack()

valider_button = tk.Button(main_frame, text="Valider ✏️", command=valider_reponse, font=("Arial", 12))
valider_button.pack(pady=5)

micro_button = tk.Button(main_frame, text="Répondre au micro 🎤", command=ecouter_et_reconnaitre, font=("Arial", 12))
micro_button.pack()

status_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="gray", bg="#f0f8ff")
status_label.pack(pady=5)

timer_label = tk.Label(main_frame, text=f"⏱ Temps : {TEMPS_PAR_QUESTION}s", font=("Arial", 14), bg="#f0f8ff")
timer_label.pack()

score_label = tk.Label(main_frame, text="Score : 0/0", font=("Arial", 14), bg="#f0f8ff")
score_label.pack(pady=5)

# Historique
historique_title = tk.Label(right_frame, text="Historique", font=("Arial", 14, "bold"), bg="#e6f2ff")
historique_title.pack(pady=5)

historique_text = tk.Text(right_frame, width=30, height=20, state="disabled", font=("Courier", 10))
historique_text.pack(padx=5, pady=5)

# Démarrage
nouvelle_operation()
fenetre.mainloop()
