import tkinter as tk
import random
import threading
import speech_recognition as sr

# === Configuration ===
NOMBRE_MAX = 10
TEMPS_PAR_QUESTION = 10
NOMBRE_DE_QUESTIONS = 10

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

    if total >= NOMBRE_DE_QUESTIONS:
        fin_du_jeu()
        return

    a = random.randint(1, NOMBRE_MAX)
    b = random.randint(1, NOMBRE_MAX)
    op = random.choice(['+', '-'])

    op = '+'  # Forcing addition for testing
    if op == '+':
        current_answer = a + b
    else:
        if a < b:
            a, b = b, a
        current_answer = a - b

    current_question = f"{a} {op} {b}"
    question_label.config(text=f"{current_question} = ?")
    total += 1
    update_score_label()

    temps_restant = TEMPS_PAR_QUESTION
    update_timer()
    demarrer_chrono()
    status_label.config(text="🎤 En attente de la réponse vocale...")
    fenetre.after(500, lancer_thread_micro)

def fin_du_jeu():
    arret_chrono()
    question_label.config(text="🎉 Bravo ! 🎉")
    status_label.config(text="Fin du jeu ! Tu peux recommencer.")
    timer_label.config(text="")
    ajouter_historique(f"\n🎯 Score final : {score}/{total}")
    bouton_recommencer.pack(pady=10)  # Affiche le bouton


def traiter_reponse(reponse):
    global score
    arret_chrono()
    try:
        if reponse == current_answer:
            score += 1
            ajouter_historique(f"{current_question} = {reponse} ✅")
        else:
            ajouter_historique(f"{current_question} = {reponse} ❌ (attendu : {current_answer})")
    except ValueError:
        ajouter_historique(f"{current_question} = ??? ❌ (entrée invalide)")

    nouvelle_operation()

def update_score_label():
    score_label.config(text=f"Score : {score}/{total}")

def lancer_thread_micro():
    thread = threading.Thread(target=ecouter_et_reconnaitre)
    thread.start()

def ecouter_et_reconnaitre():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="🎤 Écoute en cours...")
            fenetre.update()
            audio = recognizer.listen(source, timeout=TEMPS_PAR_QUESTION)

            status_label.config(text="⏳ Reconnaissance...")
            fenetre.update()
            texte = recognizer.recognize_google(audio, language="fr-FR")
            reponse = int(texte)
            fenetre.after(0, lambda: traiter_reponse(reponse))
            status_label.config(text="✅ Réponse vocale enregistrée")
        except sr.UnknownValueError:
            status_label.config(text="❌ Je n'ai pas compris.")
            fenetre.after(0, lambda: traiter_reponse("???"))
        except sr.RequestError:
            status_label.config(text="❌ Erreur de connexion.")
            fenetre.after(0, lambda: traiter_reponse("???"))
        except ValueError:
            status_label.config(text="❌ Ce n'était pas un nombre.")
            fenetre.after(0, lambda: traiter_reponse("???"))

def ajouter_historique(texte):
    historique_text.config(state="normal")
    historique_text.insert(tk.END, texte + "\n")
    historique_text.see(tk.END)
    historique_text.config(state="disabled")

def update_timer():
    timer_label.config(text=f"⏱ {temps_restant} sec")
    if temps_restant > 5:
        timer_label.config(fg="green", font=("Arial Rounded MT Bold", 28))
    elif temps_restant > 3:
        timer_label.config(fg="orange", font=("Arial Rounded MT Bold", 32))
    else:
        timer_label.config(fg="red", font=("Arial Rounded MT Bold", 36))

def compte_a_rebours():
    global temps_restant
    temps_restant -= 1
    update_timer()
    if temps_restant <= 0:
        status_label.config(text="⏱ Temps écoulé")
        traiter_reponse("Temps")
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



def recommencer_jeu():
    global score, total, historique_text
    score = 0
    total = 0
    historique_text.config(state="normal")
    historique_text.delete("1.0", tk.END)
    historique_text.config(state="disabled")
    bouton_recommencer.pack_forget()
    status_label.config(text="")
    nouvelle_operation()


# === Interface ===
fenetre = tk.Tk()
fenetre.title("🎉 Jeu de maths magique 🎲")
fenetre.geometry("700x400")
fenetre.configure(bg="#ffeef8")

main_frame = tk.Frame(fenetre, bg="#ffeef8")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_frame = tk.Frame(fenetre, bg="#fffaf0", width=200)
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

question_label = tk.Label(main_frame, text="", font=("Comic Sans MS", 28), bg="#ffeef8", fg="#333")
question_label.pack(pady=10)

timer_label = tk.Label(main_frame, text="", font=("Arial Rounded MT Bold", 32), bg="#ffeef8")
timer_label.pack()

score_label = tk.Label(main_frame, text="Score : 0/0", font=("Comic Sans MS", 16), bg="#ffeef8")
score_label.pack(pady=10)

status_label = tk.Label(main_frame, text="", font=("Comic Sans MS", 14), fg="gray", bg="#ffeef8")
status_label.pack(pady=5)

historique_title = tk.Label(right_frame, text="📜 Historique", font=("Comic Sans MS", 14, "bold"), bg="#fffaf0")
historique_title.pack(pady=5)

historique_text = tk.Text(right_frame, width=30, height=20, state="disabled", font=("Courier", 10), bg="#fffaf0")
historique_text.pack(padx=5, pady=5)

# Bouton Recommencer (caché au départ)
bouton_recommencer = tk.Button(main_frame, text="🔄 Recommencer", font=("Comic Sans MS", 14),
                               bg="#ffd", command=recommencer_jeu)


# Lancement
nouvelle_operation()
fenetre.mainloop()
